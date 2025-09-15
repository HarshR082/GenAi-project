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
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# Maximum characters per chunk to stay under token limits
MAX_CHUNK_SIZE = 5000  # adjust depending on your model's token limit


def chunk_text(text, max_size=MAX_CHUNK_SIZE):
    """
    Split text into chunks of approximately max_size characters.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_size, len(text))
        chunks.append(text[start:end])
        start = end
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
        temperature=0.3
    )
    return response.choices[0].message.content.strip()


def summarize_text(text):
    """
    Summarize text in chunks and combine results.
    """
    system = "You are an assistant that summarizes documents."
    chunks = chunk_text(text)
    summaries = []
    for chunk in chunks:
        prompt = f"Summarize the following text in under 150 words:\n\n{chunk}"
        summaries.append(call_groq_chat(system, prompt))
    return "\n".join(summaries)


def answer_question(context, question):
    """
    Answer user question based ONLY on the provided context.
    """
    system = (
        "You are an assistant that answers questions based only on the provided context. "
        "Always cite exactly which part of the context supports the answer."
    )
    # chunk context if too large
    chunks = chunk_text(context)
    answers = []
    for chunk in chunks:
        prompt = f"""Context:
{chunk}

Question:
{question}

Please answer the question based ONLY on the context. Include a justification citing the supporting text."""
        answers.append(call_groq_chat(system, prompt))
    return " ".join(answers)


def generate_questions(text):
    """
    Generate 3 logic-based or comprehension-focused questions from the document.
    """
    system = "You are a teacher assistant."
    chunks = chunk_text(text)
    all_questions = []
    for chunk in chunks:
        prompt = f"Generate 3 logic-based or comprehension-focused questions from the following text:\n\n{chunk}"
        all_questions.append(call_groq_chat(system, prompt))
    return "\n".join(all_questions)


def evaluate_answer(question, user_answer, context):
    """
    Evaluate user's answer with feedback and justification from the context.
    """
    system = "You are a critical evaluator. Judge if the user's answer is correct based on the context. Provide feedback with justification."
    chunks = chunk_text(context)
    evaluations = []
    for chunk in chunks:
        prompt = f"""
Context:
{chunk}

Question:
{question}

User's Answer:
{user_answer}

Is the answer correct? Provide feedback with justification from the context."""
        evaluations.append(call_groq_chat(system, prompt))
    return " ".join(evaluations)
