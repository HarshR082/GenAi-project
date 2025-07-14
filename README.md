# 🚀 GenAi Project – Your All-in-One Generative AI Toolkit

Welcome to **GenAi Project**!  
A versatile, AI-powered platform built with Python and Streamlit — generate text, create images, process speech, and analyze data, all from a sleek interactive web app.

---

## 🧩 Features

- ✨ **Natural Text Generation:** Produce human-like text from any prompt
- 🖼️ **Custom Image Creation:** Transform textual descriptions into images
- 🔊 **Speech Processing:** Text-to-speech & speech-to-text transcription
- 📊 **Smart Data Analysis:** Upload datasets, unlock AI-driven insights
- 💬 **Chat Interface:** Q&A and content generation in real time
- ⚡ **Modular, Scalable:** Lightweight design for fast responses

---

## ⚙️ Local Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/HarshR082/GenAi-project.git
    cd GenAi-project
    ```

2. **Create & Activate a Virtual Environment**
    ```bash
    # Linux/macOS
    python -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure API Keys**
    - Create a `.env` file in the root folder:
        ```
        Groq_API_KEY=your_openai_api_key_here
        ```
    - Or use Streamlit’s secrets management for enhanced security.

5. **Launch the App**
    ```bash
    streamlit run streamlit_app/dashboard.py
    ```

---

## 🗂 Project Structure

GenAi-project/
├── app.py                 # Main backend app file
├── llm_utils.py           # Language model helper functions
├── list_models.py         # List available AI models
├── rag_utils.py           # Retrieval-augmented generation tools
├── document_utils.py      # Document parsing and processing
├── requirements.txt       # Python dependencies
└── streamlit_app/         # Frontend folder
    └── dashboard.py             # Streamlit user interface


---

## 🛠 Technology Stack

| Technology      | Role/Use                                  |
|-----------------|-------------------------------------------|
| Python          | Core programming language                 |
| Streamlit       | Interactive UI framework                  |
| OpenAI API      | Large language models                     |
| Hugging Face    | Alternative AI models & hosting           |
| PyPDF2          | PDF text extraction                       |
| python-dotenv   | Secure environment variable management    |

---

## 🙌 Acknowledgments

- **OpenAI:** State-of-the-art language models
- **Streamlit:** Fast, easy UI development
- **Groq API Community:** Powerful AI tools and models
- **Python OSS:** Incredible libraries

---

## 🤝 Contributing

1. **Fork** the repo
2. **Create** your feature branch  
    `git checkout -b feature-name`
3. **Commit** your changes  
    `git commit -m 'Add feature'`
4. **Push** your branch  
    `git push origin feature-name`
5. **Open** a pull request

---

## 📬 Contact

Made with ❤️ by [HarshR082](https://github.com/HarshR082)  
Open an issue or reach out for support, feedback, or collaboration!

---

## 📜 License

This project is open source and available under the MIT License.

