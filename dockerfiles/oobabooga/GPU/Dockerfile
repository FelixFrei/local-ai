# The source image to start with
FROM atinoda/text-generation-webui:latest

# contact info
MAINTAINER Felix Frei; felix.frei@gmx.ch

# Update package lists an install vim and wget
RUN apt-get update && apt-get -y install vim wget asciidoctor ruby rubygems
RUN gem install asciidoctor-pdf

RUN mkdir -p '/opt/ai/'

WORKDIR /opt/ai/

COPY get_bitcoinbook_data_docker.sh .
COPY inMemory.py .
COPY localStore.py .
COPY requirements.txt .

RUN pip install -r requirements.txt