from fastapi import APIRouter, Query
from app.services.filters_service import get_Distinct_Filters

filterRouter = APIRouter()

@filterRouter.get("/distinct")
def getDistinctInFilters():
    return get_Distinct_Filters()
