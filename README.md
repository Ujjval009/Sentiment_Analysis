# EmotionSense

**AI-Powered Emotion Detection** — A full-stack web application that analyzes text and detects emotions (joy, sadness, anger, love, surprise, fear) using a Logistic Regression model with TF-IDF vectorization.

![Demo](https://img.shields.io/badge/status-production-green)
![Python](https://img.shields.io/badge/python-3.12-blue)
![React](https://img.shields.io/badge/react-19-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.100+-teal)

---

## Features

- **Real-time emotion classification** from natural language text
- **6 emotion categories** with emoji and color-coded confidence visualization
- **Probability breakdown** showing confidence across all emotion classes
- **Dark/light theme** toggle
- **Responsive design** — works on desktop and mobile
- **REST API** — can be used independently as an emotion detection service
- **86.3% model accuracy** — Logistic Regression trained on labeled text data

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 19, Vite |
| **Backend** | FastAPI, Uvicorn |
| **ML Model** | scikit-learn (Logistic Regression), TF-IDF |
| **Data Processing** | Pandas, NLTK, NumPy |
| **Deployment** | Render (backend), Vercel (frontend) |
| **Containerization** | Docker, docker-compose |

---

## Project Structure

```
sentiment-analysis/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── model.pkl              # Trained Logistic Regression model
│   ├── vectorizer.pkl         # TF-IDF vectorizer
│   └── emotion_map.pkl        # Emotion label mapping
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── App.css            # Application styles
│   │   └── main.jsx           # Entry point
│   ├── public/
│   ├── vite.config.js         # Vite configuration with API proxy
│   └── vercel.json            # Vercel SPA routing config
├── ModelForge_AI.ipynb        # Jupyter notebook (model training & exploration)
├── retrain.py                 # Standalone training script
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Multi-stage Docker build
├── docker-compose.yml         # Docker Compose configuration
├── start.sh                   # Production startup script
└── .env.example               # Environment variable reference
```

---

## Quick Start (Local Development)

### Prerequisites

- Python 3.12+
- Node.js 20+

### 1. Clone & Setup

```bash
git clone https://github.com/Ujjval009/Sentiment_Analysis.git
cd Sentiment_Analysis
```

### 2. Backend

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

> **Note:** The frontend Vite dev server proxies `/predict` and `/emotions` to `http://localhost:8000`. No extra config needed.

### 4. Verify

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"I feel so happy today!"}'
```

Expected response:

```json
{
  "emotion": "joy",
  "confidence": 0.8559,
  "emoji": "😊",
  "color": "#2ECC71",
  "probabilities": [
    {"emotion": "joy", "probability": 0.8559},
    {"emotion": "sadness", "probability": 0.0549}
  ]
}
```

---

## API Documentation

### `POST /predict`

Detect emotion from text.

**Request:**
```json
{
  "text": "I feel amazing about my new project"
}
```

**Response:**
```json
{
  "text": "I feel amazing about my new project",
  "emotion": "joy",
  "confidence": 0.7729,
  "emoji": "😊",
  "color": "#2ECC71",
  "probabilities": [
    {"emotion": "joy", "probability": 0.7729},
    {"emotion": "sadness", "probability": 0.0956},
    {"emotion": "anger", "probability": 0.0458},
    {"emotion": "love", "probability": 0.0428},
    {"emotion": "fear", "probability": 0.0294},
    {"emotion": "surprise", "probability": 0.0135}
  ]
}
```

### `GET /emotions`

Returns all supported emotions with their emoji and color.

### `GET /health`

Health check endpoint. Returns `{"status": "ok"}`.

---

## Deployment

### Render (Backend)

1. Push code to GitHub
2. Go to [dashboard.render.com](https://dashboard.render.com) → **New Web Service**
3. Connect your repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `CORS_ORIGINS=https://your-frontend.vercel.app`
6. Deploy

### Vercel (Frontend)

1. Go to [vercel.com](https://vercel.com) → **Add New Project**
2. Import your repository
3. Configure:
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Add environment variable: `VITE_API_URL=https://your-backend.onrender.com`
5. Deploy

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `PORT` | `8000` | Server port (Render sets this automatically) |
| `CORS_ORIGINS` | `*` | Comma-separated allowed origins for CORS |
| `LOG_LEVEL` | `info` | Logging level (debug, info, warning, error) |
| `VITE_API_URL` | `''` | Backend URL (set on Vercel; empty = same origin) |

---

## Model Retraining

To retrain the model with new data:

```bash
python retrain.py
```

This reads `train.txt`, preprocesses the data, trains a Logistic Regression model, and saves updated artifacts to `backend/`.

For interactive training with visualizations, open `ModelForge_AI.ipynb` in Jupyter.

---

## Docker

```bash
# Build and run
docker compose up --build
```

The application will be available at `http://localhost:8000`.

---

## License

MIT
