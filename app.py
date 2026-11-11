# Import necessary libraries
import os, re
from flask import Flask, render_template, request, redirect
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter

# Import user's Gemini service
from services.gemini_service import generate_answer, grade_essay

start_greeting = ["hi", "hello"]
end_greeting = ["bye"]
way_greeting = ["who are you?"]

# Using this folder for storing the uploaded docs. Creates the folder at runtime if not present
DATA_DIR = "__data__"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Flask App
app = Flask(__name__)

document_context = ""
document_chunks = []
chat_history = []
rubric_text = ""

class HumanMessage:
    def __init__(self, content):
        self.content = content
    
    def __repr__(self):
        return f'HumanMessage(content={self.content})'

class AIMessage:
    def __init__(self, content):
        self.content = content
    
    def __repr__(self):
        return f'AIMessage(content={self.content})'

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        filename = os.path.join(DATA_DIR, pdf.filename)
        pdf_txt = ""
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
                pdf_txt += extracted + "\n"

        with open(filename, "w", encoding="utf-8") as op_file:
            op_file.write(pdf_txt)

    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_relevant_context(question, chunks, full_text):
    """
    Selects relevant context for Gemini. Gemini 3.8 Flash comfortably handles large contexts;
    for very long multi-chapter documents, it selects the top matching chunks.
    """
    if len(full_text) < 40000:
        return full_text
    words = set(re.findall(r'\w+', question.lower()))
    scored = []
    for chunk in chunks:
        score = sum(1 for w in words if w in chunk.lower())
        scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    top_chunks = [c for s, c in scored[:8]]
    return "\n\n".join(top_chunks)

def _grade_essay(essay):
    return grade_essay(essay, rubric_text)

@app.route('/')
def home():
    return render_template('new_home.html')

@app.route('/process', methods=['POST'])
def process_documents():
    global document_context, document_chunks, chat_history
    try:
        pdf_docs = request.files.getlist('pdf_docs')
        if not pdf_docs or not pdf_docs[0].filename:
            return render_template('new_pdf_chat.html', error="Please select at least one valid PDF document.")
        
        raw_text = get_pdf_text(pdf_docs)
        if not raw_text.strip():
            return render_template('new_pdf_chat.html', error="No extractable text found in the uploaded PDF. Please make sure the PDF has selectable text.")

        document_context = raw_text
        document_chunks = get_text_chunks(raw_text)
        chat_history = []
        return redirect('/chat')
    except Exception as e:
        return render_template('new_pdf_chat.html', error=f"Document processing error: {str(e)}")

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    global document_context, document_chunks, chat_history
    error = None
    if request.method == 'POST':
        user_question = request.form.get('user_question', '')
        try:
            if not document_context:
                return render_template('new_chat.html', chat_history=chat_history, error="No documents indexed yet. Please upload a PDF first.")
            
            context = get_relevant_context(user_question, document_chunks, document_context)
            answer = generate_answer(user_question, context)
            
            chat_history.append(HumanMessage(content=user_question))
            chat_history.append(AIMessage(content=answer))
        except Exception as e:
            error = f"Gemini Error: {str(e)}"
        
    return render_template('new_chat.html', chat_history=chat_history, error=error)

@app.route('/pdf_chat', methods=['GET', 'POST'])
def pdf_chat():
    return render_template('new_pdf_chat.html')

@app.route('/essay_grading', methods=['GET', 'POST'])
def essay_grading():
    result = None
    text = None
    error = None
    if request.method == 'POST':
        if request.form.get('essay_rubric', False):
            global rubric_text
            rubric_text = request.form.get('essay_rubric')
            return render_template('new_essay_grading.html')
        
        try:
            if request.files.get('file') and len(request.files['file'].filename) > 0:
                pdf_file = request.files['file']
                text = extract_text_from_pdf(pdf_file)
                result = _grade_essay(text)
            else:
                text = request.form.get('essay_text')
                if text:
                    result = _grade_essay(text)
        except Exception as e:
            error = f"Error during essay grading: {str(e)}"
    
    return render_template('new_essay_grading.html', result=result, input_text=text, error=error)

@app.route('/essay_rubric', methods=['GET', 'POST'])
def essay_rubric():
    return render_template('new_essay_rubric.html')

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False, load_dotenv=False)
