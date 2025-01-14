import zipfile  # For handling .zip files
import gzip     # For handling .gz files
import os       # For file/directory operations
import shutil   # For file operations like copying
from pathlib import Path  # For modern path handling
import tempfile # For creating temporary directories
import boto3 # For pushing to AWS S3 
from dotenv import load_dotenv # For reading .env file

load_dotenv()

aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
aws_bucket_name = os.getenv('AWS_BUCKET_NAME')

s3_client = boto3.client(
 's3',
 aws_access_key_id=aws_access_key,
 aws_secret_access_key=aws_secret_key   
)

temp_dir=tempfile.mkdtemp()
zip_path='data.zip'

with zipfile.ZipFile(zip_path,'r') as zip_ref:
    zip_ref.extractall(temp_dir)
    print(f"Extracted {zip_path} to {temp_dir}")

day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
day_path = os.path.join(temp_dir , day_folder)

for root, dirs, files in os.walk(day_path):
    print(f"Current directory: {root}")
    print(f"Subdirectories: {dirs}")
    print(f"Files: {files}")
    for file in files:
        gz_path = os.path.join(root, file)
        json_filename = file[:-3]
        output_path = os.path.join(temp_dir, 'decompressed' , json_filename)

        os.makedirs(os.path.dirname(output_path),exist_ok=True)

        with gzip.open(gz_path,'rb') as gz_file:
            with open(output_path, 'wb') as output_file:
                shutil.copyfileobj(gz_file,output_file)

                aws_file_destination = 'python-import/'+day_folder+'/'+json_filename
                s3_client.upload_file(output_path, aws_bucket_name, aws_file_destination)

shutil.rmtree(temp_dir)
