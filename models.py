import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, Index
from tsvector import TSVector
from PIL.ExifTags import TAGS
from PIL import Image as PIL_Image
from aws import s3
from datetime import datetime
from pillow_edit_helpers import convert_sepia, sketchify_image, add_border

AWS_BUCKET_URL = "https://pixlyrithm25.s3.amazonaws.com"


db = SQLAlchemy()

def connect_db(app):
    """Connecting to database"""

    db.app = app
    db.init_app(app)


"""Models for Pixly app."""

class Image(db.Model):
    """Image information"""

    __tablename__ = 'images'

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement=True)

    upload_filename = db.Column(db.Text,
                    nullable = False)

    exif_height = db.Column(db.Integer,
                    nullable = False)

    exif_width = db.Column(db.Integer,
                    nullable = False)

    exif_camera_model = db.Column(db.Text,
                    nullable = True)

    url = db.Column(db.Text,
                    nullable = False)

    __ts_vector__ = db.Column(TSVector(),db.Computed(
         "to_tsvector('english', upload_filename || ' ' || exif_height::varchar(255) || ' ' || exif_width::varchar(255) || ' ' || exif_camera_model)",
         persisted=True))

    __table_args__ = (Index('ix_image___ts_vector__',
          __ts_vector__, postgresql_using='gin'),)


    def __repr__(self):
        return f"<Image #{self.id}: {self.upload_filename}, {self.exif_height}px, {self.exif_width}px, {self.exif_camera_model},{self. url}>"

    def extract_exif (image_path):
        """ Takes in image path -> exif metadata (width, height, camera_model)"""

        image = PIL_Image.open(image_path)

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

    @classmethod
    def upload_image(cls, path):
        """Takes image from image path, uploads to s3, and creates new Image instance for DB writing"""
        
        exif = Image.extract_exif(path)

        if "Model" not in exif:
            exif["Model"] = None

        # store image in aws
        aws_filename = str(datetime.now()).replace(" ", "") + ".jpg"
        s3.upload_file(path, "pixlyrithm25", aws_filename, ExtraArgs = {"ACL": "public-read"})

        # create new image instance with desired exif data and aws url
        new_image = Image(upload_filename = exif["Filename"],
                        exif_height = exif["Image Height"],
                        exif_width = exif["Image Width"],
                        exif_camera_model = exif["Model"],
                        url = f"{AWS_BUCKET_URL}/{aws_filename}")

        db.session.add(new_image)
        os.remove(path)

        return new_image


    @classmethod
    def make_edits(cls, path, form_data):
        """Edit image in given path with form_data conditions. Create new instance"""

        image = PIL_Image.open(path)

        if form_data["sketchify"]:
            image = sketchify_image(image)

        if form_data["sepia"]:
            image = convert_sepia(image)

        if form_data["frame"]:
            image = add_border(image)

        image.save(path)

        Image.upload_image(path)