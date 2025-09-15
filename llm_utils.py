import os
from groq import Groq

# Load your Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError(
        "\n❌ GROQ_API_KEY environment variable is not set.\n"
        "👉 Please set it before running your server.\n"
    )

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

# Pick your Groq model
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# === Helper: Chunk large text ===
def chunk_text(text, chunk_size=5000, overlap=200):
    """
    Breaks large text into smaller chunks with overlap.
    Default: ~5000 characters per chunk.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def call_groq_chat(system_prompt, user_prompt):
    """
    Calls the Groq chat completion endpoint.
    """
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=2000   # keep safe for each chunk
    )
    return response.choices[0].message.content.strip()

def summarize_text(text):
    """
    Summarize the uploaded text in under 150 words.
    If too large, split into chunks and merge summaries.
    """
    system = "You are an assistant that summarizes documents."

    if len(text) > 5000:  # chunk only if too large
        summaries = []
        for i, chunk in enumerate(chunk_text(text)):
            prompt = f"Summarize part {i+1} of the text in under 100 words:\n\n{chunk}"
            summaries.append(call_groq_chat(system, prompt))
        # final summary
        combined = " ".join(summaries)
        return call_groq_chat(system, f"Combine these partial summaries into one concise summary under 150 words:\n\n{combined}")
    else:
        prompt = f"Summarize the following text in under 150 words:\n\n{text}"
        return call_groq_chat(system, prompt)

def answer_question(context, question):
    """
    Answer user question based ONLY on the provided context.
    If context is large, split into chunks and check each.
    """
    system = (
        "You are an assistant that answers questions based only on the provided context. "
        "Always cite exactly which part of the context supports the answer."
    )

    if len(context) > 5000:
        answers = []
        for chunk in chunk_text(context):
            prompt = f"""Context:
{chunk}

Question:
{question}

Please answer the question based ONLY on the context. Include a justification citing the supporting text."""
            answers.append(call_groq_chat(system, prompt))
        # merge answers into final
        return call_groq_chat(system, f"Merge these partial answers into one final answer:\n\n{answers}")
    else:
        prompt = f"""Context:
{context}

Question:
{question}

Please answer the question based ONLY on the context. Include a justification citing the supporting text."""
        return call_groq_chat(system, prompt)

def generate_questions(text):
    """
    Generate 3 logic-based or comprehension-focused questions from the document.
    """
    system = "You are a teacher assistant."

    if len(text) > 5000:
        questions = []
        for i, chunk in enumerate(chunk_text(text)):
            prompt = f"Generate 2 comprehension-focused questions from part {i+1} of the text:\n\n{chunk}"
            questions.append(call_groq_chat(system, prompt))
        combined = " ".join(questions)
        return call_groq_chat(system, f"From these partial questions, select the 3 most logical and diverse questions:\n\n{combined}")
    else:
        prompt = f"Generate 3 logic-based or comprehension-focused questions from the following text:\n\n{text}"
        return call_groq_chat(system, prompt)

def evaluate_answer(question, user_answer, context):
    """
    Evaluate user's answer with feedback and justification from the context.
    """
    system = "You are a critical evaluator. Judge if the user's answer is correct based on the context. Provide feedback with justification."

    if len(context) > 5000:
        evaluations = []
        for chunk in chunk_text(context):
            prompt = f"""
Context:
{chunk}

Question:
{question}

User's Answer:
{user_answer}

Is the answer correct? Provide feedback with justification from the context."""
            evaluations.append(call_groq_chat(system, prompt))
        combined = " ".join(evaluations)
        return call_groq_chat(system, f"Combine these partial evaluations into one clear evaluation:\n\n{combined}")
    else:
        prompt = f"""
Context:
{context}

Question:
{question}

User's Answer:
{user_answer}

Is the answer correct? Provide feedback with justification from the context."""
        return call_groq_chat(system, prompt)
