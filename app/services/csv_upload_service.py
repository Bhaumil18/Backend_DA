from fastapi import UploadFile, Form
from datetime import date
from fastapi.responses import JSONResponse
from typing import List
from app.utils.csv_upload_util import csv_upload_util

def csv_upload_service(files : List[UploadFile], upload_date: date):
    try:
        for file in files:
            print("Processing Start for :",file.filename)
            csv_upload_util(file=file,upload_date=upload_date)
            print("Processing Completed for :",file.filename)
        return JSONResponse(content={"message" : "All csvs are uploaded and data inserted successfully...!"})

    except Exception as e:
        return JSONResponse(status_code=500,content={"message" : str(e)})
        