import os
import boto3

# Uploads to AWS s3 bucket TODO: separte out into own aws file
s3 = boto3.client(
  "s3",
  "us-east-1",
  aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
  aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
)