# AI Amazon Listing Generator

Full-stack web app that generates high-conversion Amazon India listings from optional product details and/or uploaded product images.

## Folder Structure

```text
ai-amazon-listing-tool/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   ├── prompts/
│   │   │   └── templates.py
│   │   ├── routes/
│   │   │   └── listing.py
│   │   └── services/
│   │       ├── listing_service.py
│   │       └── openai_service.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── components/
    │   │   ├── InputField.jsx
    │   │   └── Sidebar.jsx
    │   ├── lib/
    │   │   └── api.js
    │   └── pages/
    │       └── GenerateListingPage.jsx
    ├── package.json
    └── tailwind.config.js
```

## Features

- Optional form fields for product details.
- Multi-image upload (JPG, PNG, WEBP).
- AI vision analysis for missing attributes.
- Data merge layer: user input first, image inference fills blanks.
- Keyword engine (20–30 keywords: primary, long-tail, intent, festival).
- Use-case generation.
- Listing output: title, 5 bullet points, 150–200 word description, backend terms, 5 image caption ideas.
- SaaS-like dashboard layout with sidebar and output actions (copy/edit/download PDF).

## Backend (FastAPI)

### Endpoints

- `GET /health`
- `POST /api/listings/generate` (multipart form-data)
  - `payload`: JSON string for product fields
  - `images`: list of image files

### Run Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
uvicorn app.main:app --reload --port 8000
```

## Frontend (React + Tailwind)

### Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Optional env:

```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:8000
```

## AI Prompt Templates

Prompt templates are modularized in:
- `backend/app/prompts/templates.py`

They cover:
- Vision extraction
- Keyword generation
- Use case generation
- Listing generation

## Scalability Notes

- Service layer (`listing_service.py` + `openai_service.py`) keeps business logic separate from routes.
- Schemas in `schemas.py` make API contracts explicit.
- Easy to add database persistence (Supabase/PostgreSQL) by introducing a repository layer for `Saved Listings`.

## Next Enhancements

- Add authentication + team workspaces.
- Persist generated listings to PostgreSQL/Supabase.
- Implement real PDF rendering (reportlab or frontend html2pdf).
- Add competitor analysis and keyword research backed by dedicated APIs.
