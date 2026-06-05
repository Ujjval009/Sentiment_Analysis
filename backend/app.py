import os
import sys
import string
import logging
import joblib
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("backend")

BASE = os.path.dirname(__file__)
log.info("Backend directory: %s", BASE)
log.info("Python: %s", sys.version)

model_path = os.path.join(BASE, 'model.pkl')
vectorizer_path = os.path.join(BASE, 'vectorizer.pkl')
emotion_map_path = os.path.join(BASE, 'emotion_map.pkl')

log.info("Checking model.pkl:   exists=%s", os.path.exists(model_path))
log.info("Checking vectorizer.pkl: exists=%s", os.path.exists(vectorizer_path))
log.info("Checking emotion_map.pkl: exists=%s", os.path.exists(emotion_map_path))

try:
    model = joblib.load(model_path)
    log.info("model.pkl loaded successfully")
except Exception as e:
    log.error("FAILED to load model.pkl: %s", e)
    raise

try:
    vectorizer = joblib.load(vectorizer_path)
    log.info("vectorizer.pkl loaded successfully")
except Exception as e:
    log.error("FAILED to load vectorizer.pkl: %s", e)
    raise

try:
    EMOTION_MAP = joblib.load(emotion_map_path)
    log.info("emotion_map.pkl loaded successfully: %s", EMOTION_MAP)
except Exception as e:
    log.error("FAILED to load emotion_map.pkl: %s", e)
    raise

log.info("All model artifacts loaded. Ready to serve requests.")

app = FastAPI(title="Emotion Detection API")

origins = os.getenv("CORS_ORIGINS", "*").split(",")
allow_creds = origins != ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=allow_creds,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMOJI_MAP = {
    'sadness': '😢',
    'anger': '😠',
    'love': '❤️',
    'surprise': '😲',
    'fear': '😨',
    'joy': '😊',
}

COLOR_MAP = {
    'sadness': '#5B8DEF',
    'anger': '#FF4B5C',
    'love': '#FF6B9D',
    'surprise': '#FFB347',
    'fear': '#9B59B6',
    'joy': '#2ECC71',
}

class TextInput(BaseModel):
    text: str = Field(..., max_length=1000, min_length=1)

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ''.join(c for c in text if not c.isdigit())
    text = ''.join(c for c in text if c.isascii())
    return text

@app.get("/emotions")
def get_emotions():
    log.info("GET /emotions")
    return {
        "emotions": [
            {"name": k, "emoji": EMOJI_MAP.get(k, ''), "color": COLOR_MAP.get(k, '')}
            for k in EMOTION_MAP.values()
        ]
    }

@app.post("/predict")
def predict(input: TextInput):
    log.info("POST /predict - input text: '%s'", input.text[:120])

    processed = preprocess(input.text)
    features = vectorizer.transform([processed])
    probs = model.predict_proba(features)[0]
    pred_class = int(model.predict(features)[0])
    emotion_name = EMOTION_MAP[pred_class]
    confidence = float(probs[pred_class])
    log.info("Prediction: %s (%.1f%%)", emotion_name, confidence * 100)

    all_probs = [
        {"emotion": EMOTION_MAP[i], "probability": round(float(p), 4)}
        for i, p in enumerate(probs)
    ]
    all_probs.sort(key=lambda x: x["probability"], reverse=True)

    result = {
        "text": input.text,
        "emotion": emotion_name,
        "confidence": round(confidence, 4),
        "emoji": EMOJI_MAP.get(emotion_name, ''),
        "color": COLOR_MAP.get(emotion_name, ''),
        "probabilities": all_probs,
    }
    log.info("Response sent successfully")
    return result

@app.get("/health")
def health():
    return {"status": "ok"}

FRONTEND_DIR = os.path.join(BASE, "..", "frontend", "dist")
if os.path.isdir(FRONTEND_DIR):
    log.info("Mounting frontend static files from: %s", FRONTEND_DIR)
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    log.warning("Frontend dist not found at %s — SPA not mounted", FRONTEND_DIR)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    log.info("Starting uvicorn on 0.0.0.0:%d", port)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
