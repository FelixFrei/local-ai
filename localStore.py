import logging
import sys
import torch
import os
from llama_index.llms import HuggingFaceLLM
from llama_index.prompts import PromptTemplate
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage, \
    set_global_service_context, ServiceContext

os.environ['NUMEXPR_MAX_THREADS'] = '4'
os.environ['NUMEXPR_NUM_THREADS'] = '2'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Model names (make sure you have access on HF)
LLAMA2_7B = "meta-llama/Llama-2-7b-hf"
LLAMA2_7B_CHAT = "meta-llama/Llama-2-7b-chat-hf"
LLAMA2_13B = "meta-llama/Llama-2-13b-hf"
LLAMA2_13B_CHAT = "meta-llama/Llama-2-13b-chat-hf"
LLAMA2_70B = "meta-llama/Llama-2-70b-hf"
LLAMA2_70B_CHAT = "meta-llama/Llama-2-70b-chat-hf"

selected_model = LLAMA2_7B_CHAT

SYSTEM_PROMPT = """You are an AI assistant that answers questions in a friendly manner, based on the given source documents. Here are some rules you always follow:
- Generate human readable output, avoid creating output with gibberish text.
- Generate only the requested output, don't include any other language before or after the requested output.
- Never say thank you, that you are happy to help, that you are an AI agent, etc. Just answer directly.
- Generate professional language typically used in business documents in North America.
- Never generate offensive or foul language.
"""

query_wrapper_prompt = PromptTemplate(
    "[INST]<<SYS>>\n" + SYSTEM_PROMPT + "<</SYS>>\n\n{query_str}[/INST] "
)

llm = HuggingFaceLLM(
    context_window=4096,
    max_new_tokens=2048,
    generate_kwargs={"temperature": 0.0, "do_sample": False},
    query_wrapper_prompt=query_wrapper_prompt,
    tokenizer_name=selected_model,
    model_name=selected_model,
    device_map="auto",
    # change these settings below depending on your GPU
    model_kwargs={"torch_dtype": torch.float16, "load_in_8bit": True},
)


service_context = ServiceContext.from_defaults(
    llm=llm, embed_model="local:BAAI/bge-small-en"
)
set_global_service_context(service_context)

try:
    storage_context = StorageContext.from_defaults(persist_dir='./storage/cache/bitcoinbook/')
    index = load_index_from_storage(storage_context)
    # query will use the same embed_model
    query_engine = index.as_query_engine(
        verbose=True,
    )
    print('loading from disk')
except:
    # load index
    documents = SimpleDirectoryReader("./data/bitcoinbook/").load_data()
    new_index = VectorStoreIndex.from_documents(
        documents,
        service_context=service_context,
    )

    # query will use the same embed_model
    query_engine = new_index.as_query_engine(
        verbose=True,
    )

    new_index.storage_context.persist(persist_dir='./storage/cache/bitcoinbook/')
    print('persisting to disk')

response = query_engine.query("What is the purpose of BIP39?")
print("The answer is:")
print(response)

while True:
    question = input("Please insert your question: ")

    if question == '\x1b':
        break

    response = query_engine.query(question)
    print("The answer is:")
    print(response)
