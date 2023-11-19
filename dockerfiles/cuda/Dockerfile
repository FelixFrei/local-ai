# The source image to start with
FROM nvidia/cuda:12.0.1-devel-ubuntu20.04
# contact info
MAINTAINER Felix Frei; felix.frei@gmx.ch

# Update package lists an install vim and wget
RUN apt-get update && apt-get -y install vim wget

RUN mkdir -p '/opt/ai/'

WORKDIR /opt/ai/

COPY get_bitcoinbook_data.sh .
COPY inMemory.py .
COPY localStore.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

RUN chmod +x get_bitcoinbook_data.sh
RUN ./get_bitcoinbook_data.sh