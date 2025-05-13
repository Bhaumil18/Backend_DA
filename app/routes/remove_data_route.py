from fastapi import APIRouter, Query, Form

from app.services.remove_data_service import remove_data_service

remove_data_router = APIRouter()

@remove_data_router.post('/')
def remove_data_rtr(
    date : str = Form(...)
):
    remove_data_service(params = locals())