from app.utils.execute_query_util import execute_query
from fastapi.responses import JSONResponse
from app.configs.get_client import get_clickhouse_client

def get_Distinct_Filters():
    try:
        query = f"""
                SELECT 
                    groupUniqArray(Shape) AS shape,
                    groupUniqArray(Color) AS color,
                    groupUniqArray(Purity) AS purity,
                    groupUniqArray(Cut) AS cut,
                    groupUniqArray(Polish) AS polish,
                    groupUniqArray(Symm) AS symm,
                    groupUniqArray(Fls) AS fls,
                    groupUniqArray(Culet) AS culet,
                    groupUniqArray(Upload_Date) AS upload_date,
                    groupUniqArray(Country) AS country
                FROM diamonds
                """
        return execute_query(query=query,client=get_clickhouse_client())
    except Exception as e:
        return JSONResponse(status_code=500,content={"message" : f"Error in get_Distinct_Filters. Error is : {str(e)}."})
    
