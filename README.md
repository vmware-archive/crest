<!-- Copyright 2020-2021 VMware, Inc.
SPDX-License-Identifier: MIT -->

<p>
    <br>
    <img src="https://raw.githubusercontent.com/vmware/crest/main/src/crest/static/crest_logo.png?token=ATSPAQYQYG3FH2TQ5USHXLDAUSSQW" />
    <br>
<p>

# Automated Accessibility Testing Tool


**Crest** quickly tests any HTML web page for a simple way to solve your accessibility testing problems. Provide a website URL to our callable API and expose potential WCAG violations. 

Currently supports:
- Keyboard Focus Indicator
- Closed Captioning and Transcript
- Heading Analysis

## Table of contents


<!-- - [Setup](#setup)
    - [Using Pip](#using-pip)
    - [Using Conda](#using-conda)
    - [Using Docker](#using-docker)
- [Usage](#usage)
- [Understanding Results](#understanding-results)
    - [Keyboard Focus Indicator](#keyboard-focus-indicator)
    - [Closed Captioning and Transcript Check](#closed-captioning-and-transcript-check)
    - [Heading Analysis](#heading-analysis)
- [TestMePage](#testmepage)
- [Fine-tune Machine Learning Model](#fine-tune-machine-learning-model)
- [Default Settings](#default-settings) -->

- [Getting Started](#getting-started)
- [Fine-tune Machine Learning Model](#fine-tune-machine-learning-model)
- [Support](#support)
- [Contributors](#contributors)
- [Contributing](#contributing)
- [License](#license)



### Getting Started

<!-- Getting started with Crest in 5 minutes by following the instructions provided on the <a alt="Link to getting started page of API reference documentation" href="">API reference page</a>. -->

To get you started quickly let’s dive into the necessary steps needed to set up the environment.

#### To use Crest as a Python Library

##### Using Pip

1. Install Crest using python package manager (Make sure pip is installed in your system).

```python 
pip install crest
```

#### To use Crest as a Service

##### Using Conda

1. Download and Install Miniconda from [conda.io](https://docs.conda.io/en/latest/miniconda.html)

2. For Windows, launch Miniconda prompt shell. For MacOS, launch the terminal.

3. Clone the Crest repository. More details can be found at [docs.github.com](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/cloning-a-repository)

4. Go to "crest" folder in your terminal/prompt shell. Run command.
```python
conda env create -f environment.yml
conda activate crest
```

5. Install chromedriver. The details can be found in [chromium.org](https://chromedriver.chromium.org/downloads).

6. Download and Install google-chrome-stable from [ubuntuupdates.org](https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable).

7. Once all the required libraries are installed, go to 'src/crest' folder and run the below command in your terminal/prompt shell. 
```python
FLASK_APP=server.py FLASK_ENV=development flask run --port 3000
```

##### Using Docker

1. Clone the repository. More details can be found at [docs.github.com](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

2. Download and Install docker from [docker.com](https://docs.docker.com/get-docker/). Note: Make sure your docker server as well as crest image is running.

3. Go to "crest" folder in your terminal/prompt shell. Run command.
```python
docker build -t crest .
```

4. Once the docker image is created, run it by executing the following command.
```python
docker container run --name crest_container -p 3000:3000 crest 
```

**Note: A machine learning model will be downloaded from [huggingface.co](https://huggingface.co/gargam/roberta-base-crest) when you use the Heading Analysis/ Crest Single API for the first time. It will be saved in your system's cache for future use and could take approximately 2 GB of your system's memory.**


### Fine-tune Machine Learning Model

Train the machine learning model to a specific domain:

1. Prepare a labelled dataset in the below format.

| URL           | Title                              | Description                                                                    | Result |
|---------------|------------------------------------|--------------------------------------------------------------------------------|--------|
| http://gov.uk | Tell us whether you accept cookies | We use cookies to collect information about how you use GOV.UK. We use this... | True   |
2. Change the dataset directory path i.e. ['model_params']['training_data_input_file_name'] in the config.py file.
3. Run a python script placed in the `src/crest/utils/` directory by executing the following command:
```python
    python train_model.py
```

Note: Install Apex if you are using fp16 training. Please follow the instructions in  [github.com/NVIDIA/apex](https://github.com/NVIDIA/apex). (Installing Apex from pip has caused issues for several people.)

### Support

Crest is released as open source software and comes with no commercial support.<br />
But since we want to ensure success and recognize that Crest consumers might fall into a range of roles - from developers that are steeped in the conventions of open-source to customers that are more accustomed to commercial offerings, we offer several methods of engaging with the Crest team and community.<br />
For the Crest community, feel free to join our <a alt= "Link to join crest slack channel" href="https://join.slack.com/t/crest-axz6070/shared_invite/zt-q4qom3p2-7FqwoIg2yffUzlpEE7_bcA" target="_blank">Slack channel </a>

### Contributors

<table>
  <tr>
    <td align="center"><a alt="Sheri Byrne Haber's Github profile" title="Sheri Byrne Haber" href="https://github.com/sheribyrne"><img src="https://avatars.githubusercontent.com/u/47125418?v=4" width="100px;" alt=""/><br /><sub><b>Sheri Byrne Haber</b></sub></a><br /><a href="https://github.com/sheribyrne" title="Code">💻</a></td>
    <td align="center"><a alt="Amit Garg's Github profile" title="Amit Garg" href="https://github.com/gargam17"><img alt="" src="https://avatars.githubusercontent.com/u/82112579?v=4" width="100px;" /><br /><sub><b>Amit Garg</b></sub></a><br /><a href="https://github.com/gargam17" title="Code">💻</a></td>
    <td align="center"><a alt="Joyce Oshita's Github profile" title="Joyce Oshita" href="https://github.com/ojoyce"><img alt="" src="https://avatars.githubusercontent.com/u/57046849?v=4" width="100px;" /><br /><sub><b>Joyce Oshita </b></sub></a><br /><a href="https://github.com/ojoyce" title="Code">💻</a></td>
  </tr>
</table>

### Contributing

The Crest project team welcomes contributions from the community. If you wish to contribute code, please look at our <a alt="link to contrinution markdown file" title="Amit Garg" href="https://github.com/vmware/crest/blob/main/CONTRIBUTING.md">CONTRIBUTING.md</a> file.

### License

Crest is comprised of many open source software components, each of which has its own license that is located in the source code of the respective component as well as documented in the <a alt="link to license file" href="https://github.com/vmware/crest/blob/main/LICENSE">open source license file</a> accompanying the Crest distribution.
<!-- ### Setup

#### Using Pip

1. Install Crest using python package manager (Make sure pip is installed in your system).

```python 
pip install crest
```


#### Using Conda

1. Download and Install Miniconda from [conda.io](https://docs.conda.io/en/latest/miniconda.html)
2. For Windows, launch Miniconda prompt shell. For MacOS, launch the terminal.
3. Create a new virtual environment and install packages.
```python 
conda create -n crest python pandas tqdm
conda activate crest
```
4. If using cuda:
```python
conda install pytorch cudatoolkit=10.1 -c pytorch
```
else:
```python
conda install pytorch cpuonly -c pytorch
```

5. Clone the repository. More details can be found at [docs.github.com](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/cloning-a-repository)

6. Go to "x43_accessibility-" folder in your terminal/prompt shell. Run command.
```python
pip install -r requirements.txt
```
7. Install chromedriver. The details can be found in [chromium.org](https://chromedriver.chromium.org/downloads).

8. Download and Install google-chrome-stable from [ubuntuupdates.org](https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable).

8. Once all the required libraries are installed, run command in your terminal/prompt shell. 
```python
python server.py
```
#### Using Docker

1. Clone the repository. More details can be found at [docs.github.com](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

2. Download and Install docker from [docker.com](https://docs.docker.com/get-docker/). Note: Make sure your docker server as well as crest image is running.

3. Go to "x43_accessibility-" folder in your terminal/prompt shell. Run command.
```python
docker build -t crest .
```
4. Once the docker image is created, run it by executing the following command.
```python
docker container run --name crest_container -p 3000:3000 crest 
``` -->
<!-- ### Usage

To call an API, add the below python code in your script and execute it.

```python
import requests

url = "http://localhost:3000/<service-name>"
payload = "{\"url\" : \"<url-to-test>\"}" 
headers = {
    "content-type": "application/json"
    }

response = requests.request("POST", url, data=payload, headers=headers)
print(response.text) -->

<!-- # replace <service-name> with the actual service name from the service reference table
#For Instance: url = "http://localhost:3000/crest"
#Input optional parameter: "reporttype", value: 3 (for xpath) or 4 (for css selector)
```
**API Reference Table:**

| Description           | service-name                              | Issue IDs                                                                    | 
|---------------|------------------------------------|--------------------------------------------------------------------------------|
| Single API | crest | cr_heading_unrelated, cr_captions_missing, cr_focus_low, cr_focus_missing, cr_podcast_transcript_missing |
| Keyboard Focus Indicator | crest_kb | cr_focus_low, cr_focus_missing |
| Closed Captioning and Transcript Check | crest_av | cr_captions_missing, cr_podcast_transcript_missing |
| Heading Analysis | crest_ha | cr_heading_unrelated |


#### Output description

*Sample Output:*

```python
{
    "categories": {
        "alert": {
            "count": 2,
            "description": "Alerts",
            "items": {
                "cr_heading_unrelated": {
                    "count": 2,
                    "description": "Possibly unrelated heading",
                    "level": "AA",
                    "wcag": "2.4.6",
                    "xpath": [
                        "/html/body/footer/div/div/div[1]/div[2]/h2",
                        "/html/body/div[6]/main/div/section[3]/section/section/div/div[1]/h2"
                    ]
                }
            }
        },
        "error": {
            "count": 1,
            "description": "Errors",
            "items": {
                "cr_captions_missing": {
                    "count": 0,
                    "description": "Captions missing",
                    "level": "A",
                    "wcag": "1.2.2"
                },
                "cr_focus_low": {
                    "count": 1,
                    "description": "Low contrast on Focus",
                    "level": "AA",
                    "wcag": "1.4.11",
                    "xpath": [
                        "/html[1]/body[1]/div[6]/main[1]/header[1]/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]/input[1]"
                    ]
                },
                "cr_focus_missing": {
                    "count": 0,
                    "description": "Focus not visible",
                    "level": "AA",
                    "wcag": "2.4.7",
                    "xpath": []
                },
                "cr_podcast_transcript_missing": {
                    "count": 0,
                    "description": "Podcast transcript missing",
                    "level": "A",
                    "wcag": "1.2.1"
                }
            }
        }
    },
    "screenshot": "/Users/Amitgarg/Documents/VMware Internship/crest/output/screenshot.png",
    "statistics": {
        "pageurl": "https://www.gov.uk/",
        "time": 26.12,
        "totalaudios": 0,
        "totalelements": 128,
        "totalvideos": 0
    },
    "status": {
        "httpstatuscode": 200,
        "success": true
    }
}

```
*Output Definitions:*
* `categories`: Identifies type of issue (errors or alerts).
* `count`: Total Number of errors and alerts on the URL tested. 
* `description`: Description of the error or alert.
* `items`: Identifies number of failed items and relevant details.
* `xpath`: Location of failed elements identified by paths and css selectors.
* `screenshot`: Identifies Path where screenshot of failed elements are reported (red background is used to highlight issues).
* `statistics`: Reports number of elements identified and processing time for the URL.
* `level`: Refers to the conformance level defined by WCAG.
* `wcag`: WCAG success criterion reference.
* `status`: "true” indicates successful execution of script to test page. "false" indicates that the page is not testable. -->

<!-- The detailed description of the Issue IDs can be found in their respective sections. -->

<!-- ### Understanding Results
#### Keyboard Focus Indicator

**Issue ID: cr_focus_low**

*Definition*

When active interface controls (buttons, links, forms, page tabs, etc.) receive keyboard focus, the visual focus indicator does not meet the required color contrast ratio of at least 3:1.

*User Impact*

Low-vision users may have trouble seeing the visual keyboard focus indicator and may not be able to orient themselves on the page to effectively navigate content. Colorblind users may also be affected. 

*Recommendation*

Ensure that the visual keyboard focus indicator provides a sufficient color contrast ratio of at least 3:1 with adjacent colors (background and/or the control colors). Possible solutions include: using the CSS outline property to provide an outline around the focused element, and inverting the foreground and background colors.

*Success Criterion*

1.4.11 Non-text Contrast (Level AA)

*Related Success Criteria (if applicable):*

2.4.7 Focus Visible (Level AA)


More details can be found at [Understanding Success Criterion 1.4.11](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html).

**Issue ID: cr_focus_missing**

*Definition*

There is no visual keyboard focus indication when using TAB or SHIFT+TAB, and/or arrow keys (when applicable) to navigate through the controls (buttons, links, forms, page tabs, etc.) of the website.

*User Impact*

Sighted keyboard-only users are not able to orient themselves on the page and will not be able to effectively navigate content.

*Recommendation*

All interactive content must provide a visual indication of keyboard focus. Focus can be provided in a number of ways including change background, invert colors, border, outline, and other visual methods. Avoid the use of the "outline: none" CSS property.

*Success Criterion*

2.4.7 Focus Visible (Level AA)

*Related Success Criteria (if applicable):*

1.4.11 Non-text Contrast (Level AA)


More details can be found at [Understanding Success Criterion 2.4.7](https://www.w3.org/WAI/WCAG21/Understanding/focus-visible.html).

#### Closed Captioning and Transcript Check

**Issue ID: cr_transcript_missing**

*Definition*

Audio-only content such as podcasts and audio recordings of speeches and press conferences are not made available by transcript.

*User Impact*

When transcripts are provided for audio-only content, people who are deaf or deaf-blind will have access to the information visually or through the use of electronic braille.

*Recommendation*

Provide a transcript for audio-only content.

*Success Criterion*

1.2.1 Prerecorded Audio-only and Video-only (Level A)

*Related Success Criteria (if applicable):*

1.2.3 Audio Description or Media Alternative (Prerecorded) (Level A)


More details can be found at [Understanding Success Criterion 1.2.1](https://www.w3.org/WAI/WCAG21/Understanding/audio-only-and-video-only-prerecorded.html). 


**Issue ID: cr_captions_missing**

*Definition*

Synchronized captions are not provided for video or other multimedia content that contains audio. 

*User Impact*

Users who are deaf or hard of hearing will not have access to important information conveyed in audio. Captions also provide an enhanced experience for users with cognitive differences such as ADHD or learning disabilities. Additionally, captions are useful in certain situations such as environments with loud background noise or situations where sound is not allowed (e.g. the library without headphones, or near a sleeping baby).

*Recommendation*

Provide captions for all important audio information in video and multimedia content.

*Success Criterion*

1.2.2 Captions (Prerecorded) (Level A)

*Related Success Criteria (if applicable):*

2.2.2 Pause, Stop, Hide (Level A) <br />
1.1.1 Non-text Content (Level A)

More details can be found at [Understanding Success Criterion 1.2.2](https://www.w3.org/TR/UNDERSTANDING-WCAG20/media-equiv-captions.html). -->

<!-- #### Heading Analysis

**Issue ID: cr_heading_unrelated**

*Definition*

The content immediately following a heading identified by machine learning is possibly unrelated to the topic or purpose. 

*User Impact*

Blind screen reader users rely on headings to navigate page content. When headings are misleading and do not reflect the topic or purpose, users can become disoriented and have difficulty navigating the page. Users with learning differences may also have difficulty understanding page content when headings are unrelated to content.

*Recommendation*

Provide clear and descriptive headings that accurately describe the immediatley following content.

*Success Criterion*

2.4.6 Headings and Labels (Level AA)

*Related Success Criteria (if applicable):*

1.3.1 Info and Relationships (Level A)


More details can be found at [Understanding Success Criterion 2.4.6](https://www.w3.org/TR/UNDERSTANDING-WCAG20/navigation-mechanisms-descriptive.html).


### TestMePage

Test these APIs on our testMePage:

1. Start the server by following the instruction described in the [Setup](#setup) section.

2. Open a browser window and enter the following URL in the address bar
```python
http://localhost:3000/testMePage
```

3. Please replace the 
```python
<url-to-test>
```
keyword with 
 ```python
 http://localhost:3000/testMePage
 ```
  as mentioned in the [Usage](#usage) section. -->

<!-- ### Default Settings

The default args used are given below. Any of these can be overridden by passing a dict containing the corresponding key: value pairs.

```python
dir_path = os.path.dirname(os.path.realpath(__file__))
global_args = {
    'domain_file_path': dir_path + '/utils/ads_domain.txt',
    'failed_screenshot_path': dir_path + '/utils/screenshot.png',
    'model_params': {
        "training_data_input_file_name": "input/dataset.csv",
        "num_train_epochs": 1,
        "evaluate_during_training": True,
        "fp16": False,
        "use_cuda": False,
        "output_dir": "models/",
        "best_model_dir": "models/best_model/",
        "overwrite_output_dir": True
    }
}

``` -->
<hr /><br>
The Crest team is inspired to make the web accessible to all.  Join us to make it happen!
