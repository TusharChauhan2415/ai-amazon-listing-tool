import json
from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas import GenerationResult, ProductInput
from app.services.listing_service import ListingService

router = APIRouter(prefix="/api/listings", tags=["Listings"])
service = ListingService()


@router.post("/generate", response_model=GenerationResult)
async def generate_listing(
    payload: str = Form("{}"),
    images: Optional[List[UploadFile]] = File(default=None),
):
    try:
        data = json.loads(payload)
        product_input = ProductInput(**data)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid payload: {exc}") from exc

    blobs: List[bytes] = []
    if images:
        for image in images:
            if image.content_type not in {"image/jpeg", "image/png", "image/webp"}:
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {image.content_type}")
            blobs.append(await image.read())

    return await service.generate(product_input, blobs)
