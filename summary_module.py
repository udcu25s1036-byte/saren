from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
You are EduGenie helping a student revise.

Summarize the following educational text.
Keep the important facts, remove repetition, and use simple language.
Return:
- A short summary
- 3 to 5 key points

Text:
{text}
"""
    return generate_text(prompt, temperature=0.3, max_output_tokens=1000)
