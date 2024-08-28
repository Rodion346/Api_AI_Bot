from fastapi import APIRouter, Depends, UploadFile, File, Form

from .depence import get_user_service
from app.api.schemas.img_generate import ClotIn
from app.api.services.user import UserService
import requests

router_clot = APIRouter(tags=["Clothoff"], prefix="/api/v1")




@router_clot.post("/generate_image_clothoff")
async def handle_webhook(
    image: UploadFile = File(...),
    age: str = Form(...),
    breast_size: str = Form(...),
    body_type: str = Form(...),
    butt_size: str = Form(...),
    pose: str = Form(...),
    cloth: str = Form(...),
    id_gen: str = Form(...),
    webhook: str = Form(...),# Default parameter comes last
):
    url = "https://public-api.clothoff.io/undress"

    files = {"image": (image.filename, await image.read())}
    payload = {
        "age": age,
        "breast_size": breast_size,
        "body_type": body_type,
        "butt_size": butt_size,
        "cloth": cloth,
        "pose": pose,
        "id_gen": id_gen,
        "webhook": webhook
    }
    headers = {
        "accept": "application/json",
        "x-api-key": "f5406795d2baab5be031ca82f3ebe1f50da871c3"
    }

    requests.post(url, data=payload, files=files, headers=headers)
