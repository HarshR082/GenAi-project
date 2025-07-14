#📚 GenAi Project – Your All-in-One Generative AI Toolkit

A versatile AI-powered platform built using Python and Streamlit, designed to help you generate text, create images, process speech, and analyze data — all through an intuitive and interactive web app.

📜 License
This project is open source and available under the MIT License.

🚀 Features
✅ Generate natural, human-like text from any prompt

🖼️ Produce custom images from textual descriptions

🔊 Convert text to speech and perform speech-to-text transcription

📈 Upload and analyze datasets with AI-powered insights

💬 Interactive chat interface for easy Q&A and content generation

⚡ Lightweight, modular design for fast responses and scalability

⚙️ How to Set Up Locally

1. Clone the repo

git clone https://github.com/HarshR082/GenAi-project.git
cd GenAi-project

2.Create and activate a virtual environment

# On Linux/macOS
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate

3.Install required packages

pip install -r requirements.txt

4.Configure your API keys (if any)

Create a .env file in the root folder and add your keys like:
Groq_API_KEY=your_openai_api_key_here

Alternatively, use Streamlit’s secrets management for safer handling.

5. Launch the app

streamlit run streamlit_app/app.py

🗂 Project Structure Overview

GenAi-project/
├── app.py                 # Main backend app file
├── llm_utils.py           # Language model helper functions
├── list_models.py         # List available AI models
├── rag_utils.py           # Retrieval-augmented generation tools
├── document_utils.py      # Document parsing and processing
├── requirements.txt       # Python dependencies
└── streamlit_app/         # Frontend folder
    └── dashboard.py             # Streamlit user interface

🛠 Technology Stack

| Technology    | Role/Use                                  |
| ------------- | ----------------------------------------- |
| Python        | Core programming language                 |
| Streamlit     | UI framework for interactive frontend     |
| OpenAI API    | Large language models and text generation |
| Hugging Face  | Alternative AI models and hosting         |
| PyPDF2        | Extract text from PDF documents           |
| python-dotenv | Manage environment variables securely     |


🙌 Acknowledgments
OpenAI for providing state-of-the-art language models

Streamlit for enabling fast and easy UI development

Groq API  community for powerful AI tools and models

Python open-source ecosystem for incredible libraries

🤝 Contributing
Feel free to contribute!

Fork the repo

Create a feature branch (git checkout -b feature-name)

Commit your changes (git commit -m 'Add feature')

Push your branch (git push origin feature-name)

Open a pull request

📬 Contact
Made with ❤️ by HarshR082
Open an issue or reach out if you have questions, feedback, or collaboration ideas!


