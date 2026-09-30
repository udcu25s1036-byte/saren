import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


class GeminiAuthenticationError(Exception):
    pass


class GeminiQuotaError(Exception):
    pass


def generate_text(prompt, temperature=0.4, max_output_tokens=1000):
    if not API_KEY:
        raise GeminiAuthenticationError(
            "GEMINI_API_KEY is missing. Add it to your .env file and restart the server."
        )

    models = [
        "gemini-3.8-flash",
        "gemini-3.8-flash-lite",
    ]

    last_error = None
    quota_error = None

    for model in models:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config={
                        "temperature": temperature,
                        "max_output_tokens": max_output_tokens,
                    },
                )

                return response.text

            except Exception as e:
                last_error = e
                error_text = str(e)

                if any(marker in error_text.upper() for marker in (
                    "401", "403", "UNAUTHENTICATED", "PERMISSION_DENIED", "API_KEY_INVALID"
                )):
                    raise GeminiAuthenticationError(
                        f"Gemini authentication failed: {error_text}"
                    ) from e

                if any(marker in error_text.upper() for marker in (
                    "429", "RESOURCE_EXHAUSTED", "QUOTA_EXCEEDED"
                )):
                    quota_error = e
                    break

                # Retry only for temporary server overload
                if "503" in error_text or "UNAVAILABLE" in error_text:
                    if attempt < 2:
                        time.sleep(3 * (attempt + 1))
                        continue

                    break

                # Other errors should be returned immediately
                raise Exception(f"Gemini API error: {error_text}")

    if quota_error is not None:
        raise GeminiQuotaError(
            "Gemini request quota is exhausted for the available models. "
            "Check your Gemini API quota and billing, or try again after the quota resets."
        ) from quota_error

    raise Exception(
        "Gemini is temporarily unavailable after multiple attempts. "
        f"Last error: {last_error}"
    )


def generate_content(prompt):
    return generate_text(prompt)