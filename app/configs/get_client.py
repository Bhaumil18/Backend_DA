# # from clickhouse_connect import get_client

# # def get_clickhouse_client():
# #     return get_client(host='localhost',port=8123)

# from clickhouse_connect import get_client


# def get_clickhouse_client():
#     return get_client(host='192.168.0.10',port=8123)

from clickhouse_connect import get_client
import uuid

# client = 

def get_clickhouse_client():
    return get_client(
        host='3.80.227.43',  # Use internal/private IP if possible
        port=8123,
        username='default',
        password='',
        session_id=str(uuid.uuid4()),  # Ensures no session reuse
    )


