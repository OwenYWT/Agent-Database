import copy
from fastapi import FastAPI, File, UploadFile, HTTPException
import hashlib
import json
import os
from pydantic import BaseModel
import shutil
from typing import List
import uuid

from paper_experiments.utils import get_experiment_config, load_gzipped_file
from paper_experiments.doc_qa_task.doc_qa import DATA_SOURCE_NAME,\
    DOC_QA_PERSONA, DOC_QA_HUMAN, BASELINE_PROMPT, MEMGPT_PROMPT,\
    generate_docqa_response

# from memgpt import MemGPT, utils
from memgpt import create_client
from memgpt.agent_store.storage import StorageConnector, TableType
from memgpt.embeddings import default_embedding_model,embedding_model
from memgpt.schemas.passage import Passage
from concurrent.futures import ThreadPoolExecutor

from contextlib import asynccontextmanager

memgpt_client = None
source_name = "wikipedia"
config = get_experiment_config(os.environ.get("PGVECTOR_TEST_DB_URL"), endpoint_type="openai")
anon_clientid = config.anon_clientid
if anon_clientid.startswith('user-'):
    anon_clientid = anon_clientid.removeprefix('user-')
user_id = uuid.UUID(anon_clientid)
print(user_id)
user_id = str(user_id)
embedding_model1 = embedding_model(config.default_embedding_config)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global memgpt_client
    # Initialize and store your resource
    memgpt_client =  create_client()
    print(memgpt_client)
    yield
    # delete("agent", agent_name)

app = FastAPI(lifespan=lifespan)

def run_docqa_task(
    model="gpt-4", provider="openai", input_question="Answer anything"
) -> List[dict]:  # how many samples (questions) from the file
    """Run the full set of MemGPT doc QA experiments"""
    config = get_experiment_config(os.environ.get("PGVECTOR_TEST_DB_URL"), endpoint_type=provider, model=model)
    config.save()  # save config to file

    # Each line in the jsonl.gz has:
    # - a question (str)
    # - a set of answers (List[str]), often len 1
    # - a set of context documents one of which contains the answer (List[dict])
    # - a gold annotation that has a title of the context doc, a long answer, and a list of short answers
    question = input_question

    # The only thing we actually use here is the 'question'
    # We ignore the documents, and instead rely on a set of documents that is already in a data source
    # TODO make sure this is correct
    responses = generate_docqa_response(
        config=config,
        memgpt_client=memgpt_client,
        persona=DOC_QA_PERSONA,
        human=DOC_QA_HUMAN,
        data_souce_name=DATA_SOURCE_NAME,
        question=question,
    )

    return responses


def create_uuid_from_string(val: str):
    """
    Generate consistent UUID from a string
    from: https://samos-it.com/posts/python-create-uuid-from-random-string-of-words.html
    """
    hex_string = hashlib.md5(val.encode("UTF-8")).hexdigest()
    return uuid.UUID(hex=hex_string)


def insert_lines(line, conn):
    """Parse and insert list of lines into source database"""
    passages = []
    d = line
    # pprint(d)
    assert len(d) == 2, f"Line is empty: {len(d)}"
    text = d[0]["input"]
    model = d[0]["model"]
    embedding = d[1]["data"][0]["embedding"]
    embedding_dim = len(embedding)
    print(len(embedding))
    assert embedding_dim == 1536, f"Wrong embedding dim: {len(embedding)}"
    # assert embedding_dim == 768, f"Wrong embedding dim: {len(embedding)}"
    assert len(d[1]["data"]) == 1, f"More than one embedding: {len(d[1]['data'])}"
    d[1]["usage"]
    # print(text)

    passage_id = create_uuid_from_string(text)  # consistent hash for text (prevent duplicates)
    # if conn.get(passage_id):
    #    continue

    passage = Passage(
        id=passage_id,
        user_id=user_id,
        # user_id=str(user_id),
        text=text,
        embedding_model=model,
        embedding_dim=embedding_dim,
        embedding=embedding,
        # metadata=None,
        data_source=source_name,
    )
    passages.append(passage)
    conn.insert_many(passages)
    return passage_id


def load_file(files: list = [], delete: bool=False):
    # clear out existing source
    if delete:
        delete("source", source_name)
        try:
            passages_table = StorageConnector.get_storage_connector(TableType.PASSAGES, config, user_id)
            passages_table.delete_table()

        except Exception as e:
            print("Failed to delete source")
            print(e)

    # Open the file and read line by line
    conn = StorageConnector.get_storage_connector(TableType.PASSAGES, config, user_id)
    ids = []
    for lines in files:
        ids.append(insert_lines(lines, conn))
    return ids

class AddRequest(BaseModel):
    a: int
    b: int

class Question(BaseModel):
    q: str = "who is the first nobel prize?"

@app.get("/hello")
def hello_world():
    return {"message": "Hello, world!"}

@app.post("/add")
def add_numbers(request: AddRequest):
    return {"result": request.a + request.b}

@app.get("/client")
def answer_question():
    return [str(memgpt_client)]

@app.get("/question")
def answer_question(question:Question):
    question = question.q
    # raw_response = run_docqa_task("meta-llama/Llama-3.1-8B","vllm",question)
    raw_response = run_docqa_task("gpt-4","openai",question)
    raw_response = raw_response.messages
    print(raw_response)
    print(raw_response.__class__)
    filtered_data = [item for item in raw_response\
        if "function_call" == item.message_type and "send_message" == item.function_call.name]
    return filtered_data

# curl -X POST "http://0.0.0.0:8080/uploadfiles/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "files=@/path/to/first_file.txt" -F "files=@/path/to/second_file.txt"
@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    file_details = []
    files_embeding = []
    
    for file in files:
        try:
            # Read the file content as bytes

            contents = await file.read()
            # Decode bytes to string (assuming UTF-8 encoding)
            text = contents.decode("utf-8")
            embedding = embedding_model1.get_text_embedding(text)
            embedding = [{
                    "model": "sentence-transformers/gtr-t5-large",
                    "input": text
                },
                {
                    "object": "list",
                    "data": [
                        {
                            "object": "embedding", 
                            "index": 0, 
                            "embedding":embedding
                        }
                    ],
                    "model": "sentence-transformers/gtr-t5-large",
                    "usage": {"prompt_tokens": len(embedding), "total_tokens": len(embedding)}
            }]
            # print(embedding)
            files_embeding.append(embedding)
            file_details.append({
                "filename": file.filename,
                "content_type": file.content_type,
            })

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read file {file.filename}: {str(e)}")
        ids = load_file(files_embeding)
        print(ids)
        for files_d, id in zip(file_details,ids):
            files_d["id"]=id
        print(file_details)
    return {"files": file_details}
