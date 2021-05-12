# Copyright 2020-2021 VMware, Inc.
# SPDX-License-Identifier: MIT
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import webbrowser
import requests
import re
import traceback
import logging
from crest.perceivable.keyboard_focus_indicator import FocusIndicator
from crest.perceivable.cc_transcript import AudioVideo
from crest.operable.heading_analysis import HeadingContent
from multiprocessing import Process
from crest.config import *
from crest.utils.get_common_function import *
from threading import *

class AllFuncCheck:
    def __init__(self, url, locator= global_args["reporttype"]):
        self.url = to_valid_url(url)
        self.locator = locator

    def main(self):
        try:
            self.start_time = time.time()
            fi = FocusIndicator(self.url, self.locator)
            hc = HeadingContent(self.url, self.locator)
            av = AudioVideo(self.url, self.locator)
            
            responses = {}
            kfi_thread = Thread(
                target=lambda responses, arg: responses.update({"kfi": fi.main()}),
                args=(responses, ""),
            )
            ht_thread = Thread(
                target=lambda responses, arg: responses.update({"ht": hc.main()}),
                args=(responses, ""),
            )
            ct_thread = Thread(
                target=lambda responses, arg: responses.update({"ct": av.main()}),
                args=(responses, ""),
            )
            kfi_thread.start()
            ht_thread.start()
            ct_thread.start()
            kfi_thread.join()
            ht_thread.join()
            ct_thread.join()

            categories_error_count =0
            categories_error_items ={}
            categories_alert_count =0
            categories_alert_items ={}
            all_item_count =0
            total_elements =0
            total_videos =0
            total_audios =0
            for response, _ in responses.values():
                all_item_count += response['statistics']['allitemcount']
                total_elements += response['statistics']['totalelements']
                if 'totalvideos' in response['statistics'].keys():
                    total_videos += response['statistics']['totalvideos']
                
                if 'totalaudios' in response['statistics'].keys():
                    total_audios += response['statistics']['totalaudios']
                
                if 'error' in response['categories'].keys():
                    categories_error_count += response['categories']['error']['count']
                    categories_error_items.update(response['categories']['error']['items'])
                
                if 'alert' in response['categories'].keys():
                    categories_alert_count += response['categories']['alert']['count']
                    categories_alert_items.update(response['categories']['alert']['items'])
            
            output = {}
            output["categories"] = {}
            success_status = 200
            if categories_error_count !=0:
                output["categories"]["error"]={"count": categories_error_count, "description": "Errors", "items": categories_error_items}
            if categories_alert_count !=0:
                output["categories"]["alert"]={"count": categories_alert_count, "description": "Alerts", "items": categories_alert_items}
            output["statistics"] = {'allitemcount': all_item_count, 'totalvideos': total_videos, 'totalaudios': total_audios, 'pageurl': self.url, 'time': round(time.time() - self.start_time, 2), 'totalelements': total_elements}
            output["status"] = {'httpstatuscode': success_status, 'success': 'True'}
            return output, success_status
        except Exception as e:
            logging.error(e)
            response={}
            response['status']={'success':"False", 'error':"Failed with exception [%s]" % type(e).__name__}
            return response, 400 