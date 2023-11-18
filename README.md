# local-ai

This project is a collection of tools and scripts to run AI models locally on your machine. 

## Available Scripts

### RAG with Llamaindex und Llama2

Using Llamaindex and Llama2 to build a  RAG setup.
Based on 
https://gpt-index.readthedocs.io/en/latest/examples/vector_stores/SimpleIndexDemoLlama-Local.html

## Prerequisites

You will need a data set.

sudo apt-get install -y asciidoctor

git clone https://github.com/bitcoinbook/bitcoinbook.git

## How to use withouth Docker

``` 
git clone https://github.com/FelixFrei/local-ai.git

cd local-ai/

conda create -n ai python=3.11


pip3 install -r requirements.txt

```

Download the data into the data/swiss-football folder.

```


huggingface-cli login

python3 ragLlamaIndexLlama2.py

``` 


## Docker Images
You can you the base images. These own images are based on the NVIDIA CUDA images and just to safe time.


### Oobabooba GPU

Docker Image to run the Oobabooba model on a GPU.


``` 
docker build -f dockerfiles/oobabooga/GPU/Dockerfile -t felixfreichur/local-ai:0.11.0 .

docker push felixfreichur/local-ai:0.11.0
``` 

### Nvidia CUDA

Docker Image with Nvidia CUDA and PyTorch.

``` 
docker build -f dockerfiles/cuda/Dockerfile -t felixfreichur/cuda:0.1 .

docker push felixfreichur/cuda:0.1
``` 

## How to use
huggingface-cli login

python3 ragLlamaIndexLlama2.py

