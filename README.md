# EmotionSense — AI Emotion Detection

A complete end-to-end machine learning project that classifies text into six emotions using a Logistic Regression model with TF-IDF features. Achieves **86.3% accuracy** on the test set.

| Emotion | Emoji |
|---------|-------|
| Joy | 😊 |
| Sadness | 😢 |
| Anger | 😠 |
| Fear | 😨 |
| Love | ❤️ |
| Surprise | 😲 |

---

## Project Structure

```
├── ModelForge_AI.ipynb     # Jupyter notebook: EDA, preprocessing, training, evaluation
├── train.txt                # Dataset: 16K labeled text samples
├── backend/
│   ├── app.py               # FastAPI server — loads saved model, serves predictions
│   ├── model.pkl            # Trained LogisticRegression model
│   ├── vectorizer.pkl       # TF-IDF vectorizer (vocabulary + weights)
│   └── emotion_map.pkl      # Number → emotion name mapping
├── frontend/
│   └── src/
│       ├── App.jsx          # React UI component
│       ├── App.css           # Styling (dark/light theme, animations)
│       └── index.css         # Global styles
├── requirements.txt         # Python dependencies
├── start.sh                 # One-command launcher for backend + frontend
└── .gitignore
```

---

## ML Workflow

```
Dataset (train.txt)
    │
    ▼
Data Preprocessing
    • Lowercasing
    • Punctuation removal
    • Number removal
    • Emoji removal
    • Stopword removal (NLTK)
    │
    ▼
Feature Extraction
    • TF-IDF Vectorizer (scikit-learn)
    │
    ▼
Model Training
    • LogisticRegression (max_iter=1000)
    • 80/20 train-test split
    • Accuracy: 86.3%
    │
    ▼
Export Artifacts
    • model.pkl
    • vectorizer.pkl
    • emotion_map.pkl
    │
    ▼
Deployment
    • FastAPI backend → loads .pkl files → serves /predict endpoint
    • React frontend → user types text → displays emotion + confidence
```

---

## Libraries Used

| Category | Library | Purpose |
|----------|---------|---------|
| Data | `pandas`, `numpy` | Load & manipulate dataset |
| NLP | `nltk` | Stopword removal |
| ML | `scikit-learn` | TF-IDF vectorizer, LogisticRegression, train/test split |
| Viz | `matplotlib`, `seaborn` | EDA plots in notebook |
| API | `fastapi`, `uvicorn` | Backend REST server |
| Serialization | `joblib` | Save/load trained model artifacts |
| Frontend | `React` + `Vite` | User interface |

---

## Installation

### Prerequisites

- Python 3.10+
- Node.js 18+

### 1. Clone and set up Python environment

```bash
cd AutoMLPipelineSystem

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 3. Train and export the model

Open `ModelForge_AI.ipynb` in Jupyter and run all cells, or run the last cell to export the trained model artifacts:

```python
import joblib

EMOTION_MAP = {v: k for k, v in emotion_numbers.items()}

joblib.dump(logistic_model, 'backend/model.pkl')
joblib.dump(tfidf_vectorizer, 'backend/vectorizer.pkl')
joblib.dump(EMOTION_MAP, 'backend/emotion_map.pkl')
```

---

## Usage

### Option A — Start everything with one command

```bash
./start.sh
```

This launches both servers and verifies they're running.

### Option B — Start manually

#### Terminal 1 — Backend API

```bash
source venv/bin/activate
cd backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

### Access

| Service | URL |
|---------|-----|
| Frontend UI | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

### API Endpoints

**`GET /`** — Health check
```json
{ "message": "Emotion Detection API is running" }
```

**`GET /emotions`** — List supported emotions
```json
{ "emotions": [{ "name": "joy", "emoji": "😊", "color": "#2ECC71" }, ...] }
```

**`POST /predict`** — Predict emotion from text
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"I feel amazing today!"}'
```

Response:
```json
{
  "text": "I feel amazing today!",
  "emotion": "joy",
  "confidence": 0.96,
  "emoji": "😊",
  "color": "#2ECC71",
  "probabilities": [
    { "emotion": "joy",      "probability": 0.9596 },
    { "emotion": "sadness",  "probability": 0.0181 },
    { "emotion": "anger",    "probability": 0.0087 },
    { "emotion": "love",     "probability": 0.0057 },
    { "emotion": "fear",     "probability": 0.0057 },
    { "emotion": "surprise", "probability": 0.0021 }
  ]
}
```

---

## Dataset

- **Source:** 16,000 text samples labeled with emotions
- **Format:** `text;emotion` (semicolon-separated)
- **Distribution:** joy (5,362), sadness (4,666), anger (2,159), fear (1,937), love (1,304), surprise (572)

---

## License

MIT
