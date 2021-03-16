# Voluum-API
Voluum API documentation can be found [here](https://developers.voluum.com/#!/authentication).

This repository contains the whole ETL pipeline for Voluum data. Starting with making API-requests, thereafter data is transformed and enriched directly in main files. 2 Volum API-request schemas for Python are provided: [Countries Report](https://github.com/MariiaChernysh/Voluum-API/blob/main/LTD_Request.py) and [Campaigns Report](https://github.com/MariiaChernysh/Voluum-API/blob/main/Camp_Land_Off_Request.py).

To write a proper API-request for Voluum data Chrome Developers tools are used. 

![image](https://user-images.githubusercontent.com/8183295/111332712-b114e200-867a-11eb-95b6-6e2980007e0c.png)
(Pic was provided by the Voluum Support Team, many thanks to Katarzyna)

Load the report you need -> visit Network section in Chrome Developers tools -> choose the Name  "report? blah-blah-blah" -> Copy -> Copy as cURL(bash). At this point you'll have the exact request for the report you have created on a dashboard. To convert it to Python request use Postman, this [website](https://curl.trillworks.com/) or any other suitable service.

The provided batch files ([task_LTD.bat](https://github.com/MariiaChernysh/Voluum-API/blob/main/task_LTD.bat) & ...) are responsible for running the scripts and sending the data directly to GCS storage. Afterwards they run the other [BigQuery.py](https://github.com/MariiaChernysh/Voluum-API/edit/main/BigQuery.py) script, which transfers data from GCS to BigQuery. 

Please be aware, that for the proper work of BigQuery.py you need to setup environmental variable with GOOGLE_APPLICATION_CREDENTIALS to get access from the local PC to your project. To create json file with service account key credentials visit: https://cloud.google.com/docs/authentication/production.

