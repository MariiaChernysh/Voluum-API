import os
import json
import requests
import calendar
import pandas as pd
import datetime as dt
from datetime import timedelta
from datetime import date
import calendar
from google.cloud import bigquery

headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Accept': 'application/json',
}
# Receive accessId and accessKey in your voluum account.
data = '{"accessId": "your_access_id_here", "accessKey": "your_access_key_here"}'

# Send HTTP POST request to get a token that lasts for the next 4 hours.
response = requests.post('https://api.voluum.com/auth/access/session', headers=headers, data=data)
print(response.text)

# Save a token for further report requests
ttt = json.loads(response.text)
token = ttt.get('token')

start_date = '2019-01-01'
end_date = '2021-03-16'

date_i = pd.to_datetime(start_date)
# start_month = start_date.month
# start_year = start_date.year

date_i = pd.to_datetime(start_date)

cal_iter = calendar.Calendar()

iter_year = date_i.year
iter_month = date_i.month

stop = False

total_result = []

while not stop:

    cal_iter = calendar.Calendar().itermonthdates(iter_year, iter_month)
    print('\nSending request for: ' + str(iter_year) + ' - ' + str(iter_month))

    for cal_date in cal_iter:
        if cal_date.month == iter_month:
            if cal_date == date.today() - timedelta(days=1):
                headers = {
                    'authority': 'panel-api2.voluum.com',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                    'cwauth-token': token,
                    'sec-ch-ua-mobile': '?0',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                    # 'cwauth-panel-token': 'some_token_id', works without this one
                    'content-type': 'application/json',
                    'accept': 'application/json',
                    'clientid': 'your_client_id_number',
                    'origin': 'https://panel.voluum.com',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://panel.voluum.com/',
                    'accept-language': 'en-US,en;q=0.9,es;q=0.8',
                }

                params = (
                    ('from', str(cal_date) + 'T00:00:00Z'),
                    ('to', str(cal_date + timedelta(days=1)) + 'T00:00:00Z'),
                    ('tz', 'Europe/London'),
                    ('conversionTimeMode', 'CONVERSION'),
                    ('currency', 'USD'),
                    ('sort', 'cost'),
                    ('direction', 'desc'),
                    ('column',
                     ['countryName', 'visits', 'visits', 'clicks', 'clicks', 'customConversions1', 'customConversions2',
                      'revenue',
                      'cost']),
                    ('groupBy', 'country-code'),
                    ('offset', '0'),
                    ('limit', '10000'),
                    ('include', 'ACTIVE'),
                )

                response = requests.get('https://panel-api2.voluum.com/report', headers=headers, params=params)

                data = response.text

                jsn_data = json.loads(data)
                for row in jsn_data['rows']:
                    row['date'] = str(cal_date)

                print('Received the requested LTD-report data for: ' + str(cal_date))

                daily_result = [json.dumps(record) for record in jsn_data['rows']]
                total_result = total_result + daily_result
                stop = True
                break
            headers = {
                'authority': 'panel-api2.voluum.com',
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'cwauth-token': token,
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
                # 'cwauth-panel-token': '80CxSnKulRSW1yigOOrkyH7ublIz02Sf',
                'content-type': 'application/json',
                'accept': 'application/json',
                'clientid': '08148d1f-a3d6-4323-8f64-6080302fc87f',
                'origin': 'https://panel.voluum.com',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://panel.voluum.com/',
                'accept-language': 'en-US,en;q=0.9,es;q=0.8',
            }

            params = (
                ('from', str(cal_date) + 'T00:00:00Z'),
                ('to', str(cal_date + timedelta(days=1)) + 'T00:00:00Z'),
                ('tz', 'Europe/London'),
                ('conversionTimeMode', 'CONVERSION'),
                ('currency', 'USD'),
                ('sort', 'cost'),
                ('direction', 'desc'),
                ('column',
                 ['countryName', 'visits', 'visits', 'clicks', 'clicks', 'customConversions1', 'customConversions2',
                  'revenue',
                  'cost']),
                ('groupBy', 'country-code'),
                ('offset', '0'),
                ('limit', '10000'),
                ('include', 'ACTIVE'),
            )

            response = requests.get('https://panel-api2.voluum.com/report', headers=headers, params=params)

            data = response.text

            jsn_data = json.loads(data)
            for row in jsn_data['rows']:
                row['date'] = str(cal_date)

            print('Received the requested LTD-report data for: ' + str(cal_date))

            daily_result = [json.dumps(record) for record in jsn_data['rows']]
            total_result = total_result + daily_result
        elif cal_date.month == iter_month + 1:
            break

    if iter_month == 12:
        iter_year = iter_year + 1
        iter_month = 0

    iter_month = iter_month + 1

print('The request is 100% done')
with open("sample.json", "w") as outfile:
    for i in total_result:
        outfile.write(i+'\n')