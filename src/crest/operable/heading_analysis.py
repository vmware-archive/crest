# Copyright 2020-2021 VMware, Inc.
# SPDX-License-Identifier: MIT
import time
import webbrowser
import requests
import re
import traceback
import logging
from bs4 import BeautifulSoup, Comment
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import NavigableString
from crest.config import *
import pandas as pd
import numpy as np
from lxml import etree
from urllib.request import urlopen
from crest.utils.get_common_function import *
import os
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch
import nltk
os.environ["TOKENIZERS_PARALLELISM"] = "false"

nltk.download('stopwords')
nltk.download('punkt')

class HeadingContent:
    def __init__(self, url, locator= global_args["reporttype"]):
        self.url = to_valid_url(url)
        self.list_of_failed_headings = []
        self.total_headings = 0
        self.stop_words = None
        self.locator = locator
        args = global_args["model_params"]
        if 'tokenizer' not in global_args['model_params'].keys():
            self.roberta_tokenizer = RobertaTokenizer.from_pretrained('gargam/roberta-base-crest')
        else:
            self.roberta_tokenizer = global_args['model_params']['tokenizer']
        
        if 'transfomer_model' not in global_args['model_params'].keys():
            self.model = RobertaForSequenceClassification.from_pretrained('gargam/roberta-base-crest')
        else:
            self.model = global_args['model_params']['transfomer_model']

 
    def declarative_check(self, heading, content):
        tokens = list(
            filter(
                None,
                heading.lower()
                .replace(" & ", " ")
                .replace(" and ", " ")
                .replace(" | ", " ")
                .split(" "),
            )
        )
        if len(tokens) <= 3:
            logging.debug("Declarative check for {} is Passed".format(heading))
            return True
        else:
            logging.debug("Declarative check for {} is Failed".format(heading))
            return False

    def word_matching_check(self, heading, content):
        try:
            if content.strip() == "" or heading.strip() == "":
                return False
            heading_tokens = self.tokenizer(heading)
            content_tokens = self.tokenizer(content)
            logging.debug("heading Tokens: {}".format(heading_tokens))
            logging.debug("Content Tokens: {}".format(content_tokens))
            for heading_token in heading_tokens:
                if heading_token in content_tokens:
                    return True
            return False
        except:
            logging.error("Exception occured in word matching check")
            return False

    def tokenizer(self, sentence):
        if self.stop_words == None:
            self.stop_words = set(stopwords.words("english"))
        ps = PorterStemmer()
        words = word_tokenize(sentence)
        words = [ps.stem(word) for word in words]
        return list(filter(lambda x: x not in self.stop_words, words))

    def get_locator(self, node):
        logging.debug("Inside get locator")
        if self.locator == 3:
            return self.get_xpath(node)
        else:
            return self.get_css_path(node)

    def get_text_below_heading(self, heading):
        if heading is not None:
            heading_text = re.sub(" +", " ", heading.text.replace("\n", " ").strip())
            parent_elem = heading.parent
            prev = None
            cnt = self.get_content(parent_elem)
            while parent_elem is not None and cnt.strip() == heading_text:
                prev = parent_elem
                parent_elem = parent_elem.parent
                if parent_elem is not None:
                    cont = self.get_content(parent_elem)

            heading_sc = heading if prev is None else prev
            if parent_elem is None:
                parent_elem = prev
            content_below_heading = []
            content_headings = []
            flag = False
            for child_node in parent_elem.children:
                tmp = self.get_content(child_node)
                if flag is not True and child_node == heading_sc:
                    flag = True
                elif flag:
                    if isinstance(child_node, NavigableString) is not True:
                        f_heading = re.match(
                            "^h[1-6]$", child_node.name
                        ) or child_node.find(re.compile("^h[1-6]"))
                        if f_heading is None:
                            content_below_heading.append(tmp)
                        else:
                            node = child_node
                            if isinstance(node, NavigableString) is not True:
                                if " ".join(content_below_heading).strip() == "":
                                    if re.match("^h[1-6]", node.name):
                                        content_headings.append(self.get_content(node))
                                    else:
                                        hd = node.find(re.compile("^h[1-6]"))
                                        hd_txt, contxt = self.get_first_heading_context(
                                            hd
                                        )
                                        content_headings.append(hd_txt)
                                        content_below_heading.append(contxt)
                                        if contxt.strip() == "":
                                            break
                                else:
                                    c_h = " ".join(content_headings)
                                    c_b_h = " ".join(content_below_heading)
                                    return c_h + " " + c_b_h
                            else:
                                node_tmp = self.get_content(node)
                                content_below_heading.append(node_tmp)
                    else:
                        content_below_heading.append(self.get_content(child_node))

            c_h = " ".join(content_headings)
            c_b_h = " ".join(content_below_heading)
            return c_h + " " + c_b_h
        return ""

    def get_first_heading_context(self, heading):
        texts = []
        heading_text = re.sub(" +", " ", heading.text.replace("\n", " ").strip())
        parent_elem = heading.parent
        cont = self.get_content(parent_elem)
        prev = None
        while heading_text == cont:
            prev = parent_elem
            parent_elem = parent_elem.parent
            if parent_elem is None:
                parent_elem = prev
                break
            cont = self.get_content(parent_elem)

        heading_sc = heading if prev is None else prev
        for sibling in heading_sc.next_siblings:
            if sibling is None:
                continue
            if isinstance(sibling, NavigableString) is not True:
                if (
                    re.match("^h[1-6]$", sibling.name)
                    or sibling.find(re.compile("^h[1-6]")) is not None
                ):
                    break
            texts.append(self.get_content(sibling))
        return heading_text, re.sub(" +", " ", " ".join(texts)).strip()

    def get_image_video_alt_text(self, element):
        imgs = element.findAll("img")
        videos = element.findAll("video")
        text = []
        if imgs is not None:
            for img in imgs:
                alt_text = img.get("alt")
                if alt_text is not None:
                    text.append(alt_text)
        if videos is not None:
            for video in videos:
                alt_text = video.get("alt")
                if alt_text is not None:
                    text.append(alt_text)
        return " ".join(text)

    def get_content(self, element):
        if element is None:
            return ""
        if isinstance(element, NavigableString):
            return element.encode("utf-8").decode("utf-8").strip()
        else:
            cnt = re.sub(
                " +", " ", element.get_text(" ", strip=True).replace("\n", " ").strip()
            )
            img_video_txt = self.get_image_video_alt_text(element)
            return cnt + " " + img_video_txt

    def entailment_task(self, dataset):
        dataset["heading_text"] = dataset["heading_text"].apply(
            lambda x: str(x).lower().strip()
        )
        dataset["content"] = dataset["content"].apply(lambda x: str(x).lower().strip())
        inputs = self.roberta_tokenizer(dataset[["heading_text", "content"]].values.tolist(), return_tensors="pt", padding=True, truncation=True)
        outputs = self.model(**inputs)
        logits = outputs.logits
        predictions = np.argmax(logits.detach().numpy(), axis=1)
        return dataset[np.array(predictions) == 0]

    def get_heading_elems(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        resp = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        self.remove_comments(soup)
        return soup.find_all(re.compile("^h[1-6]$"))

    def get_xpath(self, element):
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name
                if 1 == len(siblings)
                else "%s[%d]"
                % (child.name, next(i for i, s in enumerate(siblings, 1) if s is child))
            )
            child = parent
        components.reverse()
        return "/%s" % "/".join(components)

    def remove_comments(self, element):
        for element in element.findAll(text=lambda text: isinstance(text, Comment)):
            element.extract()

    def is_webpage_testable(self, xpaths):
        response = urlopen(self.url)
        htmlparser = etree.HTMLParser()
        tree = etree.parse(response, htmlparser)
        for xpath in xpaths:
            if tree.xpath(xpath) is None:
                return False
        return True

    def get_css_path(self, element):
        components = []
        child = element if element.name else element.parent
        while child.parent != None:
            siblings = child.parent.find_all(child.name, recursive=False)
            for i, node in enumerate(siblings, 1):
                if node == child:
                    if i == 1:
                        components.append(child.name)
                    else:
                        components.append("%s:nth-of-type(%d)" % (child.name, i))
                    break
            child = child.parent
        components.reverse()
        return " > ".join(components)

    def main(self):
        self.start_time = time.time()
        response = {}
        response["status"] = {}
        try:
            headings = self.get_heading_elems()
            self.total_headings = len(headings)
            logging.debug(
                "Total Number of headings are {}".format(self.total_headings)
            )
            dataset = []
            dataset_with_null = []
            for i, heading in enumerate(headings):
                content = self.get_text_below_heading(heading)
                heading_text = re.sub(
                    " +", " ", heading.text.replace("\n", " ").strip()
                )
                if heading_text.strip() == "":
                    continue
                elif content.strip() == "":
                    dataset_with_null.append([heading, heading_text, content])
                else:
                    dataset.append([heading, heading_text, content])
            dataset = pd.DataFrame(
                dataset, columns=["heading", "heading_text", "content"]
            )
            dataset_with_null = pd.DataFrame(
                dataset_with_null, columns=["heading", "heading_text", "content"]
            )
            if dataset.shape[0] != 0:
                dataset = self.entailment_task(dataset)
            if dataset_with_null.shape[0] != 0:
                dataset = dataset.append(dataset_with_null, ignore_index=True)
            dataset.drop_duplicates(subset=["heading_text"], inplace=True)
            for heading, heading_text, content in dataset.values:
                if self.word_matching_check(heading_text, content):
                    logging.debug("heading {} has passed.".format(i + 1))
                else:
                    self.list_of_failed_headings.append(self.get_locator(heading))
            success_status = 200
            response["status"]["httpstatuscode"] = success_status
            num_failed_elem = len(self.list_of_failed_headings)
            logging.info(
                "List of Failed headings: {}".format(self.list_of_failed_headings)
            )
            items = {}
            locator_name = "xpaths" if self.locator == 3 else "selectors"
            if num_failed_elem>0:
                items["cr_heading_unrelated"] = {
                    "id":"cr_heading_unrelated",
                    "description": "Possibly unrelated heading",
                    "count": num_failed_elem,
                    "level": "AA",
                    # "wcag": "2.4.6",
                    locator_name: self.list_of_failed_headings,
                }
            response["categories"] = {
                "alert": {
                    "description": "Alerts",
                    "count": num_failed_elem,
                    "items": items,
                }
            }
            time_taken = round(time.time() - self.start_time, 2)
            response["statistics"] = {
                "allitemcount": num_failed_elem,
                "pageurl": self.url,
                "time": time_taken,
                "totalelements": self.total_headings,
            }
            response["status"]["success"] = "True"
            response = remove_category_add_param(response)
            return response, success_status
        except Exception as e:
            logging.error(e)
            response['status']={'success':"False", 'error':"Failed with exception [%s]" % type(e).__name__}
            return response, 400