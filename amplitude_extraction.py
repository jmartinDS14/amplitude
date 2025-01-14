#Data Extraction using Amplitude Export API
#https://amplitude.com/docs/apis/analytics/export

import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv('AMP_API_KEY')
api_secret_key=os.getenv('AMP_SECRET_KEY')

start_time='20250101T00'
end_time='20250114T00'

url='https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': start_time,
    'end': end_time
}

response = requests.get(url, params=params, auth=(api_key,api_secret_key))

if response.status_code == 200:
    data = response.content
    print('Data retrieved successfully.')
    with open('data.zip', 'wb') as file:
        file.write(data)
else:
    print(f'Error {response.status_code}: {response.text}')
