from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
You are EduGenie creating a personalized learning path.

Create a beginner-to-advanced learning roadmap for:
{topic}

Include:
1. Beginner level
2. Intermediate level
3. Advanced level
4. Suggested timeline for each level
5. Practice activities
6. Suggested resource types (videos, articles, books, documentation)
7. A final mini-project or assessment

Keep it practical and easy to follow.
"""
    return generate_text(prompt, temperature=0.45, max_output_tokens=1600)
