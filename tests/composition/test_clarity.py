#!/usr/bin/env python3
"""
Functional tests for the Clarity composition checks.
"""
# Copyright 2023 VMware, Inc.
# SPDX-License-Identifier: MIT

import dataclasses
import itertools
from typing import List, Sequence, Tuple
import tempfile
import unittest

import ddt

from crest.utils import operation
from crest.composition import clarity


@dataclasses.dataclass
class CaseItem:
    """
    Expected Item in the response from the Clarity composition checks.
    """

    inner_component: str
    outer_component: str
    selectors: List[str]
    xpaths: List[str]


@dataclasses.dataclass
class CaseData:
    """
    Expected information in the response from the Clarity composition checks.
    """

    page_html: str
    error_count: int
    allitemcount: int
    totalelements: int
    items: Sequence[CaseItem]
    __name__: str
    locator: operation.Locator = operation.Locator.UNSPECIFIED


def _set_locator(args: Tuple[CaseData, operation.Locator]):
    """
    Set the locator field in a CaseData object and compute an appropriate test
    name suffix.
    """
    case_data, locator = args
    case_data.locator = locator
    case_data.__name__ = f"{case_data.__name__}_{locator.name.lower()}"
    return case_data


@ddt.ddt
class TestClarityComposition(unittest.TestCase):
    """
    Test case for ClarityComposition functional tests.
    """

    @ddt.idata(
        map(
            _set_locator,
            itertools.product(
                (
                    CaseData(
                        __name__="alert_in_alert",
                        page_html="""
<html>
<body>
<div class="alert">
    <div class="alert">Violating</div>
</div>
</body>
</html>""",
                        error_count=1,
                        allitemcount=1,
                        totalelements=2,
                        items=(
                            CaseItem(
                                inner_component="alert",
                                outer_component="alert",
                                selectors=["html > body > div > div"],
                                xpaths=["/html[1]/body[1]/div[1]/div[1]"],
                            ),
                        ),
                    ),
                    CaseData(
                        __name__="multiple_alerts_in_alert",
                        page_html="""
<html>
<body>
<div class="alert">
    <div></div>
    <p></p>
    <div class="alert">Violating 1</div>
</div>
<div class="alert">
    <div class="alert">Violating 2</div>
    <div class="alert">Violating 3</div>
</div>
</body>
</html>""",
                        error_count=3,
                        allitemcount=3,
                        totalelements=5,
                        items=(
                            CaseItem(
                                inner_component="alert",
                                outer_component="alert",
                                selectors=[
                                    "html > body > div > div:nth-of-type(2)",
                                    "html > body > div:nth-of-type(2) > div",
                                    "html > body > div:nth-of-type(2) > div:nth-of-type(2)",
                                ],
                                xpaths=[
                                    "/html[1]/body[1]/div[1]/div[2]",
                                    "/html[1]/body[1]/div[2]/div[1]",
                                    "/html[1]/body[1]/div[2]/div[2]",
                                ],
                            ),
                        ),
                    ),
                    CaseData(
                        __name__="multiple_component_types",
                        page_html="""
<html>
<body>
<clr-accordion>
    <div class="alert">Allowed</div>
</clr-accordion>
<div class="alert">
    <clr-accordion>Violating 1</clr-accordion>
</div>
<span class="badge">
    <button class=btn>Violating 2</button>
</span>
</body>
</html>""",
                        error_count=2,
                        allitemcount=2,
                        totalelements=6,
                        items=(
                            CaseItem(
                                inner_component="accordion",
                                outer_component="alert",
                                selectors=["html > body > div > clr-accordion"],
                                xpaths=["/html[1]/body[1]/div[1]/clr-accordion[1]"],
                            ),
                            CaseItem(
                                inner_component="button",
                                outer_component="badge",
                                selectors=["html > body > span > button"],
                                xpaths=["/html[1]/body[1]/span[1]/button[1]"],
                            ),
                        ),
                    ),
                    CaseData(
                        __name__="attribute_css_selectors",
                        page_html="""
<html>
<body>
<a class="tooltip">
    <clr-radio-wrapper>
            <input type="radio"></input>
    </clr-radio-wrapper>
</a>
<clr-combobox>
    <input clrPassword>
</clr-combobox>
</body>
</html>""",
                        error_count=2,
                        allitemcount=2,
                        totalelements=4,
                        items=(
                            CaseItem(
                                inner_component="radio button",
                                outer_component="tooltip",
                                selectors=[
                                    "html > body > a > clr-radio-wrapper > input"
                                ],
                                xpaths=[
                                    "/html[1]/body[1]/a[1]/clr-radio-wrapper[1]/input[1]"
                                ],
                            ),
                            CaseItem(
                                inner_component="password",
                                outer_component="combo box",
                                selectors=["html > body > clr-combobox > input"],
                                xpaths=["/html[1]/body[1]/clr-combobox[1]/input[1]"],
                            ),
                        ),
                    ),
                ),
                (operation.Locator.XPATH, operation.Locator.CSS_SELECTOR),
            ),
        )
    )
    def test_composition(self, data: CaseData):
        """
        Test disallowed composition of Clarity components.
        """
        with tempfile.NamedTemporaryFile(mode="wt", suffix=".html") as page:
            page.write(data.page_html)
            page.flush()

            url = f"file://{page.name}"
            clarity_composition = clarity.ClarityComposition(url, data.locator.value)
            result = clarity_composition.main()

            self.assertTrue(result.status.success)
            self.assertEqual(result.status.httpstatuscode, 200)
            self.assertIsNone(result.status.error)
            self.assertIsNone(result.categories.alert)
            self.assertEqual(result.categories.error.count, data.error_count)
            self.assertEqual(result.categories.error.description, "Errors")
            for item_data in data.items:
                inner_component_name = item_data.inner_component.replace(" ", "_")
                outer_component_name = item_data.outer_component.replace(" ", "_")
                item_id = f"cc_{inner_component_name}_in_{outer_component_name}"
                self.assertIn(item_id, result.categories.error.items)
                item = result.categories.error.items[item_id]
                self.assertEqual(item.id, item_id)
                self.assertEqual(
                    item.description,
                    f"Found `{item_data.inner_component}` element contained inside a "
                    f"`{item_data.outer_component}` element, which is not allowed",
                )
                if data.locator == operation.Locator.XPATH:
                    self.assertEqual(item.xpaths, item_data.xpaths)
                    self.assertEqual(item.count, len(item_data.xpaths))
                    self.assertFalse(item.selectors)
                else:
                    self.assertEqual(item.selectors, item_data.selectors)
                    self.assertEqual(item.count, len(item_data.selectors))
                    self.assertFalse(item.xpaths)
            self.assertEqual(len(result.categories.error.items), len(data.items))
            self.assertEqual(result.statistics.pageurl, url)
            self.assertEqual(result.statistics.allitemcount, data.allitemcount)
            self.assertEqual(result.statistics.totalelements, data.totalelements)


if __name__ == "__main__":
    unittest.main()
