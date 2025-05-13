from clickhouse_connect.driver.client import Client
from decimal import Decimal
from fastapi.responses import JSONResponse
import math

def safe_float(val):
    try:
        f = float(val)
        return round(f, 2) if math.isfinite(f) else 0.0
    except:
        return val

def execute_query(query: str,client : Client):
    # print(query)
    result = client.query(query)
    rows = result.result_rows
    # print(rows)
    columns = result.column_names
    return JSONResponse(
    content=[
        dict(
            zip(
                columns,
                [
                    safe_float(v) if isinstance(v, (float, Decimal)) else v
                    for v in row
                ]
            )
        )
        for row in rows
    ]
)