"""
Module implementing checks for disallowed composition of Clarity components.
"""
# Copyright 2023 VMware, Inc.
# SPDX-License-Identifier: MIT

import csv
import logging
import os.path
import re
from typing import Dict, Generator, Iterable, List, Set, Tuple

from selenium.webdriver.common import by
from selenium.webdriver.remote import webelement

from crest.composition import clarity_components
from crest import config
from crest.utils import operation


class ClarityComposition(operation.Operation):
    """
    Class implementing checks for disallowed composition of Clarity components.
    """

    DISALLOWED_COMPOSITIONS_CSV_FILENAME = "clarity_disallowed_composition.csv"
    SKIP_COMPONENTS = {"CONTROL"}

    _COMPONENT_NAME_SPLIT_RE = re.compile("[-/(]")
    _disallowed_compositions: Dict[
        clarity_components.Component, Set[clarity_components.Component]
    ] = {}

    @staticmethod
    def _clean_component_name(name: str) -> str:
        """
        Converts the name of a component from the disallowed compositions CSV
        into the name in the name supposed to match a component defined in
        clarity_components.py.

        :param name: The component name from the CSV file.
        :return: The component name with no spaces, all uppercase.
        """
        return (
            ClarityComposition._COMPONENT_NAME_SPLIT_RE.split(name, 1)[0]
            .strip()
            .upper()
            .replace(" ", "_")
        )

    @staticmethod
    def _convert_disallowed_composition_table(
        table: Dict[str, Set[str]]
    ) -> Dict[clarity_components.Component, Set[clarity_components.Component]]:
        """
        Convert a table with strings as component identifiers into a table with
        clarity_components.Component objects as component identifiers.

        :param table: The input table with strings as components identifiers.
        :return: The output table with Component objects as objects identifiers.
        """
        output_table: Dict[
            clarity_components.Component, Set[clarity_components.Component]
        ] = {}
        for outer_name, inners_name in table.items():
            outer_component = clarity_components.Components[outer_name].value
            output_table[outer_component] = {
                clarity_components.Components[i].value for i in inners_name
            }
        return output_table

    @classmethod
    def _load_disallowed_compositions(cls):
        """
        Parse the CSV file containing the disallowed Clarity component
        compositions.
        The columns are the outer/container components, while the rows are the
        inner/contained components. A specific composition is disallowed if "n"
        is in the corresponding cell.
        """
        if cls._disallowed_compositions:
            # Already initialized.
            # It could end up parsing the table twice in a multithreading
            # environment, but it would not be an issue as
            # _disallowed_compositions is updated atomically.
            return
        logger = logging.getLogger(__name__).getChild(cls.__name__)
        csv_filename = os.path.join(
            os.path.dirname(__file__), cls.DISALLOWED_COMPOSITIONS_CSV_FILENAME
        )
        logger.info("Parsing disallowed Clarity compositions from %s", csv_filename)
        with open(csv_filename, newline="", encoding="ascii") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",")
            headers = next(csv_reader)
            outer_containers = [cls._clean_component_name(i) for i in headers[1:]]
            disallowed_compositions_table = {}
            for i in outer_containers:
                if i not in cls.SKIP_COMPONENTS:
                    disallowed_compositions_table[i] = set()
            for row in csv_reader:
                inner = cls._clean_component_name(row[0])
                for outer, decision in zip(outer_containers, row[1:]):
                    if (
                        decision == "n"
                        and outer not in cls.SKIP_COMPONENTS
                        and inner not in cls.SKIP_COMPONENTS
                    ):
                        disallowed_compositions_table[outer].add(inner)
        cls._disallowed_compositions = cls._convert_disallowed_composition_table(
            disallowed_compositions_table
        )
        logger.info("Loaded %d outer components", len(cls._disallowed_compositions))

    def __init__(self, url: str, locator: int = config.global_args["reporttype"]):
        super().__init__(url, locator)
        self._load_disallowed_compositions()
        self._totalelements = 0

    def _main(self, response: operation.Response):
        """
        Entry point for the Clarity composition checks.

        :param response: The Response that will be updated with the outcome of
            the Clarity composition checks.
        """
        items: Dict[str, operation.Item] = {}
        for outer_component, outer_element in self._find_outer_elements():
            self._totalelements += 1
            for (
                disallowed_inner_component,
                disallowed_inner_elements,
            ) in self._find_disallowed_inner_elements(outer_component, outer_element):
                self._create_or_append_to_item(
                    items,
                    outer_component,
                    disallowed_inner_component,
                    disallowed_inner_elements,
                )
        categories = operation.Categories()
        if items:
            categories.error = operation.Issue(description="Errors", items=items)
        response.categories = categories
        response.statistics.totalelements = self._totalelements

    def _find_outer_elements(
        self,
    ) -> Generator[
        Tuple[clarity_components.Component, webelement.WebElement], None, None
    ]:
        """
        Generator yielding all elements in the webpage that can be the container
        of a disallowed component.

        :yield: A tuple containing the Clarity component definition and
            corresponding Selenium WebElement reference.
        """
        for outer_component in self._disallowed_compositions:
            if outer_component is None:
                continue
            for outer_selector in outer_component.css_selectors:
                self._logger.debug(
                    "Searching for elements of type %s with CSS selector %s",
                    outer_component.name,
                    outer_selector,
                )
                for outer_element in self._driver.find_elements(
                    by.By.CSS_SELECTOR, outer_selector
                ):
                    self._logger.debug("Found element %s", outer_selector)
                    yield outer_component, outer_element

    def _find_disallowed_inner_elements(
        self,
        outer_component: clarity_components.Component,
        outer_element: webelement.WebElement,
    ) -> Generator[
        Tuple[clarity_components.Component, List[webelement.WebElement]], None, None
    ]:
        """
        Generator yielding all elements in the webpage contained inside the
        specified component and that are not allowed to be contained in a
        component of that type.

        :param outer_component: The Component definition of the container.
        :param outer_element: The WebElement reference of the container.
        :yield: A tuple containing the Clarity component definition and
            corresponding Selenium WebElement reference.
        """
        for disallowed_inner_component in self._disallowed_compositions[
            outer_component
        ]:
            if disallowed_inner_component is None:
                continue
            inner_selector = ",".join(disallowed_inner_component.css_selectors)
            self._logger.debug(
                "Searching for inner elements of type %s with CSS selector %s",
                disallowed_inner_component.name,
                inner_selector,
            )
            disallowed_inner_elements = outer_element.find_elements(
                by.By.CSS_SELECTOR, inner_selector
            )
            if disallowed_inner_elements:
                self._logger.debug("Found inner element %s", inner_selector)
                yield disallowed_inner_component, disallowed_inner_elements

    def _create_or_append_to_item(
        self,
        items: Dict[str, operation.Item],
        outer_component: clarity_components.Component,
        disallowed_inner_component: clarity_components.Component,
        disallowed_inner_elements: Iterable[webelement.WebElement],
    ):
        """
        Given a container component and a disallowed inner component, compute
        the ID corresponding to this disallowed component composition.
        In the dict with issue item IDs and corresponding Item objects, create a
        new issue Item with the computed ID, or update the existing one, adding
        the xpath or CSS selector path for the disallowed inner component.

        :param items: The dict of issue item IDs and corresponding Item object.
        :param outer_component: The Component definition of the container.
        :param disallowed_inner_component: The Component definition of the
            disallowed inner component.
        :param disallowed_inner_elements: The WebElement reference of the
            disallowed inner component.
        """
        disallowed_inner_component_name = disallowed_inner_component.name.replace(
            " ", "_"
        )
        outer_component_name = outer_component.name.replace(" ", "_")
        item_id = f"cc_{disallowed_inner_component_name}_in_{outer_component_name}"
        if item_id in items:
            if self._locator == operation.Locator.XPATH.value:
                items[item_id].xpaths += [
                    self.get_xpath(e) for e in disallowed_inner_elements
                ]
            else:
                items[item_id].selectors += [
                    self.get_css_path(e) for e in disallowed_inner_elements
                ]

        else:
            xpaths = None
            selectors = None
            if self._locator == operation.Locator.XPATH.value:
                xpaths = [self.get_xpath(e) for e in disallowed_inner_elements]
            else:
                selectors = [self.get_css_path(e) for e in disallowed_inner_elements]

            items[item_id] = operation.Item(
                id=item_id,
                description=f"Found `{disallowed_inner_component.name}` element contained inside a"
                f" `{outer_component.name}` element, which is not allowed",
                selectors=selectors,
                xpaths=xpaths,
            )
