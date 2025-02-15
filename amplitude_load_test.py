import boto3 # For pushing to AWS S3 
import os       # For file/directory operations
from dotenv import load_dotenv # For reading .env file

load_dotenv()

aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
aws_bucket_name = os.getenv('AWS_BUCKET_NAME')

#print(aws_access_key,aws_secret_key,aws_bucket_name)

s3_client = boto3.client(
 's3',
 aws_access_key_id=aws_access_key,
 aws_secret_access_key=aws_secret_key   
)

s3_client.upload_file('test_upload.json',aws_bucket_name,'python-import/test_upload.json')