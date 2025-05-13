from app.services.inventory_service import get_Inventory_Details, get_Cheapest_Stone_Details, get_Movement_Insights, get_Detailed_Insights, get_Sold_Stone_Details, get_InDemand_Data_Details

from fastapi import APIRouter, Query

invRouter = APIRouter()

@invRouter.get('/')
def getInventoryDetails(
    shape : str = Query(None),
    color : str = Query(None),
    purity : str = Query(None),
    cut : str = Query(None),
    polish : str = Query(None),
    symm : str = Query(None),
    fls : str = Query(None),
    culet : str = Query(None),
    country : str = Query(None),
    cts : str = Query(None),
    length : str = Query(None),
    width : str = Query(None),
    depth : str = Query(None),
    depth_per : str = Query(None),
    table_per : str = Query(None),
    # limit : int = Query(None),
    d1 : str = Query(None),
    d2 : str = Query(None)
):
    return get_Inventory_Details(locals())

@invRouter.get('/cheapStone')
def getInventoryDetails(
    shape : str = Query(None),
    color : str = Query(None),
    purity : str = Query(None),
    cut : str = Query(None),
    polish : str = Query(None),
    symm : str = Query(None),
    fls : str = Query(None),
    culet : str = Query(None),
    country : str = Query(None),
    cts : str = Query(None),
    length : str = Query(None),
    width : str = Query(None),
    depth : str = Query(None),
    depth_per : str = Query(None),
    table_per : str = Query(None),
    limit : int = Query(None),
    d1 : str = Query(None)
):
    return get_Cheapest_Stone_Details(locals())

@invRouter.get('/movement-insights')
def getMovementInsights(
    shape : str = Query(None),
    color : str = Query(None),
    purity : str = Query(None),
    cut : str = Query(None),
    polish : str = Query(None),
    symm : str = Query(None),
    fls : str = Query(None),
    culet : str = Query(None),
    country : str = Query(None),
    cts : str = Query(None),
    length : str = Query(None),
    width : str = Query(None),
    depth : str = Query(None),
    depth_per : str = Query(None),
    table_per : str = Query(None),
    limit : int = Query(None),
    d1 : str = Query(None),
    d2 : str = Query(None)
):
    return get_Movement_Insights(locals())

@invRouter.get('/detailed-insights')
def getDetailedInsights(
    shape : str = Query(None),
    color : str = Query(None),
    purity : str = Query(None),
    cut : str = Query(None),
    polish : str = Query(None),
    symm : str = Query(None),
    fls : str = Query(None),
    culet : str = Query(None),
    country : str = Query(None),
    cts : str = Query(None),
    length : str = Query(None),
    width : str = Query(None),
    depth : str = Query(None),
    depth_per : str = Query(None),
    table_per : str = Query(None),
    limit : int = Query(None),
    d1 : str = Query(None),
    d2 : str = Query(None),
    company : str = Query(None),
    field : str = Query(None),
):
    return get_Detailed_Insights(params=locals())

@invRouter.get('/sold-stone-details')
def getSoldStoneDetails(
    shape : str = Query(None),
    color : str = Query(None),
    purity : str = Query(None),
    cut : str = Query(None),
    polish : str = Query(None),
    symm : str = Query(None),
    fls : str = Query(None),
    culet : str = Query(None),
    country : str = Query(None),
    cts : str = Query(None),
    length : str = Query(None),
    width : str = Query(None),
    depth : str = Query(None),
    depth_per : str = Query(None),
    table_per : str = Query(None),
    limit : int = Query(None),
    d1 : str = Query(None),
    d2 : str = Query(None),
):
    return get_Sold_Stone_Details(params=locals())

@invRouter.get('/in-demand')
def getInDemandData(
    shape : str = Query(None),
    color : str = Query(None),
    purity : str = Query(None),
    cut : str = Query(None),
    polish : str = Query(None),
    symm : str = Query(None),
    fls : str = Query(None),
    culet : str = Query(None),
    country : str = Query(None),
    cts : str = Query(None),
    length : str = Query(None),
    width : str = Query(None),
    depth : str = Query(None),
    depth_per : str = Query(None),
    table_per : str = Query(None),
    limit : int = Query(None),
    d1 : str = Query(None),
    d2 : str = Query(None),
):
    return get_InDemand_Data_Details(params=locals())