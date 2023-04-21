"""
Module providing the common code for a Crest operation.
"""
# Copyright 2023 VMware, Inc.
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
import dataclasses
import enum
import logging
import time
from typing import Any, Collection, Dict, List, Optional, Tuple

from selenium.webdriver.remote import webelement

from crest import config
from crest import utils
from crest.utils import get_common_function


class Locator(enum.Enum):
    """
    Enumeration of possible HTML element locator types.
    """

    UNSPECIFIED = -1
    XPATH = 3
    CSS_SELECTOR = 4


@dataclass
class Item:
    """
    Item contained in an Issue reported by Crest.
    """

    description: str
    id: str  # pylint: disable=invalid-name
    count: int = 0
    level: Optional[str] = None
    selectors: Optional[List[str]] = None
    xpaths: Optional[List[str]] = None


@dataclass
class Issue:
    """
    Issue container reported by Crest. It could be an alert or an error.
    """

    description: str
    items: Dict[str, Item]
    count: int = 0


@dataclass
class Categories:
    """
    Categories of issues reposted by Crest.
    """

    alert: Optional[Issue] = None
    error: Optional[Issue] = None


@dataclass
class Statistics:
    """
    Statistics reported by Crest.
    """

    pageurl: str
    allitemcount: int = 0
    time: Optional[float] = None
    totalelements: Optional[int] = None


@dataclass
class Status:
    """
    Operation status reported by Crest.
    """

    success: bool
    error: Optional[str] = None
    httpstatuscode: Optional[int] = None


@dataclass
class Response:
    """
    Response to a Crest operation.
    """

    statistics: Statistics
    categories: Optional[Categories] = None
    status: Optional[Status] = None

    def asdict(self) -> Dict[str, Any]:
        """
        Convert the Response object to nested dict representation, suitable
        for serialization as JSON.

        :return: The dict representation of this Response object.
        """
        return dataclasses.asdict(self, dict_factory=self._dictfactory)

    @staticmethod
    def _dictfactory(fields: Collection[Tuple[str, Any]]) -> Dict[str, Any]:
        """
        Convert a collection of tuples (key, value) into a dict {key: value},
        omitting keys whose value is None.

        :param fields: A collection of (key, value) tuples.
        :returns: The {key, value} dict with no None value.
        """
        return dict(f for f in fields if f[1] is not None)


class Operation:
    """
    Base class for a Crest operation.
    """

    def __init__(self, url: str, locator: int = config.global_args["reporttype"]):
        self._logger = logging.getLogger(self.__class__.__module__).getChild(
            self.__class__.__name__
        )
        self._driver = get_common_function.get_driver()
        self._logger.info("Fetching URL %s", url)
        self._pageurl = url
        self._driver.get(url)
        self._locator = locator
        if locator == Locator.XPATH.value:
            utils.define_absolute_xpath_fn(self._driver)
        else:
            utils.define_css_path_fn(self._driver)

    def get_css_path(self, element: webelement.WebElement) -> str:
        """
        Get the CSS selector path for the given element.

        :param element: The element whose path will be returned.
        :return: the CSS selector path of `element`.
        """
        path = self._driver.execute_script("return cssPath(arguments[0]);", element)
        return path

    def get_xpath(self, element: webelement.WebElement) -> str:
        """
        Get the xpath for the given element.

        :param element: The element whose path will be returned.
        :return: the xpath of `element`.
        """
        path = self._driver.execute_script(
            "return absoluteXPath(arguments[0]);", element
        )
        return path

    def main(self) -> Response:
        """
        The entrypoint for a Crest operation.
        """
        response = Response(statistics=Statistics(pageurl=self._pageurl))
        start_time = time.time()
        try:
            self._main(response)
            response.status = Status(httpstatuscode=200, success=True)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            self._logger.exception("Error performing crest check")
            response.status = Status(
                success=False, error=f"Failed with exception: {exc}"
            )
        finally:
            duration = round(time.time() - start_time, 2)
            response.statistics.time = duration
            self._update_counts(response)
            self._driver.quit()
            self._driver = None
        return response

    def __del__(self):
        if self._driver:
            self._driver.quit()
            self._driver = None

    def _main(self, response: Response):
        """
        This method needs to be implemented by subclasses, as entry point for
        the subclass implementation.

        :param response: The Response object that needs to be updated based on
            the outcome of the operation.
        """
        raise NotImplementedError()

    @staticmethod
    def _update_counts(response: Response):
        """
        Update the counters in categories and statistics of a Response object.

        :param response: The Response object whose counters to update.
        """
        if response.categories:
            for category in (response.categories.alert, response.categories.error):
                if category:
                    if category.items:
                        for i in category.items.values():
                            if i.selectors:
                                i.count += len(i.selectors)
                            if i.xpaths:
                                i.count += len(i.xpaths)
                            category.count += i.count
                    response.statistics.allitemcount += category.count
