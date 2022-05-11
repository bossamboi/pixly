import os
from dotenv import load_dotenv
import boto3

load_dotenv()

s3 = boto3.client(
  "s3",
  "us-east-1",
  aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
  aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
)

s3.upload_file("./bg.png", "pixlyrithm25", "eric.png", ExtraArgs = {
    "ACL": "public-read"
})