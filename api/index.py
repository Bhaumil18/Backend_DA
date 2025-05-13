from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.csv_upload_route import csv_upload_router
from app.routes.filters_route import filterRouter
from app.routes.inventory_router import invRouter
from app.routes.remove_data_route import remove_data_router

from app.services.filters_service import get_Distinct_Filters

app = FastAPI(title="Analysis App")


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)

@app.get("/")
def read_root():
    return {"msg": "FastAPI is running on Vercel!"}

@app.get("/distinct")
def getGilter():
    return get_Distinct_Filters()


app.include_router(csv_upload_router, prefix="/upload")
app.include_router(filterRouter, prefix='/details')
app.include_router(invRouter, prefix='/inventory')
app.include_router(remove_data_router,prefix='/delete')
