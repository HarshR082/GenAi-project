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
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def summarize_text(text):
    """
    Summarize the uploaded text in under 150 words.
    """
    system = "You are an assistant that summarizes documents."
    prompt = f"Summarize the following text in under 150 words:\n\n{text}"
    return call_groq_chat(system, prompt)

def answer_question(context, question):
    """
    Answer user question based ONLY on the provided context.
    """
    system = (
        "You are an assistant that answers questions based only on the provided context. "
        "Always cite exactly which part of the context supports the answer."
    )
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
    prompt = f"Generate 3 logic-based or comprehension-focused questions from the following text:\n\n{text}"
    return call_groq_chat(system, prompt)

def evaluate_answer(question, user_answer, context):
    """
    Evaluate user's answer with feedback and justification from the context.
    """
    system = "You are a critical evaluator. Judge if the user's answer is correct based on the context. Provide feedback with justification."
    prompt = f"""
Context:
{context}

Question:
{question}

User's Answer:
{user_answer}

Is the answer correct? Provide feedback with justification from the context."""
    return call_groq_chat(system, prompt)
