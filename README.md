# Sentiment-Feedback App

A full-stack application that lets users enter free-text feedback, automatically:

1. Detects sentiment & key phrases with **Azure Cognitive Services**  
2. Generates a short AI reply with **OpenAI GPT-3.5**  
3. Stores everything in **PostgreSQL**  
4. (Optional) Returns an MP3 reply via Azure Text-to-Speech

| Folder | Stack | Purpose |
| ------ | ----- | ------- |
| **`frontend/`** | React 19 · Vite · MUI | Collect feedback & list past analyses |
| **`backend/`**  | Python 3.11 · Flask | Sentiment, GPT reply, TTS, persistence |

> **No CI/CD yet.**  
> The roadmap (bottom) shows planned automation.

---

## Quick Start (local)

### Requirements

| Tool | Version |
|------|---------|
| Node | ≥ 18 |
| npm  | ≥ 9 |
| Python | ≥ 3.10 |
| PostgreSQL | 13 + |
| Azure Cognitive Services | Text-Analytics & Speech |
| OpenAI | API key |

```bash
git clone <YOUR-REPO-URL> sentiment-feedback
cd sentiment-feedback
1 · Backend
bash
Copy
Edit
cd backend
python -m venv venv           # Windows: py -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # add your own secrets
flask --app app run           # http://127.0.0.1:5000
backend/.env.example

dotenv
Copy
Edit
AZURE_ENDPOINT=
AZURE_API_KEY=
AZURE_SPEECH_KEY=
AZURE_SPEECH_REGION=
DATABASE_URL=postgresql://user:pass@host:port/db
OPENAI_API_KEY=
Create the table once:

sql
Copy
Edit
CREATE TABLE IF NOT EXISTS sentiment_analysis (
  id              SERIAL PRIMARY KEY,
  feedback        TEXT        NOT NULL,
  analysis        JSONB,
  audio_file_path TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
2 · Frontend
bash
Copy
Edit
cd ../frontend
npm install
npm run dev         # http://localhost:5173
The React app expects the API at http://127.0.0.1:5000.
Change API_URL constants in src/components/SubmitFeedback.jsx and ViewFeedback.jsx if necessary.

Project Structure
bash
Copy
Edit
backend/
├── app.py
├── routes/azure_routes.py
├── services/
│   ├── azure_cognitive.py
│   └── open_ai_service.py
├── repository/sentiment_repository.py
├── db.py
└── requirements.txt

frontend/
├── src/
│   ├── components/
│   │   ├── SubmitFeedback.jsx
│   │   └── ViewFeedback.jsx
│   ├── App.jsx
│   └── main.jsx
└── vite.config.js
API Endpoints
Verb	Endpoint	Body / Query	Response (200)
POST	/analyze	{ "content": "Great job!" }	AI reply + sentiment JSON
GET	/feedbacks?limit=20&offset=0	–	List of analyses
GET	/output_audio/<filename>	–	audio/mpeg stream

Error format: { "error": "message" }.

Scripts
Frontend
Command	Action
npm run dev	Start Vite dev server
npm run build	Production build to dist/
npm run lint	ESLint

Backend
Command	Action
make run or flask --app app run	Start Flask
make install	Install Python dependencies

Deployment Notes
Backend: Serve with Gunicorn →
gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app()'

Frontend: npm run build and serve frontend/dist with Nginx, Netlify, Vercel, etc.

Secrets: keep all keys in environment variables—never commit to Git.

CORS: default wildcard in dev; restrict origins in prod.
