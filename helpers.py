import os
from dotenv import load_dotenv
import boto3
from PIL import Image
from PIL.ExifTags import TAGS

load_dotenv()

# path to the image or video
# imagename = "images/bg.jpg"

# takes in image path -> exif metadata (width, height, camera_model)
def extract_exif (image_path):
    image = Image.open(image_path)

    # read the image data using PIL
    info_dict = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
    }

    # for label,value in info_dict.items():
    #     print(f"{label}: {value}")

    # extract EXIF data
    exifdata = image.getexif()

    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        info_dict[tag]=data
    return info_dict


s3 = boto3.client(
  "s3",
  "us-east-1",
  aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
  aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
)

# s3.upload_file("./bg.png", "pixlyrithm25", "eric.png", ExtraArgs = {
#     "ACL": "public-read"
# })