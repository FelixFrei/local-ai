# The source image to start with
FROM atinoda/text-generation-webui:latest

# contact info
MAINTAINER Felix Frei; felix.frei@gmx.ch

# Update package lists an install vim and wget
RUN apt-get update && apt-get -y install vim wget


RUN mkdir -p '/opt/ai/'


WORKDIR /opt/ai/

COPY requirements.txt .

RUN pip install -r requirements.txt


RUN mkdir -p 'data/swiss-football/'

WORKDIR /opt/ai/data/swiss-football

COPY get_swiss-football_dataset.sh .

RUN chmod +x get_swiss-football_dataset.sh
RUN ./get_swiss-football_dataset.sh
