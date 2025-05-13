from fastapi.responses import JSONResponse

from app.configs.get_client import get_clickhouse_client
from app.utils.execute_query_util import execute_query

def remove_data_service(params : dict):
    try:
        date = params['date']
        print(params)
        query = f"""
        ALTER TABLE diamonds DELETE WHERE Upload_Date = '{date}'
                """
    
        return execute_query(query=query,client=get_clickhouse_client())
    except Exception as e:
        return JSONResponse(status_code=500,content={"message" : f"Error in get_InDemand_Data_Details. Error is : {str(e)}."})