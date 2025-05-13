from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from app.services.csv_upload_service import csv_upload_service
from datetime import date

csv_upload_router = APIRouter()

@csv_upload_router.post("/csvs")
def csv_upload(files : List[UploadFile] = File(...), upload_date: date = Form(...)):
    return csv_upload_service(files=files,upload_date=upload_date)
