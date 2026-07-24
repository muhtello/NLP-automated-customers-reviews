# Automated Customer Reviews

NLP-powered system for Amazon product reviews: sentiment classification, product category clustering, and AI-generated category summaries, served through a FastAPI backend and a Next.js dashboard.

## Live App

[https://signalnlpreview.vercel.app/](https://signalnlpreview.vercel.app/)

## Project Structure

- **`ml/`** — data cleaning + model training (sentiment, clustering, summarization). Run locally to (re)train the models:
  ```bash
  cd ml
  venv\Scripts\Activate.ps1
  python run.py
  ```
  This takes a while depending on your PC (trains a transformer model) and writes results to `ml/outputs/`.
- **`api/`** — FastAPI backend that loads `ml/outputs/` artifacts and serves predictions/summaries to the frontend.
- **`web/`** — Next.js dashboard (frontend) that consumes the API.

## Run Locally

**Terminal 1 — API**
```bash
cd api
.venv\Scripts\Activate.ps1
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 — Web**
```bash
cd web
npm run dev
```

Then open [http://localhost:3000](http://localhost:3000).
