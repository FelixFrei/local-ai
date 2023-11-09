# local-ai

This project is a collection of tools and scripts to run AI models locally on your machine. 

## Available Scripts

In the project directory, you can run:

### `runLocalLlama.py`

Runs a local Lllama model.


## Docker Images

### Oobabooba GPU

Docker Image to run the Oobabooba model on a GPU.
`

``` 
docker build -f oobabooga/GPU/Dockerfile -t felixfreichur/local-ai:0.9.0 .

docker push felixfreichur/local-ai:0.9.0
``
