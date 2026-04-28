from google import genai
import os
from config import GEMINI_API_KEY 

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(question, contexts, history=None):

    history_text = ""

    if history:
        for msg in history:
            role = msg["role"]
            content = msg["content"]
            history_text += f"{role.upper()}: {content}\n"

    context_text = ""

    for chunk in contexts:
        context_text += f"""
File: {chunk.get('file_path')}
Code:
{chunk.get('text')}
"""

    prompt = f"""
You are a senior software engineer.

Conversation History:
{history_text}

Answer the question using context.

Question:
{question}

Context:
{context_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text