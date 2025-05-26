# Sentiment-Feedback App

## Overview

A full-stack application that automatically analyzes user feedback by:

- Detecting sentiment & key phrases with **Azure Cognitive Services**
- Generating AI responses with **OpenAI GPT-3.5**
- Storing all data in **PostgreSQL**
- Optionally converting responses to audio via **Azure Text-to-Speech**

## Tech Stack

| Component | Technologies |
|-----------|--------------|
| **Frontend** | React 19 · Vite · Material-UI |
| **Backend** | Python 3.11 · Flask |
| **Services** | Azure Cognitive Services · OpenAI · PostgreSQL |

---

## Quick Start Guide

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Node.js | ≥ 18 |
| npm | ≥ 9 |
| Python | ≥ 3.10 |
| PostgreSQL | ≥ 13 |
| Azure Cognitive Services | Text Analytics & Speech |
| OpenAI | API key |

### Installation

```
git clone <YOUR-REPO-URL> sentiment-feedback
cd sentiment-feedback
```

### Backend Setup

```
cd backend
python -m venv venv           # Windows: py -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # Configure with your API keys
flask --app app run           # Runs on http://127.0.0.1:5000
```

#### Environment Configuration

Create a `.env` file with the following variables:

```
AZURE_ENDPOINT=
AZURE_API_KEY=
AZURE_SPEECH_KEY=
AZURE_SPEECH_REGION=
DATABASE_URL=postgresql://user:pass@host:port/db
OPENAI_API_KEY=
```

#### Database Initialization

Execute the following SQL once to create the required table:

```
CREATE TABLE IF NOT EXISTS sentiment_analysis (
  id              SERIAL PRIMARY KEY,
  feedback        TEXT        NOT NULL,
  analysis        JSONB,
  audio_file_path TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Frontend Setup

```
cd ../frontend
npm install
npm run dev         # Runs on http://localhost:5173
```

> **Note:** The React app expects the API at `http://127.0.0.1:5000`. To change this, update the `API_URL` constants in `src/components/SubmitFeedback.jsx` and `ViewFeedback.jsx`.

## Project Structure

```
backend/
├── app.py                             # Flask application entry point
├── routes/azure_routes.py             # API route definitions
├── services/
│   ├── azure_cognitive.py             # Sentiment analysis logic
│   └── open_ai_service.py             # GPT integration
├── repository/sentiment_repository.py # Database operations
├── db.py                              # Database connection
└── requirements.txt                   # Python dependencies

frontend/
├── src/
│   ├── components/
│   │   ├── SubmitFeedback.jsx         # Feedback submission form
│   │   └── ViewFeedback.jsx           # Feedback history display
│   ├── App.jsx                        # Main React component
│   └── main.jsx                       # Application entry point
└── vite.config.js                     # Vite configuration
```

## API Reference

| Method | Endpoint | Request Body / Query | Response (200) |
|--------|----------|---------------------|----------------|
| POST | `/analyze` | `{ "content": "Great job!" }` | AI reply + sentiment analysis JSON |
| GET | `/feedbacks?limit=20&offset=0` | - | List of analysis results |
| GET | `/output_audio/<filename>` | - | Audio/mpeg stream |

Error responses follow the format: `{ "error": "message" }`.

## Scripts

### Frontend

| Command | Description |
|---------|-------------|
| `npm run dev` | Start Vite development server |
| `npm run build` | Create production build in `dist/` |
| `npm run lint` | Run ESLint |

### Backend

| Command | Description |
|---------|-------------|
| `make run` or `flask --app app run` | Start Flask server |
| `make install` | Install Python dependencies |

## Deployment Guidelines

### Backend
Serve with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app()'
```

### Frontend
Run `npm run build` and serve the `frontend/dist` directory using Nginx, Netlify, Vercel, or similar.

### Security Considerations
- Store all API keys and credentials as environment variables
- Never commit sensitive information to Git
- CORS: Use wildcard (`*`) for development only; restrict origins in production
