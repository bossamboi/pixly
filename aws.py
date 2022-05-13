import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Upload to AWS s3 bucket 
s3 = boto3.client(
  "s3",
  "us-east-1",
  aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
  aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
)