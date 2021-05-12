# Copyright 2020-2021 VMware, Inc.
# SPDX-License-Identifier: MIT
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import DesiredCapabilities
from crest.config import *
import webbrowser
import requests
import re
import traceback
import logging
import os
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from crest.utils.get_common_function import *
 

class FocusIndicator:
    def __init__(self, url, locator= global_args["reporttype"]):
        self.image_diff = set()
        self.base_css = {}
        self.focus_missing_elems = []
        self.focus_low_elems = []
        self.total_elems = 0
        self.failed_elems_count = 0
        self.url = to_valid_url(url)
        self.locator = locator
        self.driver = get_driver()
        self.driver.get(self.url)
        self.save_complete_base_css()
        required_width = self.driver.execute_script(
            "return document.body.parentNode.scrollWidth"
        )
        required_height = self.driver.execute_script(
            "return document.body.parentNode.scrollHeight"
        )
        self.driver.set_window_size(required_width, required_height)
        self.focus_event_listener_fn()

    def get_locator(self, element):
        logging.debug("Inside get locator")
        if self.locator == 3:
            return self.xpath_fn(element)
        else:
            return self.css_selector_fn(element)

    def check_website(self):
        try:
            same_elem_count_allowed = 0
            while True:
                actions = ActionChains(self.driver)
                actions = actions.send_keys(Keys.TAB)
                actions.perform()
                active_elem = self.driver.switch_to.active_element
                active_elem_xpath = self.driver.execute_script("return window.absoluteXPath(document.activeElement)")
                if self.total_elems<10 and active_elem is not None:
                    cookie_banner = self.driver.execute_script(
                        'var buttonText = String(arguments[0].outerHTML).toLowerCase(); if (buttonText.indexOf("close")!=-1 || buttonText.indexOf("quit")!=-1 || buttonText.indexOf("accept")!=-1 || buttonText.indexOf("thank")!=-1){arguments[0].click(); return true;} else {return false;};',
                        active_elem,
                    )
                    if cookie_banner:
                        time.sleep(2)
                        self.total_elems = 0
                        self.failed_elems_count = 0
                        same_elem_count_allowed = 0
                        self.focus_low_elems = []
                        self.focus_missing_elems = []
                        self.image_diff = set()
                        continue
                if active_elem in self.image_diff:
                    same_elem_count_allowed += 1
                    if same_elem_count_allowed < 5:
                        logging.debug(
                            "Same element is focused again and count is {}".format(
                                same_elem_count_allowed
                            )
                        )
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        continue
                    else:
                        logging.debug(
                            "Same element is focused again and count is  {}. So, exiting the loop.".format(
                                same_elem_count_allowed
                            )
                        )
                        break
                else:
                    same_elem_count_allowed = 0
                    self.image_diff.add(active_elem)
                new_style_props = self.driver.execute_script("return window.items")
                self.total_elems += 1
                if active_elem_xpath in self.base_css.keys():
                    logging.debug("Active element is present in base_css")
                    base_style_props = self.base_css[active_elem_xpath]
                    fg_color_change = self.is_fg_color_change(
                        base_style_props, new_style_props
                    )
                    bg_color_change = self.is_bg_color_change(
                        base_style_props, new_style_props
                    )
                    is_border_present, border_color_change = self.is_border_change(
                        base_style_props, new_style_props
                    )
                    is_box_present, box_shadow_change = self.check_box_shadow(
                        base_style_props, new_style_props
                    )
                    logging.debug(
                        "{}, {}, {}, {}".format(
                            bg_color_change,
                            fg_color_change,
                            border_color_change,
                            box_shadow_change,
                        )
                    )
                    if (
                        fg_color_change
                        or bg_color_change
                        or border_color_change
                        or box_shadow_change
                    ):
                        pass
                    else:
                        try:
                            if is_border_present or is_box_present:
                                self.focus_low_elems.append(
                                    self.get_locator(active_elem)
                                )
                            else:
                                self.focus_missing_elems.append(
                                    self.get_locator(active_elem)
                                )
                            self.failed_elems_count += 1
                        except:
                            logging.error("Exception occured while updating error list")
                            traceback.print_exc()
                            continue
        except Exception as e:
            traceback.print_exc()

    def check_box_shadow(self, old, new):
        try:
            logging.debug("Inside check box shadow")
            param = "box-shadow"
            text = new[param]
            pattern = "\((.*?)\)"
            if self.is_diff(old, new, [param]) and text is not None and text != "":
                bg_color = new["background-color"]
                bg_tuple, _ = self.extract_color(bg_color, bg_color)
                color_arr = re.findall(pattern, text)
                logging.debug(color_arr)
                if len(color_arr) != 0:
                    for color in color_arr:
                        color_arr = color.split(",")
                        color = [int(i) for i in color_arr[:3]]
                        logging.debug(
                            "Shadow color: {} and Background color: {}".format(
                                color, bg_tuple
                            )
                        )
                        if self.luminosity_ratio_check(color, bg_tuple):
                            return True, True
                    return True, False
            return False, False
        except:
            logging.debug("Exception in check box shadow")
            return False, False

    def is_fg_color_change(self, old, new):
        try:
            logging.debug("Inside is_fg_color_change")
            fg_tag = "text-decoration-color"
            bg_tag = "background-color"
            fg_old, fg_new = self.extract_color(old[fg_tag], new[fg_tag])
            logging.debug("Foreground color: old :{}, new : {}".format(fg_old, fg_new))
            if fg_old != fg_new:
                bg_old, bg_new = self.extract_color(old[bg_tag], new[bg_tag])
                return (
                    self.luminosity_ratio_check(fg_old, fg_new)
                    or self.luminosity_ratio_check(bg_old, fg_new)
                    or self.luminosity_ratio_check(bg_new, fg_new)
                )
            else:
                return False
        except:
            logging.debug("Tag not found")
            return False

    def is_bg_color_change(self, old, new):
        logging.debug("Inside is_bg_color_change")
        try:
            fg_tag = "text-decoration-color"
            bg_tag = "background-color"
            bg_old, bg_new = self.extract_color(old[bg_tag], new[bg_tag])
            logging.debug("Background color: old :{}, new : {}".format(bg_old, bg_new))
            if bg_old != bg_new:
                fg_old, fg_new = self.extract_color(old[fg_tag], new[fg_tag])
                return (
                    self.luminosity_ratio_check(bg_old, bg_new)
                    or self.luminosity_ratio_check(fg_old, bg_new)
                    or self.luminosity_ratio_check(fg_new, bg_new)
                )
            else:
                return False
        except:
            logging.debug("Tag not found")
            return False

    def is_border_change(self, old, new):
        logging.debug("Inside is_border_change")
        bg_tag = "background-color"
        border_status, border_color = self.check_border(old, new)
        logging.debug(
            "After checking border: {} , {}".format(border_status, border_color)
        )
        outline_status, outline_color = self.check_outline(old, new)
        logging.debug(
            "After checking outline: {} , {}".format(outline_status, outline_color)
        )
        if outline_status and border_status:
            color1, color2 = self.extract_color(outline_color, new[bg_tag])
            logging.debug("Outline Color: {}, bg Color: {}".format(color1, color2))
            if self.luminosity_ratio_check(color1, color2) is not True:
                color1, color2 = self.extract_color(border_color, new[bg_tag])
                logging.debug("Border Color: {}, bg Color: {}".format(color1, color2))
                return True, self.luminosity_ratio_check(color1, color2)
            else:
                return True, True
        elif outline_status or border_status:
            color = border_color if border_status else outline_color
            color1, color2 = self.extract_color(color, new[bg_tag])
            logging.debug("Color: {}, bg Color: {}".format(color1, color2))
            return True, self.luminosity_ratio_check(color1, color2)
        return False, False

    def is_color_visible(self, color):
        color = re.search(r"\((.*?)\)", color).group(1).split(",")
        if len(color) == 4 and float(color[3].strip()) == 0.0:
            return False
        else:
            return True

    def check_color(self, elem_css, params):
        logging.debug(elem_css)
        if params[1] in elem_css.keys() and elem_css[params[1]] not in [
            "none",
            "hidden",
        ]:
            width = "".join(filter(str.isdigit, elem_css[params[2]]))
            if (( width is not None and int(width) > 0 ) or elem_css[params[1]]=="dotted") and self.is_color_visible(elem_css[params[0]]):
                if params[0] in elem_css.keys():
                    return True, elem_css[params[0]]
                else:
                    return True, "rgb(0, 0, 0)"
        return False, "rgb(0, 0, 0)"

    def check_outline(self, old_css, elem_css):
        outline_params = ["outline-color", "outline-style", "outline-width"]
        if self.is_diff(old_css, elem_css, outline_params):
            return self.check_color(elem_css, outline_params)
        else:
            return False, "rgb(0, 0, 0)"

    def is_diff(self, old, new, param):
        for item in param:
            if item in old.keys() and item in new.keys():
                logging.debug("{} : {}".format(old[item], new[item]))
                if old[item] != new[item]:
                    return True
        return False

    def check_border(self, old_css, elem_css):
        bottom_border_params = [
            "border-bottom-color",
            "border-bottom-style",
            "border-bottom-width",
        ]
        top_border_params = ["border-top-color", "border-top-style", "border-top-width"]
        left_border_params = [
            "border-left-color",
            "border-left-style",
            "border-left-width",
        ]
        right_border_params = [
            "border-right-color",
            "border-right-style",
            "border-right-width",
        ]
        if (
            self.is_diff(old_css, elem_css, bottom_border_params)
            and self.is_diff(old_css, elem_css, top_border_params)
            and self.is_diff(old_css, elem_css, left_border_params)
            and self.is_diff(old_css, elem_css, right_border_params)
        ):
            if (
                self.check_color(elem_css, bottom_border_params)[0]
                and self.check_color(elem_css, top_border_params)[0]
                and self.check_color(elem_css, right_border_params)[0]
                and self.check_color(elem_css, left_border_params)[0]
            ):
                return self.check_color(elem_css, bottom_border_params)
        return False, "rgb(0, 0, 0)"

    def extract_color(self, color1, color2):
        logging.debug("Inside extract_color")
        color1 = re.search(r"\((.*?)\)", color1).group(1).split(",")
        color2 = re.search(r"\((.*?)\)", color2).group(1).split(",")
        color1 = [int(i) for i in color1[:3]]
        color2 = [int(i) for i in color2[:3]]

        return color1, color2

    def save_complete_base_css(self):
        logging.debug("Inside saveCompletebase_css")
        self.base_css = self.driver.execute_script("""
        function getKeyboardFocusableElements (element = document) { return [...element.querySelectorAll( 'a, button, input, textarea, select, details,[tabindex]:not([tabindex="-1"])' )] .filter(el => !el.hasAttribute('disabled')) }
        window.absoluteXPath = function (element) { var comp, comps = []; var parent = null; var xpath = ''; var getPos = function(element) { var position = 1, curNode; if (element.nodeType == Node.ATTRIBUTE_NODE) { return null; } for (curNode = element.previousSibling; curNode; curNode = curNode.previousSibling){ if (curNode.nodeName == element.nodeName) { ++position; } } return position; }; if (element instanceof Document) { return '/'; } for (; element && !(element instanceof Document); element = element.nodeType == Node.ATTRIBUTE_NODE ? element.ownerElement : element.parentNode) { comp = comps[comps.length] = {}; switch (element.nodeType) { case Node.TEXT_NODE: comp.name = 'text()'; break; case Node.ATTRIBUTE_NODE: comp.name = '@' + element.nodeName; break; case Node.PROCESSING_INSTRUCTION_NODE: comp.name = 'processing-instruction()'; break; case Node.COMMENT_NODE: comp.name = 'comment()'; break; case Node.ELEMENT_NODE: comp.name = element.nodeName; break; } comp.position = getPos(element); } for (var i = comps.length - 1; i >= 0; i--) { comp = comps[i]; xpath += '/' + comp.name.toLowerCase(); if (comp.position !== null) { xpath += '[' + comp.position + ']'; } }return xpath;}
        window.cssPath = function (el) { if (!(el instanceof Element)) return; var path = []; while (el.nodeType === Node.ELEMENT_NODE) { var selector = el.nodeName.toLowerCase(); if (el.id) { selector += "#" + el.id; path.unshift(selector); break; } else { var sib = el, nth = 1; while (sib = sib.previousElementSibling) { if (sib.nodeName.toLowerCase() == selector) nth++; } if (nth != 1) selector += ":nth-of-type("+nth+")"; } path.unshift(selector); el = el.parentNode; } return path.join(" > ");}
        function bgcolor(elem){ var cmpsty = getComputedStyle(elem); var color = cmpsty.getPropertyValue("background-color"); if (color !== "rgba(0, 0, 0, 0)" || elem == document.body) { if(color == "rgba(0, 0, 0, 0)"){return "rgba(255,255,255,0)";}else{return color;}} return bgcolor(elem.parentElement);};
        function getElementCss(element){ var items = {};var compsty = getComputedStyle(element);var len = compsty.length;for (index = 0; index < len; index++){items [compsty[index]] = compsty.getPropertyValue(compsty[index])}; items['background-color']= bgcolor(element); return items;}
        var elements = getKeyboardFocusableElements()
        var output = {}; for(i=0;i<elements.length;i++){output[absoluteXPath(elements[i])] = getElementCss(elements[i]);}
        return output;
        """)

    def save_failed_screenshot(self):
        try:
            self.driver.save_screenshot(global_args["failed_screenshot_path"])
            return True
        except Exception as e:
            traceback.print_exc()
            return False

    def luminosity_ratio_check(self, color1, color2):
        l1 = self.get_luminance(color1)
        l2 = self.get_luminance(color2)
        ratio = (l1 + 0.05) / (l2 + 0.05)
        logging.debug("Counter: {}, Ratio: {}".format(self.total_elems, ratio))
        if ratio <= 1 / 3.0 or ratio >= 3.0:
            return True
        else:
            return False

    def get_luminance(self, color):
        R = 0
        G = 0
        B = 0
        RsRGB = color[0] / 255
        GsRGB = color[1] / 255
        BsRGB = color[2] / 255
        if RsRGB <= 0.03928:
            R = RsRGB / 12.92
        else:
            R = ((RsRGB + 0.055) / 1.055) ** 2.4

        if GsRGB <= 0.03928:
            G = GsRGB / 12.92
        else:
            G = ((GsRGB + 0.055) / 1.055) ** 2.4

        if BsRGB <= 0.03928:
            B = BsRGB / 12.92
        else:
            B = ((BsRGB + 0.055) / 1.055) ** 2.4

        l = 0.2126 * R + 0.7152 * G + 0.0722 * B
        return l

    def css_selector_fn(self, element):
        return self.driver.execute_script('return window.cssPath(arguments[0])', element)
    def focus_event_listener_fn(self):
        self.driver.execute_script(
            'function bgcolor(elem){ var cmpsty = getComputedStyle(elem); var color = cmpsty.getPropertyValue("background-color"); if (color !== "rgba(0, 0, 0, 0)" || elem == document.body) { return color;} return bgcolor(elem.parentElement);}; window.items = {}; function onElementFocused(e){var elem = document.activeElement;var cmpsty = getComputedStyle(elem);for(var i =0;i<cmpsty.length;i++){window.items[cmpsty[i]]=cmpsty.getPropertyValue(cmpsty[i]);} items["background-color"] = bgcolor(elem);} if (document.addEventListener) document.addEventListener("focus", onElementFocused, true);'
        )

    def xpath_fn(self, element):
        return self.driver.execute_script('return window.absoluteXPath(arguments[0])', element)

    def main(self):
        self.start_time = time.time()
        response = {}
        response["status"] = {}
        try:
            self.check_website()
            logging.info(
                "{} : Total Elements : {} : Failed Elements : {}".format(
                    self.url, self.total_elems, self.failed_elems_count
                )
            )
            success_status = 200
            response["status"]["httpstatuscode"] = success_status
            items = {}
            locator_name = "xpaths" if self.locator == 3 else "selectors"
            if len(self.focus_low_elems)>0:
                items["cr_focus_low"] = {
                    "id": "cr_focus_low",
                    "description": "Low contrast on Focus",
                    "count": len(self.focus_low_elems),
                    locator_name: self.focus_low_elems,
                    "level": "AA",
                    # "wcag": "1.4.11",
                }
            
            if len(self.focus_missing_elems)>0:
                items["cr_focus_missing"] = {
                    "id": "cr_focus_missing",
                    "description": "Focus not visible",
                    "count": len(self.focus_missing_elems),
                    locator_name: self.focus_missing_elems,
                    "level": "AA",
                    # "wcag": "2.4.7",
                }
            response["categories"] = {
                "error": {
                    "description": "Errors",
                    "count": self.failed_elems_count,
                    "items": items,
                }
            }
            timetaken = round(time.time() - self.start_time, 2)
            response["statistics"] = {
                "pageurl": self.url,
                "time": timetaken,
                "totalelements": self.total_elems,
            }
            response["status"]["success"] = "True"
            response = remove_category_add_param(response)
            return response, success_status
        except Exception as e:
            logging.error(e)
            response['status']={'success':"False", 'error':"Failed with exception [%s]" % type(e).__name__}
            return response, 400
        finally:
            self.driver.quit()

