#!/usr/bin/env python3
"""
Functional tests for perceivable keyboard focus indicator checks.
"""
# Copyright 2023 VMware, Inc.
# SPDX-License-Identifier: MIT


import os.path
import unittest


from crest.perceivable import keyboard_focus_indicator


class TestFocusIndicator(unittest.TestCase):
    """
    Functional tests for the FocusIndicator class.
    """

    def test_test_me_page(self):
        """
        Test that expected errors are generated when analyzing testMePage.html.
        """
        test_page_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "src",
                "crest",
                "templates",
                "testMePage.html",
            )
        )
        url = f"file://{test_page_path}"
        focus_indicator = keyboard_focus_indicator.FocusIndicator(url)
        result, statuscode = focus_indicator.main()
        self.assertEqual(statuscode, 200)
        self.assertEqual(result["status"], {"success": "True", "httpstatuscode": 200})
        self.assertEqual(
            result["categories"],
            {
                "error": {
                    "description": "Errors",
                    "count": 2,
                    "items": {
                        "cr_focus_low": {
                            "id": "cr_focus_low",
                            "description": "Low contrast on Focus",
                            "count": 1,
                            "xpaths": [
                                "/html[1]/body[1]/section[2]/div[1]/div[1]/div[1]/div[1]/div[1]/"
                                "ul[2]/li[2]/a[1]"
                            ],
                            "level": "AA",
                        },
                        "cr_focus_missing": {
                            "id": "cr_focus_missing",
                            "description": "Focus not visible",
                            "count": 1,
                            "xpaths": [
                                "/html[1]/body[1]/section[2]/div[1]/div[1]/div[1]/div[1]/div[1]/"
                                "ul[2]/li[1]/a[1]"
                            ],
                            "level": "AA",
                        },
                    },
                }
            },
        )
        self.assertIn("time", result["statistics"])
        del result["statistics"]["time"]
        self.assertIn("totalelements", result["statistics"])
        del result["statistics"]["totalelements"]
        self.assertEqual(
            result["statistics"],
            {
                "pageurl": url,
                "allitemcount": 2,
            },
        )


if __name__ == "__main__":
    unittest.main()
