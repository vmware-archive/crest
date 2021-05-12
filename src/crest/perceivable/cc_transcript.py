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
from urllib.parse import urlsplit
from crest.config import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.common.by import By
from PIL import Image
from pytesseract import image_to_string
from io import BytesIO
from difflib import SequenceMatcher
from crest.utils.get_common_function import *

class AudioVideo:
    def __init__(self, url, locator= global_args["reporttype"]):
        self.list_of_video_elems = set()
        self.list_of_cc_elems = set()
        self.list_of_audio_elems = set()
        self.list_of_transcript_elems = set()
        self.url = to_valid_url(url)
        self.locator = locator
        self.driver = get_driver()
        self.driver.get(self.url)
    
    
    def check_webpage(self, iframe_status, iframe_elem=None):
        vStatus, vElements = self.check_video_player( iframe_status, iframe_elem)
        logging.debug(
            ("Number of videos found : {}").format(len(self.list_of_video_elems))
        )
        if vStatus:
            self.check_cc(self.driver, vElements, iframe_status, iframe_elem)

        aStatus, aElements = self.check_audio_player(self.driver, iframe_status, iframe_elem)
        logging.debug(
            ("Number of audios found : {}").format(len(self.list_of_audio_elems))
        )
        if aStatus:
            self.check_transcript(self.driver, iframe_status, iframe_elem)

    def check_audio_player(self, driver, iframe_status, iframe_elem):
        logging.debug("check audio player")
        try:
            elements = driver.find_elements_by_xpath("//audio")
            if elements is None or len(elements) == 0:
                return False, None
            vElem = []

            for element in elements:
                if self.is_advertisement(driver, element) is not True:
                    self.list_of_audio_elems.add(element)
                    vElem.append(element)
            if len(vElem) != 0:
                return True, vElem
            else:
                return False, None
        except:
            logging.error("Exception in finding audio player")
            traceback.print_exc()
            logging.debug("Audio Player does not exist.")
            return False, None

    def check_transcript(self, driver, iframe_status, iframe_elem):
        clickable_elems = []
        try:
            clickable_elems = driver.execute_script(
                'var allElements = document.getElementsByTagName("*"); var elemsList=[]; for ( var i = 0; i<allElements.length; i++ ) { var elem = allElements[i]; var compsty = getComputedStyle(elem); if(window.isVisible(elem) && (compsty.getPropertyValue("cursor")=="pointer" || elem.nodeName=="BUTTON")) { var buttonText= String(elem.cloneNode(false).outerHTML).toLowerCase(); if (buttonText.indexOf("transcript")!=-1){elemsList.push(elem);}}}; return elemsList;'
            )
        except:
            logging.debug("Exception occur in get_all_button_tags")
        if clickable_elems is None or len(clickable_elems) == 0:
            elem = self.check_siblings_content(driver)
            if elem is not None:
                self.list_of_transcript_elems.add(elem)
        else:
            self.list_of_transcript_elems.update(clickable_elems)
            logging.debug(
                "Transcript elements count reached to : {}".format(
                    len(self.list_of_transcript_elems)
                )
            )

    def check_siblings_content(self, driver):
        elem = driver.execute_script(
            'var allElements = document.getElementsByTagName("*"); for ( var i = 0; i<allElements.length; i++ ) { var elem = allElements[i]; var compsty = getComputedStyle(elem); if(window.isVisible(elem) && compsty.getPropertyValue("cursor")!="pointer") { var elementText= String(elem.cloneNode(false).outerHTML).toLowerCase(); if (elementText.indexOf("transcript")!=-1 && elem.parentNode.textContent.length > 100){return elem;}}}; return null;'
        )
        return elem

    def check_video_player(self, iframe_status, iframe_elem):
        logging.debug("check video player")
        try:
            elements = self.driver.find_elements_by_xpath("//video")
            if elements is None or len(elements) == 0:
                return False, None
            else:
                vElem = []
                for element in elements:
                    is_visible = self.driver.execute_script(
                        "if(window.isVisible(arguments[0])){return true;}; return false;",
                        element,
                    )
                    if (
                        self.is_advertisement(self.driver, element) is not True
                        and is_visible
                    ):
                        self.list_of_video_elems.add(element)
                        vElem.append(element)
                if len(vElem) != 0:
                    return True, vElem
                else:
                    return False, None
        except:
            traceback.print_exc()
            logging.debug("Video Player does not exist.")
            return False, None

    def get_ads_domain_names(self):
        domain_names = set()
        with open(global_args["domain_file_path"], "r") as f:
            domain_names.add(f.readline())
        return domain_names

    def is_advertisement(self, driver, element):
        logging.debug("Checking whether the element is an ad. or not")
        try:
            src = element.get_attribute("src")
            if src is not None and src != "":
                url_prop = urlsplit(src)
                hostname = url_prop.hostname
                if hostname is not None and hostname in self.domain_names:
                    driver.execute_script('arguments[0].style.display="none"', element)
                    logging.debug("It is a ad.")
                    return True
            is_ad = driver.execute_script(
                'var cont = arguments[0].outerHTML.toLowerCase(); return cont.indexOf("advertisement")!=-1 || /[^A-Za-z]ad[s]{0,1}[^A-Za-z]/.test(cont)',
                element,
            )
            if is_ad:
                driver.execute_script('arguments[0].style.display="none"', element)
                logging.debug("It is an ad.")
                return True
            logging.debug("It's not an ad.")
            return False
        except:
            logging.debug(
                "Exception occured while checking element whether its a ad. or not."
            )
            logging.debug("It's not ad.")
            return False

    def get_all_frames(self, driver):
        iframes_without_ads = []
        try:
            iframes = driver.find_elements_by_xpath("//iframe")
            for iframe in iframes:
                if self.is_advertisement(driver, iframe) is not True:
                    is_visible = driver.execute_script(
                        "if(window.isVisible(arguments[0])){return true;}; return false;",
                        iframe,
                    )
                    if is_visible:
                        iframes_without_ads.append(iframe)
        except:
            logging.debug(
                "Exception occured while checking iframe whether its a adver. or not."
            )
        return iframes_without_ads

    def check_cc(self, driver, elements, iframe_status, iframe_elem):
        logging.debug("Checking Closed Captioning")
        for element in elements:
            try:
                try:
                    button = WebDriverWait(driver, 5).until(
                        cond.element_to_be_clickable(
                            (By.XPATH, '//button[@aria-label="Play"]')
                        )
                    )
                    if button is not None:
                        button.click()
                        if self.check_inbuilt_captions(driver, element):
                            self.list_of_cc_elems.add(element)
                            return
                    else:
                        driver.execute_script("arguments[0].play();", element)
                except:
                    logging.debug("Exception occured while clicking on the video")

                self.get_all_button_tags(driver, iframe_status, iframe_elem)
                tracks = element.find_element_by_tag_name("track")
                if tracks is not None and (
                    tracks.get_attribute("kind") == "subtitles"
                    or tracks.get_attribute("kind") == "captions"
                ):
                    self.list_of_cc_elems.add(element)
            except:
                logging.debug("There is no track element found")

    def check_inbuilt_captions(self, driver, element):
        first_text = ""
        time_count = 0
        while first_text == "" and time_count < 5:
            first_text = image_to_string(
                self.get_element_screenshot(driver, element), lang="eng"
            )
            first_text = re.sub(" +", " ", first_text.replace("\n", " ")).strip()
            if len(first_text.split(" ")) < 3:
                first_text = ""
            time.sleep(1)
            time_count += 1

        logging.debug("First Text: " + first_text)
        if first_text == "":
            return False

        time_count = 0
        ratio = 1
        comp_text = ""
        while (ratio > 0.5 or comp_text == "") and time_count < 5:
            comp_text = image_to_string(
                self.get_element_screenshot(driver, element), lang="eng"
            )
            comp_text = re.sub(" +", " ", comp_text.replace("\n", " ")).strip()
            ratio = SequenceMatcher(None, first_text, comp_text).ratio()
            time.sleep(1)
            time_count += 1
            logging.debug("Comp Text: " + comp_text)
            logging.debug("Ratio: " + ratio)

        if ratio < 0.5 and comp_text != "":
            return True
        else:
            return False

    def get_element_screenshot(self, driver, element):
        location = element.location
        size = element.size
        png = driver.get_screenshot_as_png()

        im = Image.open(BytesIO(png))

        left = location["x"]
        top = location["y"]
        right = location["x"] + size["width"]
        bottom = location["y"] + size["height"]

        im = im.crop((left, top, right, bottom))
        return im

    def get_all_button_tags(self, driver, iframe_status, iframe_elem):
        logging.debug("Checking all the clickable tags")
        clickable_elems = []
        try:
            clickable_elems = driver.execute_script(
                'var allElements = document.getElementsByTagName("*"); var elemsList=[]; for ( var i = 0; i<allElements.length; i++ ) { var elem = allElements[i]; var compsty = getComputedStyle(elem); if(window.isVisible(elem) && (compsty.getPropertyValue("cursor")=="pointer" || elem.nodeName=="BUTTON")) { var buttonText= String(elem.cloneNode(false).outerHTML).toLowerCase(); if (buttonText.indexOf("caption")!=-1  || buttonText.indexOf("subtitle")!=-1){elemsList.push(elem);}}}; return elemsList;'
            )
        except:
            logging.debug("Exception occur in get_all_button_tags")
        self.list_of_cc_elems.update(clickable_elems)
        logging.debug(
            "cc elements count reached to : {}".format(len(self.list_of_cc_elems))
        )

    def get_xpath(self, driver, element):
        path = driver.execute_script("return absoluteXPath(arguments[0]);", element)
        return path

    def absolute_xpath_fn(self):
        return self.driver.execute_script(
            "function absoluteXPath(element) {"
            + "var comp, comps = [];"
            + "var parent = null;"
            + "var xpath = '';"
            + "var getPos = function(element) {"
            + "var position = 1, curNode;"
            + "if (element.nodeType == Node.ATTRIBUTE_NODE) {"
            + "return null;"
            + "}"
            + "for (curNode = element.previousSibling; curNode; curNode = curNode.previousSibling){"
            + "if (curNode.nodeName == element.nodeName) {"
            + "++position;"
            + "}"
            + "}"
            + "return position;"
            + "};"
            + "if (element instanceof Document) {"
            + "return '/';"
            + "}"
            + "for (; element && !(element instanceof Document); element = element.nodeType == Node.ATTRIBUTE_NODE ? element.ownerElement : element.parentNode) {"
            + "comp = comps[comps.length] = {};"
            + "switch (element.nodeType) {"
            + "case Node.TEXT_NODE:"
            + "comp.name = 'text()';"
            + "break;"
            + "case Node.ATTRIBUTE_NODE:"
            + "comp.name = '@' + element.nodeName;"
            + "break;"
            + "case Node.PROCESSING_INSTRUCTION_NODE:"
            + "comp.name = 'processing-instruction()';"
            + "break;"
            + "case Node.COMMENT_NODE:"
            + "comp.name = 'comment()';"
            + "break;"
            + "case Node.ELEMENT_NODE:"
            + "comp.name = element.nodeName;"
            + "break;"
            + "}"
            + "comp.position = getPos(element);"
            + "}"
            + "for (var i = comps.length - 1; i >= 0; i--) {"
            + "comp = comps[i];"
            + "xpath += '/' + comp.name.toLowerCase();"
            + "if (comp.position !== null) {"
            + "xpath += '[' + comp.position + ']';"
            + "}"
            + "}"
            + "return xpath;"
            + "}"
        )

    def init_script(self):
        self.domain_names = self.get_ads_domain_names()
        self.driver.execute_script(
            "window.isVisible = function(elem) {"
            + "if (!(elem instanceof Element)) return false;"
            + "const style = getComputedStyle(elem);"
            + 'if (style.display === "none") return false;'
            + 'if (style.visibility !== "visible") return false;'
            + "if (style.opacity < 0.1) return false;"
            + "return true;"
            + "}"
        )
        self.absolute_xpath_fn()

    def hide_elem(self, driver, elem):
        try:
            driver.execute_script('arguments[0].style.display="none"', elem)
        except:
            logging.debug("Element can't be hidden.")

    def main(self):
        self.start_time = time.time()
        response = {}
        response["status"] = {}
        try:
            self.init_script()
            self.check_webpage(False)
            success_status = 200
            if self.driver is not None:
                logging.debug("Object Successfully created")
                logging.debug("Getting all the iframe present on the web page")
                iframes = self.get_all_frames(self.driver)
                logging.debug(
                    "Number of iframes present on the web page : {}".format(
                        len(iframes)
                    )
                )
                i = 0
                logging.debug("Checking iframes one by one")
                while i < len(iframes):
                    try:
                        logging.debug("Checking iframe: {}".format(i + 1))
                        self.driver.switch_to.frame(iframes[i])
                        self.init_script()
                        self.check_webpage(True, iframes[i])
                        self.driver.switch_to.default_content()
                        self.hide_elem(self.driver, iframes[i])
                    except:
                        logging.debug("No such Frame exist.")
                        self.driver.switch_to.default_content()
                    i += 1

                logging.info(
                    "Total number of videos: {}".format(len(self.list_of_video_elems))
                )
                end = time.time()
                logging.info(
                    "Total number of videos that {} contains: {}".format(
                        self.url, len(self.list_of_video_elems)
                    )
                )
                logging.info(
                    "Total number of closed captioning buttons that {} contains: {}".format(
                        self.url, len(self.list_of_cc_elems)
                    )
                )
                vCount = len(self.list_of_video_elems)
                ccCount = len(self.list_of_cc_elems)
                aCount = len(self.list_of_audio_elems)
                transcript_count = len(self.list_of_transcript_elems)
                response["status"]["httpstatuscode"] = success_status
                items = {}
                captions_missing_count = max(vCount - ccCount, 0)
                transcript_missing_count = max(aCount - transcript_count, 0)
                if captions_missing_count>0:
                    items["cr_captions_missing"] = {
                        "id":"cr_captions_missing",
                        "description": "Captions missing",
                        "count": captions_missing_count,
                        "level": "A",
                        # "wcag": "1.2.2",
                    }
                if transcript_missing_count > 0:
                    items["cr_transcript_missing"] = {
                        "id":"cr_transcript_missing",
                        "description": "Podcast transcript missing",
                        "count": transcript_missing_count,
                        "level": "A",
                        # "wcag": "1.2.1",
                    }

                response["categories"] = {
                    "error": {
                        "description": "Errors",
                        "count": max(aCount - transcript_count, 0)
                        + max(vCount - ccCount, 0),
                        "items": items,
                    }
                }
                time_taken = round(time.time() - self.start_time, 2)
                response["statistics"] = {
                    "pageurl": self.url,
                    "time": time_taken,
                    "totalvideos": vCount,
                    "totalaudios": aCount,
                    "totalelements": aCount+vCount,
                }
                response["status"]["success"] = "True"
                response = remove_category_add_param(response)
                return response, success_status
            else:
                return response, success_status
        except Exception as e:
            logging.error(e)
            response['status']={'success':"False", 'error':"Failed with exception [%s]" % type(e).__name__}
            return response, 400
        finally:
            self.driver.quit()
