# EduGenie - Gemini 3.8 Flash

EduGenie is a FastAPI + HTML/CSS/JavaScript educational assistant based on the supplied project document.

## Features
- Question answering
- Simple concept explanations
- 3-question MCQ quiz generation
- Text summarization
- Beginner-to-advanced learning recommendations

## Model
Gemini 3.8 Flash:
`gemini-3.8-flash`

## Setup
```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` and replace the placeholder with your Gemini API key.

## Run
```powershell
uvicorn main:app --reload
```

Open:
http://127.0.0.1:8000

## API
- GET `/`
- GET `/health`
- POST `/qa`
- POST `/explain`
- POST `/quiz`
- POST `/summarize`
- POST `/learn/recommendations`

For quick browser testing:
`http://127.0.0.1:8000/qa?question=Why%20is%20the%20sky%20blue`
