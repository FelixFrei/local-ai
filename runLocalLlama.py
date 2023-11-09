import logging
import sys
import torch
from llama_index.llms import HuggingFaceLLM
from llama_index.prompts import PromptTemplate
from llama_index import VectorStoreIndex, ServiceContext, set_global_service_context, SimpleDirectoryReader

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

documents = SimpleDirectoryReader("./data/paul_graham/").load_data()

service_context = ServiceContext.from_defaults(
    llm=llm, embed_model="local:BAAI/bge-small-en"
)
set_global_service_context(service_context)

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()

response = query_engine.query("What did the author do growing up?")
print("The answer is:")
print(response)
