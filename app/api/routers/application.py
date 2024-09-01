from fastapi import APIRouter, Depends

from .depence import get_applicaton_service
from app.api.schemas.application import ApplicationIn
from app.api.services.application import ApplicationService


router_application = APIRouter(tags=["Application"], prefix="/api/v1")



@router_application.post("/application", response_model=ApplicationIn)
async def create_application(application: ApplicationIn, applic_service: ApplicationService = Depends(get_applicaton_service)):
    application = await applic_service.create(application)
    return application

@router_application.get("/application/{user_id}", response_model=ApplicationIn)
async def get_application_info(user_id: str, applic_service: ApplicationService = Depends(get_applicaton_service)):
    application_info = await applic_service.read(user_id)
    return application_info

