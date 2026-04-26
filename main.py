"""
MindEase - Mental Health Chatbot API
FastAPI backend using a trained Logistic Regression model and TF-IDF vectorizer
for mental health text classification and empathetic response generation.
"""

import re
import pickle
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ──────────────────────────────────────────────
# App Initialization
# ──────────────────────────────────────────────

app = FastAPI(
    title="MindEase Chatbot API",
    description="A mental health chatbot powered by NLP classification.",
    version="1.0.0",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────
# Model Loading
# ──────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent

def load_pickle(filepath: Path):
    """Load a pickled object from disk."""
    with open(filepath, "rb") as f:
        return pickle.load(f)

model = load_pickle(BASE_DIR / "model.pkl")
vectorizer = load_pickle(BASE_DIR / "vectorizer.pkl")

# ──────────────────────────────────────────────
# Pydantic Schemas
# ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    """Schema for incoming chat messages."""
    message: str = Field(..., min_length=1, description="User message text")

class ChatResponse(BaseModel):
    """Schema for chatbot responses."""
    response: str = Field(..., description="Chatbot reply")
    label: str = Field(..., description="Predicted mental health label")
    confidence: float = Field(..., description="Prediction confidence score")

# ──────────────────────────────────────────────
# Text Preprocessing
# ──────────────────────────────────────────────

def preprocess_text(text: str) -> str:
    """
    Clean and normalize input text:
      - Convert to lowercase
      - Remove URLs
      - Remove punctuation
      - Remove numbers
      - Collapse multiple spaces
    """
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", "", text)      # Remove URLs
    text = re.sub(r"[^\w\s]", "", text)                # Remove punctuation
    text = re.sub(r"\d+", "", text)                    # Remove numbers
    text = re.sub(r"\s+", " ", text).strip()           # Collapse whitespace
    return text

# ──────────────────────────────────────────────
# Prediction
# ──────────────────────────────────────────────

def predict(text: str) -> tuple[str, float]:
    """
    Run the NLP pipeline on raw input text.

    Returns:
        (label, confidence) — the predicted class and its probability.
    """
    cleaned = preprocess_text(text)
    vectorized = vectorizer.transform([cleaned])
    label = model.predict(vectorized)[0]
    probabilities = model.predict_proba(vectorized)[0]
    confidence = float(probabilities.max())
    return label, confidence

# ──────────────────────────────────────────────
# Response Generation
# ──────────────────────────────────────────────

RESPONSES: dict[str, str] = {
    "depression": (
        "I hear you, and I want you to know that your feelings are valid. "
        "It's okay to not be okay sometimes. You don't have to go through this alone — "
        "consider reaching out to a trusted friend, family member, or a mental health professional. "
        "You matter, and things can get better. 💙"
    ),
    "anxiety": (
        "It sounds like you might be feeling overwhelmed right now. "
        "Try taking a slow, deep breath — inhale for 4 seconds, hold for 4, exhale for 4. "
        "Grounding yourself in the present moment can help. "
        "Remember, it's okay to take things one step at a time. You're doing great. 🌿"
    ),
    "stress": (
        "It seems like you're carrying a heavy load right now. "
        "Please remember that it's okay to take a break and prioritize your well-being. "
        "Even small acts of self-care — a walk, some music, or a few minutes of quiet — "
        "can make a real difference. You're stronger than you think. 💪"
    ),
    "suicidal": (
        "I'm really concerned about what you're sharing, and I want you to know that help is available. "
        "Please reach out to a crisis helpline right away:\n"
        "• **National Suicide Prevention Lifeline**: 988 (call or text)\n"
        "• **Crisis Text Line**: Text HOME to 741741\n"
        "• **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/\n\n"
        "You are not alone, and there are people who care about you deeply. ❤️"
    ),
}

FALLBACK_RESPONSE = (
    "Thank you for sharing. I'm not entirely sure how to interpret that, "
    "but I'm here for you. Could you tell me a little more about how you're feeling?"
)

GENERAL_RESPONSE = (
    "Thank you for opening up. Whatever you're going through, "
    "know that it's okay to seek support. I'm here to listen whenever you need. 😊"
)

CONFIDENCE_THRESHOLD = 0.3


def generate_response(label: str, confidence: float) -> str:
    """
    Build an empathetic chatbot reply based on the predicted label
    and model confidence.
    """
    if confidence < CONFIDENCE_THRESHOLD:
        return FALLBACK_RESPONSE

    return RESPONSES.get(label, GENERAL_RESPONSE)

# ──────────────────────────────────────────────
# API Endpoints
# ──────────────────────────────────────────────

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "MindEase Chatbot API"}


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(request: ChatRequest):
    """
    Process a user message and return an empathetic chatbot response.

    - Preprocesses the input text
    - Classifies it using the trained model
    - Returns a context-appropriate response
    """
    try:
        label, confidence = predict(request.message)
        reply = generate_response(label, confidence)
        return ChatResponse(response=reply, label=label, confidence=confidence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
