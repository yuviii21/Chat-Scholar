# ChatScholar 📚
> **Academic Document Inquiry & Rubric-Guided Essay Evaluation Platform**

ChatScholar is an academic workspace built for students, researchers, and educators. It simplifies reading dense research papers and elevates writing quality through grounded document question answering and rubric-calibrated essay critiques powered by **Google Gemini 3.8 Flash**.

---

## 🌟 Key Features

### 1. Source-Grounded Document Inquiry
* Ingest multi-page academic PDFs with automatic text extraction and chunk normalization.
* Query your sources directly—answers are strictly grounded in your uploaded documents to prevent hallucinations.
* Auto-scrolling conversation thread designed for sustained research reading.

### 2. Rubric-Calibrated Essay Studio
* Define custom evaluation rubrics with specific focus areas, criteria weights, and performance benchmarks.
* Submit essays as raw draft text or upload manuscript PDFs.
* Receive structured, actionable academic feedback with rubric scores, strengths, and targeted revision guidance.

### 3. Human-Crafted Academic Interface
* **Academic Editorial (Light Theme):** High-contrast, warm off-white canvas with sharp typography and tactile components designed to feel like a scholarly journal.
* **Scholar Obsidian (Dark Theme):** Deep charcoal and slate workspace free of neon glows or synthetic AI gradient tropes.
* Persistent **`☀️ / 🌙 Theme`** switcher stored in browser preferences.

---

## 🏗️ Project Architecture

```text
ChatScholar/
├── app.py                      # Flask application routes and document pipelines
├── services/
│   ├── __init__.py
│   └── gemini_service.py       # Google GenAI SDK client & prompt orchestrations
├── static/
│   ├── app.css                 # Scholarly design system (Light & Dark themes)
│   └── app.js                  # Theme toggle, drag-and-drop, and chat auto-scroll
├── templates/
│   ├── base.html               # Shell layout, navigation, and theme loader
│   ├── new_home.html           # Landing page with workflow pillars & dossier preview
│   ├── new_pdf_chat.html       # Document upload and ingestion workspace
│   ├── new_chat.html           # Grounded research conversation thread
│   ├── new_essay_rubric.html   # Rubric criteria setup phase
│   └── new_essay_grading.html  # Essay submission desk & evaluation report
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── .gitignore                  # Protection for secret keys, caches, and upload data
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10+ (tested on Python 3.13)
* A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yuviii21/Chat-Scholar.git
   cd Chat-Scholar
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API Key:**
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Add your Gemini API key inside `.env`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Start the application:**
   ```bash
   python app.py
   ```

6. Open your browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

---

## 🛠️ Technology Stack

* **Backend:** Flask, Python 3
* **Large Language Model:** Google Gemini 3.8 Flash (`google-genai` SDK)
* **Document Processing:** PyPDF2, LangChain Text Splitters
* **Frontend:** Modern CSS3 variables, Semantic HTML5, Vanilla JavaScript

---

## 🔒 Security & Privacy

* API keys and secrets are loaded securely from environment variables.
* Uploaded files and local caches are ignored by `.gitignore` to prevent sensitive academic documents from being committed to version control.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
