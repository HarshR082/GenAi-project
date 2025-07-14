from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import document_utils
import rag_utils
import llm_utils

app = FastAPI(
    title="Smart Assistant for Research Summarization",
    description="Backend API for document-aware assistant",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global vector store and document text
vector_store = rag_utils.VectorStore()
full_text = ""

class AskRequest(BaseModel):
    question: str

class EvaluateRequest(BaseModel):
    question: str
    user_answer: str

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    global full_text, vector_store
    content = await file.read()

    if file.content_type == "application/pdf":
        full_text = document_utils.extract_text_from_pdf(content)
    else:
        full_text = document_utils.extract_text_from_txt(content)

    chunks = document_utils.chunk_text(full_text)
    vector_store = rag_utils.VectorStore()
    vector_store.add_text_chunks(chunks)

    return {"message": "Document processed", "total_chunks": len(chunks)}

@app.post("/summarize")
async def summarize():
    global full_text
    if not full_text:
        return {"error": "No document uploaded yet."}
    summary = llm_utils.summarize_text(full_text)
    return {"summary": summary}

@app.post("/ask")
async def ask_question(request: AskRequest):
    retrieved = vector_store.retrieve(request.question)
    context = "\n\n".join(retrieved)
    answer = llm_utils.answer_question(context, request.question)
    return {"answer": answer, "context_used": context}

@app.post("/generate_questions")
async def generate_questions():
    global full_text
    if not full_text:
        return {"error": "No document uploaded yet."}
    questions = llm_utils.generate_questions(full_text)
    return {"questions": questions}

@app.post("/evaluate")
async def evaluate(request: EvaluateRequest):
    retrieved = vector_store.retrieve(request.question)
    context = "\n\n".join(retrieved)
    feedback = llm_utils.evaluate_answer(request.question, request.user_answer, context)
    return {"feedback": feedback, "context_used": context}
