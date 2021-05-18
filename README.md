<!-- Copyright 2020-2021 VMware, Inc.
SPDX-License-Identifier: MIT -->

<p>
    <br>
    <img src="https://raw.githubusercontent.com/vmware/crest/main/src/crest/static/crest_logo.png?token=ATSPAQYQYG3FH2TQ5USHXLDAUSSQW" />
    <br>
<p>

<p>
    <a href="">
        <img alt="Website" src="https://img.shields.io/badge/beta-phase-red">
    </a>
    <a href="https://vmware.github.io/crest">
        <img alt="Website" src="https://img.shields.io/badge/website-online-green">
    </a>
    <a href="https://pypi.org/project/pythoncrest/">
        <img alt="Build" src="https://img.shields.io/badge/build-python%20package-blue">
    </a>
    <a href="https://github.com/vmware/crest/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/badge/License-MIT-brightgreen">
    </a>
</p>

# Automated Accessibility Testing Tool


**Crest** quickly tests any HTML web page for a simple way to solve your accessibility testing problems. Provide a website URL to our callable API and expose potential WCAG violations. 

Currently supports:
- Keyboard Focus Indicator
- Closed Captioning and Transcript
- Heading Analysis

## Table of contents



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
pip install pythoncrest
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
FLASK_APP=server.py FLASK_ENV=development flask run --port 3000 --host 0.0.0.0
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

The Crest project team welcomes contributions from the community. Before you start working with Crest, please read our [Developer Certificate of Origin](https://cla.vmware.com/dco). All contributions to this repository must be signed as described on that page. Your signature certifies that you wrote the patch or have the right to pass it on as an open-source patch.

If you wish to contribute code, please look at our <a alt="link to contribution markdown file" title="Amit Garg" href="https://github.com/vmware/crest/blob/main/CONTRIBUTING.md">CONTRIBUTING.md</a> file.

### License

Crest is comprised of many open source software components, each of which has its own license that is located in the source code of the respective component as well as documented in the <a alt="link to license file" href="https://github.com/vmware/crest/blob/main/LICENSE">open source license file</a> accompanying the Crest distribution.

<hr />
The Crest team is inspired to make the web accessible to all.  Join us to make it happen!
