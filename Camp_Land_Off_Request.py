import json
import requests
#CONST; TODO: auto-dates
date='2021-03-14'
date1='2021-03-15'

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
token=ttt.get('token')

# To write a proper request use Chrome Developers tools. Load the report you need -> visit Network section in Chrome Developers tools -> choose the Name  "report? blah-blah-blah"
#-> Copy -> Copy as cURL(bash). At this point you'll have the exact request for the report you have created on a dashboard. To convert it to Python request use Postman or 
#https://curl.trillworks.com/ or any other suitable service
headers = {
    'authority': 'panel-api2.voluum.com',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'cwauth-token': token, # change to token variable
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    #'cwauth-panel-token': 'some_other_token_here', # it works just fine without this one
    'content-type': 'application/json',
    'accept': 'application/json',
    'clientid': 'your_client_id_here',
    'origin': 'https://panel.voluum.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://panel.voluum.com/',
    'accept-language': 'uk-UA,uk;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6,es;q=0.5',
}

params = (
    ('from', date+'T00:00:00Z'), #add auto dates
    ('to', date1+'T00:00:00Z'), #add auto dates
    ('tz', 'Europe/London'),
    ('conversionTimeMode', 'CONVERSION'),
    ('currency', 'USD'),
    ('sort', 'customConversions2'),
    ('direction', 'desc'),
    ('column', ['campaignName', 'landerName', 'offerName', 'campaignNotes', 'externalStatus', 'campaignUrl', 'visits', 'suspiciousVisitsPercentage', 'visits', 'suspiciousVisits', 'clicks', 'suspiciousClicksPercentage', 'clicks', 'suspiciousClicks', 'conversions', 'customConversions1', 'customConversions2', 'revenue', 'cost', 'costSources', 'profit', 'ctr', 'cr', 'roi', 'ecpm', 'ecpa', 'CTL', 'transitivePause', 'cpm', 'campaignIdMarker', 'actions', 'type', 'readOnly', 'deleted', 'campaignType', 'isOptimizationEnabled', 'externalCampaignId', 'isDsp', 'landerUrl', 'landerNotes', 'landerWorkspaceName', 'offerUrl', 'offerNotes']),
    ('groupBy', 'campaign'),
    ('offset', '0'),
    ('limit', '100'),
    ('include', 'TRAFFIC'),
)

data100500 = requests.get('https://panel-api2.voluum.com/report', headers=headers, params=params)
