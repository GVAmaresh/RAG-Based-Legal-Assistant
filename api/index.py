from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks, UploadFile, File, HTTPException
import asyncio
import os
from uuid import uuid4
from api.langChain3 import main_process
from api.chatbot import query_answer

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for task results
task_results: Dict[str, str] = {}


class ChatbotRequest(BaseModel):
    question: str


@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}


@app.post("/api/chatbot")
def chatbot(request: ChatbotRequest):
    answer = query_answer(request.question)
    return {"answer": f"Chatbot message should come {answer}"}


async def process_pdf(file_path: str, task_id: str):
    await asyncio.sleep(10)  # Simulate a long-running task
    summary = main_process(file_path, "api/data/pa.pdf")
    os.remove(file_path)  # Clean up the uploaded file
    task_results[task_id] = summary
    print("Summerized is done!!")


@app.post("/api/uploadFile")
async def upload_files(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"
    upload_dir = "./data"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Ensure the directory exists
    os.makedirs(upload_dir, exist_ok=True)
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    task_id = str(uuid4())
    background_tasks.add_task(process_pdf, file_path, task_id)
    return {"task_id": task_id, "status": "Processing file in the background"}


@app.get("/api/taskResult/{task_id}")
async def get_task_result(task_id: str):
    if task_id not in task_results:
        raise HTTPException(status_code=404, detail="Task not found or not yet completed")
    
    summary = task_results.pop(task_id) 
    return {"task_id": task_id, "summary": summary, "status": "success"}

