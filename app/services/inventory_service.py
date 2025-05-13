from app.utils.filters_util import build_filter
from app.utils.execute_query_util import execute_query
from app.configs.get_client import get_clickhouse_client

from fastapi.responses import JSONResponse

def get_Inventory_Details(params : dict):
    try:
        filter_clause = build_filter(params=params)
        d1 = params['d1']
        d2 = params['d2']
        limit = 10
        # if params['limit'] is not None:
        #     limit = params['limit']
        query = f"""
                SELECT 
                    Company,
                    ifNull(COUNT(CASE WHEN Upload_Date = '{d1}' THEN 1 END), 0) AS D1_Pieces,
                    ifNull(COUNT(CASE WHEN Upload_Date = '{d2}' THEN 1 END), 0) AS D2_Pieces,
                    ifNull(
                        COUNT(CASE WHEN Upload_Date = '{d2}' THEN 1 END) - COUNT(CASE WHEN Upload_Date = '{d1}' THEN 1 END),
                        toDecimal64(0, 2)
                    ) AS Diff_Pieces,

                    ifNull(SUM(CASE WHEN Upload_Date = '{d1}' THEN Cts END), toDecimal64(0, 2)) AS D1_Cts,
                    ifNull(SUM(CASE WHEN Upload_Date = '{d2}' THEN Cts END), toDecimal64(0, 2)) AS D2_Cts,
                    ifNull(
                        SUM(CASE WHEN Upload_Date = '{d1}' THEN Cts END) 
                        - 
                        SUM(CASE WHEN Upload_Date = '{d2}' THEN Cts END),
                        toDecimal64(0, 2)
                    ) AS Diff_Cts,

                    ifNull(SUM(CASE WHEN Upload_Date = '{d1}' THEN Net_Value END), toDecimal64(0, 2)) AS D1_Net_Val,
                    ifNull(SUM(CASE WHEN Upload_Date = '{d2}' THEN Net_Value END), toDecimal64(0, 2)) AS D2_Net_Val,
                    ifNull(
                        SUM(CASE WHEN Upload_Date = '{d1}' THEN Net_Value END) 
                        - 
                        SUM(CASE WHEN Upload_Date = '{d2}' THEN Net_Value END),
                        toDecimal64(0, 2)
                    ) AS Diff_Net_Val,
                    
                    ifNull(AVG(CASE WHEN Upload_Date = '{d1}' THEN Net_Value END), toDecimal64(0, 2)) AS D1_Avg_Val,
                    ifNull(AVG(CASE WHEN Upload_Date = '{d2}' THEN Net_Value END), toDecimal64(0, 2)) AS D2_Avg_Val,
                    ifNull(
                        AVG(CASE WHEN Upload_Date = '{d1}' THEN Net_Value END) 
                        - 
                        AVG(CASE WHEN Upload_Date = '{d2}' THEN Net_Value END),
                        toDecimal64(0, 2)
                    ) AS Diff_Avg_Val
                    
                FROM diamonds
                WHERE Upload_Date IN ('{d1}','{d2}')
                    AND {filter_clause} 
                    AND Company != ''
                GROUP BY Company
                ORDER BY Company
                -- LIMIT {limit}
                """
                
        return execute_query(query=query,client=get_clickhouse_client())
    except Exception as e:
        return JSONResponse(status_code=500,content={"message" : f"Error in get_Inventory_Details. Error is : {str(e)}."})
    
def get_Cheapest_Stone_Details(params : dict):
    try:
        filter_clause = build_filter(params=params)
        d1 = params['d1']
        limit = 10
        if params['limit'] is not None:
            limit = params['limit']
        query = f"""
                SELECT 
                    Company,
                    Packet_No,
                    Cert_No,
                    Cts,
                    Shape,
                    Color,
                    Purity,
                    Cut,
                    Polish,
                    Symm,
                    Fls,
                    Length,
                    Width,
                    Depth,
                    Table_,
                    Depth_,
                    Girdle,
                    Girdle_,
                    Culet,
                    Disc_,
                    Net_Rate,
                    Net_Value,
                    Upload_Date
                FROM diamonds
                WHERE {filter_clause} 
                    AND Upload_Date IN ('{d1}')
                    AND Net_Value > 0
                ORDER BY Net_Value ASC
                LIMIT {limit}
                """
                
        return execute_query(query=query,client=get_clickhouse_client())
    except Exception as e:
        return JSONResponse(status_code=500,content={"message" : f"Error in get_Cheapest_Stone_Details. Error is : {str(e)}."})
    
    
def get_Movement_Insights(params : dict):
    try:
        filter_clause = build_filter(params=params)
        d1 = params['d1']
        d2 = params['d2']
        limit = 10
        if params['limit'] is not None:
            limit = params['limit']
        query = f"""
                SELECT 
                    Company, 
                    countIf(has_12 = 1) AS Total_on_D1, 
                    countIf(flag = 'only_first') AS Sold, 
                    countIf(flag = 'both') AS Unsold,
                    countIf(flag = 'only_second') AS New, 
                    countIf(has_21 = 1) AS Total_on_D2, 
                    SUM(CASE WHEN value_21 > value_12 THEN 1 ELSE 0 END) AS Inc_Price, 
                    SUM(CASE WHEN value_21 < value_12 THEN 1 ELSE 0 END) AS Dec_Price,
                    SUM(CASE WHEN value_21 = value_12 THEN 1 ELSE 0 END) AS Same_Price 
                FROM 
                (
                    SELECT 
                        Company, 
                        Cert_No, 
                        max(Upload_Date = '{d1}') AS has_12, 
                        max(Upload_Date = '{d2}') AS has_21, 
                        CASE 
                            WHEN max(Upload_Date = '{d1}') = 1 AND max(Upload_Date = '{d2}') = 1 
                            THEN 'both' 
                            WHEN max(Upload_Date = '{d1}') = 1 
                            THEN 'only_first' 
                            ELSE 'only_second' 
                        END AS flag, 
                        MAX(CASE WHEN Upload_Date = '{d1}' THEN Net_Value END) AS value_12, 
                        MAX(CASE WHEN Upload_Date = '{d2}' THEN Net_Value END) AS value_21 
                    FROM diamonds 
                    WHERE {filter_clause} AND 
                        Cert_No != '' 
                        AND Company != '' 
                        AND Upload_Date IN ('{d1}', '{d2}') 
                    GROUP BY Company, Cert_No
                ) AS result 
                GROUP BY Company
                --LIMIT {limit} 
                """
    
        return execute_query(query=query,client=get_clickhouse_client())
    except Exception as e:
        return JSONResponse(status_code=500,content={"message" : f"Error in get_Movement_Insights. Error is : {str(e)}."})
    
def get_Detailed_Insights(params : dict):
    try:
        filter_clause = build_filter(params=params)
        d1 = params['d1']
        d2 = params['d2']
        field = params['field']
        company = params['company']
        company = company.replace("'", "''")
        limit = 10
        if params['limit'] is not None:
            limit = params['limit']
        if (field == 'Inc_Price'):
            query = f"""
                    SELECT 
                        Company, 
                        Cert_No, 
                        MAX(CASE WHEN Upload_Date = '{d1}' THEN Net_Value END) AS Value_on_D1, 
                        MAX(CASE WHEN Upload_Date = '{d2}' THEN Net_Value END) AS Value_on_D2,
                        Cts,
                        Shape,
                        Color,
                        Purity,
                        Cut,
                        Polish,
                        Symm,
                        Fls,
                        Culet
                    FROM 
                        diamonds 
                    WHERE {filter_clause} 
                    AND Upload_Date IN ('{d1}', '{d2}') 
                        AND Company = '{company}' 
                    GROUP BY 
                        Company, 
                        Cert_No,
                        Cts,
                        Shape,
                        Color,
                        Purity,
                        Cut,
                        Polish,
                        Symm,
                        Fls,
                        Culet
                    HAVING 
                        Value_on_D2 > Value_on_D1
                    -- LIMIT {limit} 
                    """
        elif (field == 'Dec_Price'):
            query = f"""
                    SELECT 
                        Company, 
                        Cert_No, 
                        MAX(CASE WHEN Upload_Date = '{d1}' THEN Net_Value END) AS Value_on_D1, 
                        MAX(CASE WHEN Upload_Date = '{d2}' THEN Net_Value END) AS Value_on_D2,
                         Cts,
                        Shape,
                        Color,
                        Purity,
                        Cut,
                        Polish,
                        Symm,
                        Fls,
                        Culet
                    FROM 
                        diamonds 
                    WHERE {filter_clause} 
                    AND Upload_Date IN ('{d1}', '{d2}') 
                        AND Company = '{company}' 
                    GROUP BY 
                        Company, 
                        Cert_No,
                        Cts,
                        Shape,
                        Color,
                        Purity,
                        Cut,
                        Polish,
                        Symm,
                        Fls,
                        Culet
                    HAVING 
                        Value_on_D2 < Value_on_D1
                    -- LIMIT {limit} 
                    """   
        elif (field == 'New'):
            query = f"""
                    SELECT 
                        Company, 
                        Cert_No,
                        Net_Value, 
                        Cts,
                        Shape,
                        Color,
                        Purity,
                        Cut,
                        Polish,
                        Symm,
                        Fls,
                        Culet
                    FROM diamonds 
                    WHERE {filter_clause} 
                    AND Upload_Date = '{d2}'
                        AND Company = '{company}' 
                    AND Cert_No NOT IN (
                        SELECT 
                            Cert_No 
                        FROM diamonds 
                        WHERE Upload_Date = '{d1}'
                            AND Company = '{company}'
                    )
                    -- LIMIT {limit} 
                    """
        elif (field == 'Sold'):
            query = f"""
                    SELECT 
                        Company, 
                        Cert_No,
                        Net_Value, 
                        Cts,
                        Shape,
                        Color,
                        Purity,
                        Cut,
                        Polish,
                        Symm,
                        Fls,
                        Culet
                    FROM diamonds 
                    WHERE {filter_clause} 
                    AND Upload_Date = '{d1}'
                        AND Company = '{company}' 
                        AND Cert_No NOT IN (
                            SELECT 
                                Cert_No 
                            FROM diamonds 
                            WHERE Upload_Date = '{d2}'
                                AND Company = '{company}'
                        )
                    -- LIMIT {limit} 
                    """ 
        return execute_query(query=query,client=get_clickhouse_client())
        
    except Exception as e:
        return JSONResponse(status_code=500,content={"message" : f"Error in get_Detailed_Insights. Error is : {str(e)}."})
    
def get_Sold_Stone_Details(params : dict):
    try:
        filter_clause = build_filter(params=params)
        d1 = params['d1']
        d2 = params['d2']
        limit = 10
        if params['limit'] is not None:
            limit = params['limit']
        query = f"""
                SELECT 
                    Cert_No,
                    MAX(CASE WHEN Upload_Date = '{d1}' THEN Company END) AS Seller_Company,
                    MAX(CASE WHEN Upload_Date = '{d2}' THEN Company END) AS Buyer_Company,
                    MAX(CASE WHEN Upload_Date = '{d1}' THEN Net_Value END) AS Old_Price,
                    MAX(CASE WHEN Upload_Date = '{d2}' THEN Net_Value END) AS New_Price,
                    Cts,
                    Shape,
                    Color,
                    Purity,
                    Cut,
                    Polish,
                    Symm,
                    Fls,
                    Culet
                FROM diamonds
                PREWHERE 
                    {filter_clause}
                    AND Upload_Date IN ('{d1}', '{d2}') 
                    AND Cert_No != '' 
                    AND Company != ''
                GROUP BY 
                    Cert_No,
                    Cts,
                    Shape,
                    Color,
                    Purity,
                    Cut,
                    Polish,
                    Symm,
                    Fls,
                    Culet
                HAVING 
                    Seller_Company IS NOT NULL 
                    AND Buyer_Company IS NOT NULL 
                    AND Seller_Company != Buyer_Company
                ORDER BY Seller_Company
                LIMIT {limit}
                """
    
        return execute_query(query=query,client=get_clickhouse_client())
    except Exception as e:
        return JSONResponse(status_code=500,content={"message" : f"Error in get_Sold_Stone_Details. Error is : {str(e)}."})
    
    
def get_InDemand_Data_Details(params : dict):
    try:
        filter_clause = build_filter(params=params)
        d1 = params['d1']
        d2 = params['d2']
        limit = 10
        if params['limit'] is not None:
            limit = params['limit']
        query = f"""
                SELECT 
                    Shape,
                    Color,
                    Purity,
                    Cut,
                    Polish,
                    Symm,
                    Fls,

                    countIf(
                        Upload_Date = '{d1}' 
                        AND Cert_No NOT IN (
                            SELECT Cert_No 
                            FROM diamonds 
                            WHERE Upload_Date = '{d2}' AND Company != ''
                        )
                    ) AS Total_Sold,

                    countIf(
                        Upload_Date = '{d2}' 
                        AND Cert_No NOT IN (
                            SELECT Cert_No 
                            FROM diamonds 
                            WHERE Upload_Date = '{d1}' AND Company != ''
                        )
                    ) AS Total_New,

                    countIf(Upload_Date = '{d1}') AS Total_D1_Count,
                    countIf(Upload_Date = '{d2}') AS Total_D2_Count

                FROM diamonds
                PREWHERE Upload_Date IN ('{d1}', '{d2}')
                    AND Company != ''
                    AND Cert_No != ''
                    AND {filter_clause}

                GROUP BY 
                    Shape,
                    Color,
                    Purity,
                    Cut,
                    Polish,
                    Symm,
                    Fls

                ORDER BY Total_Sold DESC
                LIMIT {limit}
                """
    
        return execute_query(query=query,client=get_clickhouse_client())
    except Exception as e:
        return JSONResponse(status_code=500,content={"message" : f"Error in get_InDemand_Data_Details. Error is : {str(e)}."})
    
    
# SELECT 
#     Shape,
#     Color,
#     Purity,
#     Cut,
#     Polish,
#     Symm,
#     Fls,
#     COUNT(*) AS Count
# FROM diamonds 
# WHERE {filter_clause}
# AND Upload_Date = '{d1}'
# AND Company != ''
# AND Cert_No != ''
# AND Cert_No NOT IN (
#     SELECT Cert_No 
#     FROM diamonds 
#     WHERE Upload_Date = '{d2}'
#     AND Company != ''
# )
# GROUP BY 
#     Shape,
#     Color,
#     Purity,
#     Cut,
#     Polish,
#     Symm,
#     Fls
# ORDER BY Count DESC
# LIMIT 10