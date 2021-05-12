# Copyright 2020-2021 VMware, Inc.
# SPDX-License-Identifier: MIT

FROM python:3.8

# WORKDIR .

COPY ./requirements.txt .

RUN pip install -r requirements.txt
RUN curl https://chromedriver.storage.googleapis.com/2.31/chromedriver_linux64.zip -o /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chromedriver
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb 
# RUN apt-get update
# RUN yes | apt install ./google-chrome-stable_current_amd64.deb 

COPY src/ /usr/src/app/

WORKDIR /usr/src/app/

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

EXPOSE 3000

CMD ["python", "/usr/src/app/crest/server.py"]