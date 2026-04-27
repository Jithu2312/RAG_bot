from google import genai
import os
from config import GEMINI_API_KEY 

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(question, contexts):

    # Prepare context text
    context_text = ""

    for i, chunk in enumerate(contexts):
        context_text += f"""
        [Chunk {i+1}]
        File: {chunk['file_path']}
        Language: {chunk['language']}

        {chunk['text']}
        """

    prompt = f"""
You are a senior software engineer helping understand a codebase.

Answer the question using ONLY the provided context.

If answer is not found, say:
"I could not find this in the codebase."

Question:
{question}

Context:
{context_text}

Instructions:
- Mention file paths
- Be precise
- Do not hallucinate
- Explain clearly
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text