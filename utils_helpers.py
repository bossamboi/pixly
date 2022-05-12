import os
from dotenv import load_dotenv
import boto3
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from models import Image as Image_Model

load_dotenv()

AWS_BUCKET_URL = "https://pixlyrithm25.s3.amazonaws.com"

# TODO: fix
def create_temp_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def extract_exif (image_path):
    """ Takes in image path -> exif metadata (width, height, camera_model)"""
    image = Image.open(image_path)

    # read the image data using PIL
    info_dict = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
    }

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


# Uploads to AWS s3 bucket
s3 = boto3.client(
  "s3",
  "us-east-1",
  aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
  aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
)

def prep_img_for_db(path):
    """Takes image from image path, uploads to s3, and creates new Image instance for DB writing"""

    exif = extract_exif(path)

    if "Model" not in exif:
        exif["Model"] = None

    # store image in aws
    aws_filename = str(datetime.now()).replace(" ", "") + ".jpg"
    s3.upload_file(path, "pixlyrithm25", aws_filename, ExtraArgs = {"ACL": "public-read"})

    # create new image instance with desired exif data and aws url
    new_image = Image_Model(exif_height = exif["Image Height"],
                    exif_width = exif["Image Width"],
                    exif_camera_model = exif["Model"],
                    url = f"{AWS_BUCKET_URL}/{aws_filename}")
                    
    return new_image