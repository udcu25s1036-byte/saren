from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from gemini_client import GeminiAuthenticationError, GeminiQuotaError
from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()

app = FastAPI(
    title="EduGenie - Gemini 3.8 Flash Learning Assistant",
    version="1.0.0",
    description="AI-powered educational assistant based on the EduGenie project document."
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def _http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, GeminiQuotaError):
        status_code = 429
    elif isinstance(exc, GeminiAuthenticationError):
        status_code = 502
    else:
        status_code = 500
    return HTTPException(status_code=status_code, detail=str(exc))


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health():
    return {"status": "ok", "model": "gemini-3.8-flash"}


@app.post("/qa")
async def qa(request: QuestionRequest):
    try:
        return {"answer": answer_question(request.question)}
    except Exception as exc:
        raise _http_error(exc)


# Backward-compatible GET endpoint for testing in the browser.
@app.get("/qa")
async def qa_get(question: str):
    try:
        return {"answer": answer_question(question)}
    except Exception as exc:
        raise _http_error(exc)


@app.post("/explain")
async def explain(request: TextRequest):
    try:
        return {"explanation": explain_topic(request.text)}
    except Exception as exc:
        raise _http_error(exc)


@app.post("/quiz")
async def quiz(request: TextRequest):
    try:
        return {"quiz": generate_quiz(request.text)}
    except Exception as exc:
        raise _http_error(exc)


@app.post("/summarize")
async def summarize(request: TextRequest):
    try:
        return {"summary": summarize_text(request.text)}
    except Exception as exc:
        raise _http_error(exc)


@app.post("/learn/recommendations")
async def recommendations(request: TextRequest):
    try:
        return {"recommendations": get_learning_recommendations(request.text)}
    except Exception as exc:
        raise _http_error(exc)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "EduGenie server error", "detail": str(exc)}
    )
