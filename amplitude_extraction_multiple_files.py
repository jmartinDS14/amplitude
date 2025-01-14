#Data Extraction using Amplitude Export API
#https://amplitude.com/docs/apis/analytics/export

import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

api_key=os.getenv('AMP_API_KEY')
api_secret_key=os.getenv('AMP_SECRET_KEY')

start_time='20250101T00'
end_time='20250109T00'

now=datetime.now()
end_time=datetime(now.year,now.month,now.day)
start_time=end_time-timedelta(days=1)
start_time=start_time.strftime("%Y%m%dT%H")
end_time=end_time.strftime("%Y%m%dT%H")

stamp = now.strftime("%Y%m%d_%H%M%S")
file_name = f"data_{stamp}.zip"

url='https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': start_time,
    'end': end_time
}

response = requests.get(url, params=params, auth=(api_key,api_secret_key))

if response.status_code == 200:
    data = response.content
    print('Data retrieved successfully.')
    with open(file_name, 'wb') as file:
        file.write(data)
else:
    print(f'Error {response.status_code}: {response.text}')
