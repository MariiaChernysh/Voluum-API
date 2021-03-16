# Source code is taken from here: https://github.com/googleapis/python-bigquery/blob/master/samples/load_table_uri_json.py
from google.cloud import bigquery

client = bigquery.Client()
#Set table_id to the ID of the table to create.
table_id = "marchs-reports.March.LTD_Report"
job_config = bigquery.LoadJobConfig(
    schema=[
            bigquery.SchemaField("clicks", "INTEGER"),
            bigquery.SchemaField("cost", "FLOAT"),
            bigquery.SchemaField("countryCode", "STRING"),
            bigquery.SchemaField("countryName", "STRING"),
            bigquery.SchemaField("customConversions1", "INTEGER"),
            bigquery.SchemaField("customConversions2", "INTEGER"),
            bigquery.SchemaField("revenue", "FLOAT"),
            bigquery.SchemaField("visits", "INTEGER"),
            bigquery.SchemaField("date", "DATE"),
        ],
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )
# set the pth to the data in GCS
uri = "gs://.../sample.json"
load_job = client.load_table_from_uri(
    uri,
    table_id,
    location="US",  # Must match the destination dataset location.
    job_config=job_config,
)
load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))
