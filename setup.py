# Copyright 2020-2021 VMware, Inc.
# SPDX-License-Identifier: MIT
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythoncrest", 
    version="1.0.0",
    author="Sheri Byrne Haber, Amit Garg, Joyce Oshita",
    author_email="sbyrnehaber@vmware.com, gargam@vmware.com, ojoyce@vmware.com",
    description="Automated Accessibility Testing Tool",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://vmware.github.io/crest",
    project_urls={
        "Bug Tracker": "https://github.com/vmware/crest/issues",
    },
    classifiers=[
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "selenium>=3.141.0",
        "requests>=2.24.0",
        "urllib3>=1.25.9",
        "webdriver_manager",
        "pillow",
        "pytesseract>=0.3.6",
        "bs4>=0.0.1",
        "nltk>=3.5",
        "transformers>=4.5.0",
        "pandas>=1.0.5",
        "numpy>=1.19.0",
        "lxml>=4.5.2",
        "flask>=1.1.2",
        "flask_cors>=3.0.10",
        "torch",
    ],
)