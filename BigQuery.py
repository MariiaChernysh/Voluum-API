# Source code is taken from here: https://github.com/googleapis/python-bigquery/blob/master/samples/load_table_uri_json.py
import os
from google.cloud import bigquery
#setup environmental variable with GOOGLE_APPLICATION_CREDENTIALS to get access from the local PC to your project
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/.../Credentials.json"
client = bigquery.Client()
#Set table_id to the ID of the table to create.
table_id = "project.dataset.table_id"
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
# set the path to the data in GCS
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

# 
#
# To update data in the already existing BQ table use the code below
#
#

import os
from datetime import timedelta
from datetime import date
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/.../Credentials.json"

from google.cloud.bigquery.client import Client

client = Client()

sql = """
    DELETE FROM `dataset.table_id`
    WHERE date >= '""" + str(start_date) + """'
"""

# Start the query, passing in the extra configuration.
query_job = client.query(sql)  # Make an API request.
query_job.result()  # Wait for the job to complete.

table_id = "project.dataset.table_id"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ],
)

# set the path to the data in GCS
uri = "gs://dataset/sample.json"
load_job = client.load_table_from_uri(
    uri,
    table_id,
    location="US",  # Must match the destination dataset location.
    job_config=job_config,
)
load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)

print("\nLoaded data for {}-{}.{}.{}.".format(start_date.day, date_today.day, date_today.month, date_today.year))
print("\nTotally {} rows.".format(destination_table.num_rows))
