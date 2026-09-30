import json
import re

from gemini_client import generate_text


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_quiz(passage: str) -> list[dict]:
    prompt = f"""
You are EduGenie generating a student quiz.

Create exactly 3 multiple-choice questions from the supplied passage/topic.
Each question must have exactly 4 options.
The correct_answer must exactly match one option.

Return ONLY valid JSON. No markdown and no extra text.

Required JSON format:
[
  {{
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A"
  }}
]

Passage/topic:
{passage}
"""

    raw = generate_text(prompt, temperature=0.25, max_output_tokens=1400)
    cleaned = clean_json_block(raw)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Quiz JSON parsing failed: {exc}") from exc

    if not isinstance(data, list) or len(data) != 3:
        raise RuntimeError("Gemini did not return exactly 3 quiz questions.")

    validated = []
    for item in data:
        if not isinstance(item, dict):
            raise RuntimeError("Invalid quiz question format.")

        question = item.get("question")
        options = item.get("options")
        correct = item.get("correct_answer")

        if (
            not isinstance(question, str)
            or not isinstance(options, list)
            or len(options) != 4
            or not all(isinstance(x, str) for x in options)
            or not isinstance(correct, str)
            or correct not in options
        ):
            raise RuntimeError("Invalid quiz question/options/correct_answer format.")

        validated.append(
            {
                "question": question,
                "options": options,
                "correct_answer": correct,
            }
        )

    return validated
