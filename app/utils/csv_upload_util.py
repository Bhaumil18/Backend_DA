# from fastapi import UploadFile
# import io
# import csv
# import subprocess
# from datetime import date
# from app.configs.get_client import get_clickhouse_client

# def csv_upload_util(file: UploadFile, upload_date: date):
#     input_stream = io.StringIO(file.file.read().decode("ISO-8859-1"))
#     output_stream = io.StringIO()

#     reader = csv.reader(input_stream)
#     writer = csv.writer(output_stream)

#     header = next(reader, None)
#     if header:
#         # Append "Upload_Date" to header (57th column)
#         header.append("Upload_Date")
#         writer.writerow(header)

#     # Skip second row
#     next(reader, None)

#     for row in reader:
#         if len(row) == 56:  # expected CSV rows
#             row.append(str(upload_date))  # Add Upload_Date as 57th column
#             writer.writerow(row)

#     output_stream.seek(0)
#     csv_data_bytes = output_stream.getvalue().encode("ISO-8859-1")

#     client = get_clickhouse_client()
#     client.insert_csv("diamonds", output_stream.getvalue())
#     # subprocess.run([
#     #     "wsl", "clickhouse-client",
#     #     "--query=INSERT INTO diamonds FORMAT CSVWithNames"
#     # ], input=csv_data_bytes)


# import io
# import csv
# import requests
# from datetime import date
# from fastapi import UploadFile

# def csv_upload_util(file: UploadFile, upload_date: date):
#     # Read CSV file in memory
#     input_stream = io.StringIO(file.file.read().decode("ISO-8859-1"))
#     reader = csv.reader(input_stream)

#     # Prepare the header and append Upload_Date
#     header = next(reader, None)
#     if header:
#         header.append("Upload_Date")  # Add Upload_Date as new column

#     next(reader, None)  # Skip second row

#     rows = []
#     for row in reader:
#         if len(row) == 56:
#             row.append(str(upload_date))
#             rows.append(row)

#     # Convert the data into CSV format
#     output_stream = io.StringIO()
#     writer = csv.writer(output_stream)
#     writer.writerow(header)
#     writer.writerows(rows)

#     # Prepare the data for HTTP request
#     csv_data = output_stream.getvalue().encode("ISO-8859-1")

#     # Send a POST request to ClickHouse
#     url = "http://44.220.151.213:8123"  # Replace with your ClickHouse HTTP endpoint
#     headers = {'Content-Type': 'application/csv'}
#     query = "INSERT INTO diamonds FORMAT CSVWithNames"  # The ClickHouse query

#     response = requests.post(url, headers=headers, data=csv_data, params={'query': query})

#     # Check response
#     if response.status_code == 200:
#         return {"message": "CSV data successfully inserted into ClickHouse!"}
#     else:
#         return {"message": f"Error: {response.text}"}

import io
import csv
import requests
from datetime import date
from fastapi import UploadFile

BATCH_SIZE = 20000  # You can tune this for performance

def csv_upload_util(file: UploadFile, upload_date: date):
    input_stream = io.StringIO(file.file.read().decode("ISO-8859-1"))
    reader = csv.reader(input_stream)

    header = next(reader, None)
    if header:
        header.append("Upload_Date")  # Add Upload_Date as new column

    next(reader, None)  # Skip second row

    url = "http://3.80.227.43:8123"
    headers = {'Content-Type': 'text/csv'}
    query = "INSERT INTO diamonds FORMAT CSVWithNames"

    batch = []
    total_inserted = 0

    for row in reader:
        if len(row) == 56:
            row.append(str(upload_date))
            batch.append(row)

        if len(batch) == BATCH_SIZE:
            success = send_batch(batch, header, url, headers, query)
            if not success:
                return {"message": f"Error uploading batch after {total_inserted} rows"}
            total_inserted += len(batch)
            batch = []

    # Send remaining rows
    if batch:
        success = send_batch(batch, header, url, headers, query)
        if not success:
            return {"message": f"Error uploading final batch after {total_inserted} rows"}
        total_inserted += len(batch)

    return {"message": f"Successfully inserted {total_inserted} rows into ClickHouse"}

def send_batch(batch, header, url, headers, query):
    try:
        output_stream = io.StringIO()
        writer = csv.writer(output_stream)
        writer.writerow(header)
        writer.writerows(batch)

        response = requests.post(
            url,
            headers=headers,
            data=output_stream.getvalue(),
            params={'query': query},
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Exception during batch upload: {e}")
        return False

