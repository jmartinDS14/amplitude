import zipfile  # For handling .zip files
import gzip     # For handling .gz files
import os       # For file/directory operations
import shutil   # For file operations like copying
from pathlib import Path  # For modern path handling
import tempfile # For creating temporary directories
import boto3 # For pushing to AWS S3 
from dotenv import load_dotenv # For reading .env file

temp_dir=tempfile.mkdtemp()
zip_path='data.zip'

with zipfile.ZipFile(zip_path,'r') as zip_ref:
    zip_ref.extractall(temp_dir)
    print(f"Extracted {zip_path} to {temp_dir}")

#print(os.listdir(temp_dir))

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
