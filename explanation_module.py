from gemini_client import generate_text


def explain_topic(topic: str) -> str:
    prompt = f"""
You are EduGenie explaining a concept to a beginner.

Explain the following topic in very simple, clear language.
Structure the answer as:
1. Simple definition
2. How it works
3. Easy example
4. Key points to remember

Topic:
{topic}
"""
    return generate_text(prompt, temperature=0.35, max_output_tokens=1100)
