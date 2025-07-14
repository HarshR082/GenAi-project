import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Smart Assistant Dashboard", layout="wide")
st.title("📄 Smart Assistant for Research Summarization")

# Initialize session state variables
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "challenge_questions" not in st.session_state:
    st.session_state.challenge_questions = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = {}

st.sidebar.header("1️⃣ Upload Document")
uploaded_file = st.sidebar.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

if uploaded_file:
    st.sidebar.success(f"✅ File selected: {uploaded_file.name}")
    if st.sidebar.button("Upload to Backend", key="upload_button"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        try:
            res = requests.post(f"{BASE_URL}/upload", files=files)
            if res.status_code == 200:
                st.session_state.uploaded = True
                st.sidebar.success("✅ Document uploaded and processed.")
            else:
                st.sidebar.error(f"❌ Upload failed: {res.text}")
        except Exception as e:
            st.sidebar.error(f"❌ Upload error: {e}")

if st.session_state.uploaded:
    st.success("✅ Document uploaded. Ready to interact!")

    with st.expander("📌 Auto-summary"):
        if st.button("Generate Summary", key="generate_summary"):
            with st.spinner("Generating summary..."):
                try:
                    res = requests.post(f"{BASE_URL}/summarize", json={"text": "Generate summary from uploaded document."})
                    if res.status_code == 200:
                        st.session_state.summary = res.json().get("summary", "")
                    else:
                        st.error(f"❌ Failed to generate summary: {res.text}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        if st.session_state.summary:
            st.write(st.session_state.summary)

    st.divider()
    mode = st.radio("Choose Mode", ["Ask Anything", "Challenge Me"])

    if mode == "Ask Anything":
        st.subheader("🗨️ Ask Anything about the Document")
        question = st.text_input("Your Question", key="ask_question_input")
        if st.button("Submit Question", key="submit_question"):
            if question.strip():
                with st.spinner("Getting answer..."):
                    try:
                        res = requests.post(f"{BASE_URL}/ask", json={"question": question})
                        if res.status_code == 200:
                            answer = res.json().get("answer", "")
                            context = res.json().get("context_used", "")
                            st.markdown("**Answer:**")
                            st.write(answer)
                            with st.expander("Context Used"):
                                st.write(context)
                        else:
                            st.error(f"❌ Failed to get answer: {res.text}")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

    elif mode == "Challenge Me":
        st.subheader("🧩 Challenge Me Mode")

        if not st.session_state.challenge_questions:
            if st.button("Generate 3 Questions", key="generate_challenge_questions"):
                with st.spinner("Generating questions..."):
                    try:
                        res = requests.post(f"{BASE_URL}/generate_questions")
                        if res.status_code == 200:
                            questions_text = res.json().get("questions", "")
                            if isinstance(questions_text, list):
                                st.session_state.challenge_questions = questions_text
                            else:
                                st.session_state.challenge_questions = [q.strip() for q in questions_text.split("\n") if q.strip()]
                        else:
                            st.error(f"❌ Failed to generate questions: {res.text}")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

        # Show questions and input fields
        for idx, question in enumerate(st.session_state.challenge_questions):
            st.markdown(f"**Q{idx + 1}:** {question}")
            answer_key = f"answer_{idx}"
            st.session_state.answers.setdefault(answer_key, "")
            user_input = st.text_input("Your Answer", value=st.session_state.answers[answer_key], key=answer_key)
            st.session_state.answers[answer_key] = user_input

            eval_button_key = f"evaluate_{idx}"
            if st.button(f"Evaluate Q{idx + 1}", key=eval_button_key):
                if user_input.strip():
                    with st.spinner("Evaluating..."):
                        try:
                            res = requests.post(f"{BASE_URL}/evaluate", json={"question": question, "user_answer": user_input})
                            if res.status_code == 200:
                                feedback = res.json().get("feedback", "")
                                context = res.json().get("context_used", "")
                                st.session_state.feedbacks[eval_button_key] = (feedback, context)
                            else:
                                st.error(f"❌ Evaluation failed: {res.text}")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")

            # Show feedback if available
            if eval_button_key in st.session_state.feedbacks:
                feedback, context = st.session_state.feedbacks[eval_button_key]
                st.markdown(f"✅ **Feedback:**")
                st.write(feedback)
                with st.expander("Context Used"):
                    st.write(context)
