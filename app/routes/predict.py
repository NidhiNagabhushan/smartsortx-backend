"""
POST /predict — Upload a waste image and get AI classification.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ai.classifier import classify_image
from app.models.schemas import PredictionResponse
import uuid
import os

router = APIRouter()

# Only allow image files
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE_MB   = 10


@router.post(
    "/",
    response_model=PredictionResponse,
    summary="Classify a waste image",
    description="Upload a waste photo and get disposal guidance + EcoPoints.",
)
async def predict(image: UploadFile = File(..., description="Waste image (JPEG/PNG/WEBP)")):

    # ── Validate file type ─────────────────────────────────────────────────────
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{image.content_type}'. Please use JPEG, PNG or WEBP."
        )

    # ── Read image bytes ───────────────────────────────────────────────────────
    image_bytes = await image.read()

    # ── Validate file size ─────────────────────────────────────────────────────
    if len(image_bytes) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {MAX_SIZE_MB}MB."
        )

    # ── Save uploaded image to uploads/ folder ─────────────────────────────────
    os.makedirs("uploads", exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{image.filename}"
    filepath = os.path.join("uploads", filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes)

    # ── Run AI classification ──────────────────────────────────────────────────
    try:
        result = await classify_image(image_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Classification failed: {str(e)}"
        )

    # ── Return prediction response ─────────────────────────────────────────────
    return PredictionResponse(
        item         = result["item"],
        category     = result["category"],
        bin          = result["bin"],
        recyclable   = result["recyclable"],
        hazard_level = result["hazard_level"],
        eco_points   = result["eco_points"],
        confidence   = result["confidence"],
        impact       = result["impact"],
        eco_tip      = result["eco_tip"],
    )