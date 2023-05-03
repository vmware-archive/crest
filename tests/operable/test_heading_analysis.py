#!/usr/bin/env python3
"""
Functional tests for operable heading analysis checks.
"""
# Copyright 2023 VMware, Inc.
# SPDX-License-Identifier: MIT


import os.path
import unittest


from crest.operable import heading_analysis


class TestHeadingContent(unittest.TestCase):
    """
    Functional tests for the HeadingContent class.
    """

    def test_test_me_page(self):
        """
        Test that expected alerts are generated when analyzing testMePage.html.
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
        heading_content = heading_analysis.HeadingContent(url)
        result, statuscode = heading_content.main()
        self.assertEqual(statuscode, 200)
        self.assertEqual(result["status"], {"success": "True", "httpstatuscode": 200})
        self.assertEqual(
            result["categories"],
            {
                "alert": {
                    "description": "Alerts",
                    "count": 3,
                    "items": {
                        "cr_heading_unrelated": {
                            "id": "cr_heading_unrelated",
                            "description": "Possibly unrelated heading",
                            "count": 3,
                            "level": "AA",
                            "xpaths": [
                                "/html/body/section[4]/div/div/div/div/div/ul[2]/li[2]/h4",
                                "/html/body/section[4]/div/div/div/div/div/ul[2]/li[1]/h4",
                                "/html/body/section[4]/div/div/div/div/div/ul[2]/li[3]/div[1]/h4",
                            ],
                        }
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
                "allitemcount": 3,
                "pageurl": url,
            },
        )


if __name__ == "__main__":
    unittest.main()
