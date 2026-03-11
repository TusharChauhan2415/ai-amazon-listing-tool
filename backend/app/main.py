from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.listing import router as listing_router

app = FastAPI(title="AI Amazon Listing Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listing_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
