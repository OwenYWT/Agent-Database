import gzip
import json
from typing import List

from memgpt.config import MemGPTConfig
from memgpt.constants import LLM_MAX_TOKENS
# from memgpt.data_types import EmbeddingConfig, LLMConfig
from memgpt.schemas.embedding_config import EmbeddingConfig
from memgpt.schemas.llm_config import LLMConfig


def load_gzipped_file(file_path):
    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def read_jsonl(filename) -> List[dict]:
    lines = []
    with open(filename, "r") as file:
        for line in file:
            lines.append(json.loads(line.strip()))
    return lines


def get_experiment_config(postgres_uri, endpoint_type="openai", model="gpt-4"):
    config = MemGPTConfig.load()
    #this overwriten the setting from config file(and above load())
    config.archival_storage_type = "postgres"
    config.archival_storage_uri = postgres_uri

    if endpoint_type == "openai":
        llm_config = LLMConfig(
            model=model, model_endpoint_type="openai", model_endpoint="https://api.openai.com/v1", context_window=LLM_MAX_TOKENS[model]
        )
        embedding_config = EmbeddingConfig(
            embedding_endpoint_type="openai",
            embedding_endpoint="https://api.openai.com/v1",
            embedding_dim=1536,
            embedding_model="text-embedding-ada-002",
            embedding_chunk_size=300,  # TODO: fix this
        )
    else:
        # assert model == "ehartford/dolphin-2.5-mixtral-8x7b", "Only model supported is ehartford/dolphin-2.5-mixtral-8x7b"
        if model == "ehartford/dolphin-2.5-mixtral-8x7b":
            llm_config = LLMConfig(
                model="ehartford/dolphin-2.5-mixtral-8x7b",
                model_endpoint_type="vllm",
                model_endpoint="https://api.memgpt.ai",
                model_wrapper="chatml",
                context_window=16384,
            )
            embedding_config = EmbeddingConfig(
                embedding_endpoint_type="hugging-face",
                embedding_endpoint="https://embeddings.memgpt.ai",
                embedding_dim=1024,
                embedding_model="BAAI/bge-large-en-v1.5",
                embedding_chunk_size=300,
            )
        elif model == "meta-llama/Llama-3.1-8B":
            llm_config = LLMConfig(
                model="meta-llama/Llama-3.1-8B",
                model_endpoint_type="vllm",
                model_endpoint="http://0.0.0.0:8000",
                model_wrapper="llama3",
                context_window=16384,
            )
            embedding_config = EmbeddingConfig(
                embedding_endpoint_type="default",
                embedding_endpoint="http://0.0.0.0:8000",
                embedding_dim=1536,
                embedding_model="BAAI/bge-large-en-v1.5",
                embedding_chunk_size=300,
            )
        # elif model == "meta-llama/Llama-3.3-70B-Instruct":
        #     llm_config = LLMConfig(
        #         model="meta-llama/Llama-3.3-70B-Instruct",
        #         model_endpoint_type="vllm",
        #         model_endpoint="http://0.0.0.0:8001",
        #         model_wrapper="llama3",
        #         context_window=16384,
        #     )
        #     embedding_config = EmbeddingConfig(
        #         embedding_endpoint_type="default",
        #         embedding_endpoint="http://0.0.0.0:8000",
        #         embedding_dim=1536,
        #         embedding_model="BAAI/bge-large-en-v1.5",
        #         embedding_chunk_size=300,
        #     )
        elif model == "meta-llama/Llama-3.3-70B-Instruct":
            llm_config = LLMConfig(
                model="meta-llama/Llama-3.3-70B-Instruct",
                model_endpoint_type="vllm",
                model_endpoint="http://0.0.0.0:8001",
                model_wrapper="llama3",
                context_window=16384,
            )
            embedding_config = EmbeddingConfig(
                embedding_endpoint_type="openai",
                # embedding_endpoint="http://0.0.0.0:8000",
                embedding_endpoint="https://api.openai.com/v1",
                embedding_dim=1536,
                embedding_model="text-embedding-ada-002-v2",
                embedding_chunk_size=300,
            )
        else:
            raise Exception("Wrong Model!")
    # this overwrite the config is the one we used
    config = MemGPTConfig(
        anon_clientid=config.anon_clientid,
        archival_storage_type="postgres",
        archival_storage_uri=postgres_uri,
        recall_storage_type="postgres",
        recall_storage_uri=postgres_uri,
        metadata_storage_type="postgres",
        metadata_storage_uri=postgres_uri,
        default_llm_config=llm_config,
        default_embedding_config=embedding_config,
    )
    print("Config model", config.default_llm_config.model)
    return config
