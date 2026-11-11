import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.8-flash"


def generate_answer(question, context):

    prompt = f"""
    You are Chat Scholar, an academic AI assistant.

    Use the following study material to answer
    the student's question.

    Study Material:
    {context}

    Question:
    {question}

    Provide a clear and accurate answer.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


def grade_essay(essay_text, rubric_text=""):
    prompt = f"""
    You are Chat Scholar, an academic essay evaluator.

    Evaluate the following essay based strictly on the provided rubric.

    Rubric:
    {rubric_text if rubric_text else "Assess thesis validity, evidence, organization, and language."}

    Essay:
    {essay_text}

    Provide a structured evaluation with strengths, areas for improvement, and an overall grade.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.replace("\n", "<br>")
