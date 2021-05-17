# Copyright 2020-2021 VMware, Inc.
# SPDX-License-Identifier: MIT
from flask import Flask
from flask import request
from flask import render_template
import os
import logging
import traceback
import requests
import time
from crest.config import *
from crest.perceivable import keyboard_focus_indicator
from crest.perceivable import cc_transcript
from crest.operable import heading_analysis
from crest.all_in_one.crest_init import AllFuncCheck
from flask_cors import CORS, cross_origin
from crest.utils.startup_util import *

app = Flask(__name__)

cors = CORS(app, resources={"*": {"origins": "*"}})

logging.basicConfig(
    filename=global_args["log_path"],
    level=global_args["log_level"],
    format="%(asctime)s:%(levelname)s:%(message)s",
)


@app.route("/crest/api/all", methods=["POST"])
def run():
    try:
        logging.debug("Inside run")
        data = request.get_json()
        locator = (
            data["reporttype"] if "reporttype" in data else global_args["reporttype"]
        )
        all_func_check = AllFuncCheck(data["url"], locator)
        response, status_code = all_func_check.main()
        return response, status_code
    except Exception as e:
        logging.error(e)
        response={}
        response['status']={'success':"False", 'error':"Failed with exception [%s]" % type(e).__name__}
        return response, 400



@app.route("/crest/api/perceivable/keyboard-focus-indicator", methods=["POST"])
def run_kb():
    try:
        logging.debug("Inside run")
        data = request.get_json()
        locator = (
            data["reporttype"] if "reporttype" in data else global_args["reporttype"]
        )
        indicator = keyboard_focus_indicator.FocusIndicator(data["url"], locator)
        response, status_code  = indicator.main()    
        return response, status_code 
    except Exception as e:
        logging.error(e)
        response={}
        response['status']={'success':"False", 'error':"Failed with exception [%s]" % type(e).__name__}
        return response, 400

 
@app.route("/crest/api/operable/heading-analysis", methods=["POST"])
def run_ha():
    try:
        data = request.get_json()
        logging.debug("Request body data: ", data)
        locator = (
            data["reporttype"] if "reporttype" in data else global_args["reporttype"]
        )
        heading_content = heading_analysis.HeadingContent(data["url"], locator)
        response, status_code = heading_content.main()
        return response, status_code
    except Exception as e:
        logging.error(e)
        response={}
        response['status']={'success':"False", 'error':"Failed with exception [%s]" % type(e).__name__}
        return response, 400


@app.route("/crest/api/perceivable/cc-transcript", methods=["POST"])
def run_av():
    try:
        logging.debug("Inside run")
        data = request.get_json()
        locator = (
            data["reporttype"] if "reporttype" in data else global_args["reporttype"]
        )
        audio_video = cc_transcript.AudioVideo(data["url"], locator)
        response, status_code = audio_video.main()
        return response, status_code
    except Exception as e:
        logging.error(e)
        response={}
        response['status']={'success':"False", 'error':"Failed with exception [%s]" % type(e).__name__}
        return response, 400



@app.route("/crest/testMePage")
def testMePage():
    return render_template("testMePage.html")

crest_init()

if __name__ == "__main__":
    app.run(host=global_args["server-ip"], port=global_args["port"], debug=True)
