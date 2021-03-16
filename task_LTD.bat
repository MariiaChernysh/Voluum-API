cd C:\Users\...\Volum-API
#Running code locally
python LTD_Request.py
#Transferring data from PC to GCS
gsutil -m cp -r "C:/Users/.../Voluum-API/sample.json" gs://.../sample.json
#Transferring data from GCS to BigQuery
python BigQuery.py
