#!/usr/bin/env python3
"""
Functional tests for perceivable closed caption transcripts checks.
"""
# Copyright 2023 VMware, Inc.
# SPDX-License-Identifier: MIT


import os.path
import unittest


from crest.perceivable import cc_transcript


class TestAudioVideo(unittest.TestCase):
    """
    Functional tests for the AudioVideo class.
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
        audio_video = cc_transcript.AudioVideo(url)
        result, statuscode = audio_video.main()
        self.assertEqual(statuscode, 200)
        self.assertEqual(result["status"], {"success": "True", "httpstatuscode": 200})
        self.assertEqual(
            result["categories"],
            {
                "error": {
                    "description": "Errors",
                    "count": 3,
                    "items": {
                        "cr_captions_missing": {
                            "id": "cr_captions_missing",
                            "description": "Captions missing",
                            "count": 2,
                            "level": "A",
                        },
                        "cr_transcript_missing": {
                            "id": "cr_transcript_missing",
                            "description": "Podcast transcript missing",
                            "count": 1,
                            "level": "A",
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
                "totalvideos": 3,
                "totalaudios": 2,
                "allitemcount": 3,
            },
        )


if __name__ == "__main__":
    unittest.main()
