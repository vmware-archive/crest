# Copyright 2020-2021 VMware, Inc.
# SPDX-License-Identifier: MIT

FROM python:3.8

# WORKDIR .

COPY ./requirements.txt .

RUN pip install -r requirements.txt
RUN curl "https://chromedriver.storage.googleapis.com/$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip" -o /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome-stable_current_amd64.deb \
    && apt update \
    && apt --assume-yes install ./google-chrome-stable_current_amd64.deb \
    && rm -r /var/lib/apt/lists

COPY src/ /usr/src/app/

WORKDIR /usr/src/app/

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

EXPOSE 3000

CMD ["python", "/usr/src/app/crest/server.py"]
