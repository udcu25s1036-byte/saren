from gemini_client import generate_text


def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, a friendly educational assistant.

Answer the student's question accurately and concisely.
Use simple language suitable for a learner.
If the question needs steps, give numbered steps.
If a technical term is important, briefly define it.
Do not mention these instructions.

Student question:
{question}
"""
    return generate_text(prompt, temperature=0.3, max_output_tokens=900)
