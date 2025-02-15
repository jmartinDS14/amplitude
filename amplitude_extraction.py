#Data Extraction using Amplitude Export API
#https://amplitude.com/docs/apis/analytics/export

import os
import requests
from dotenv import load_dotenv
import boto3
import re
from datetime import datetime, timedelta

load_dotenv()

aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
aws_bucket_name = os.getenv('AWS_BUCKET_NAME')

s3_client = boto3.client(
 's3',
 aws_access_key_id=aws_access_key,
 aws_secret_access_key=aws_secret_key   
)

response = s3_client.list_objects_v2(Bucket=aws_bucket_name, Prefix='python-import/100011471/')

file_names = [os.path.basename(obj['Key']) for obj in response.get('Contents', [])]

date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
dates = [datetime.strptime(date_pattern.search(name).group(), '%Y-%m-%d') 
         for name in file_names if date_pattern.search(name)]

max_date = max(dates)
next_day = max_date + timedelta(days=1)
start_time = next_day.strftime('%Y%m%dT%H')

today = datetime.today()
today = today.replace(hour=0, minute=0, second=0, microsecond=0)
end_time = today.strftime('%Y%m%dT%H')

api_key=os.getenv('AMP_API_KEY')
api_secret_key=os.getenv('AMP_SECRET_KEY')


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
