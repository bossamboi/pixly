from app import app
from models import db, Image

db.drop_all()
db.create_all()

i1 = Image(
    upload_filename="cat.jpg",
    exif_height=500,
    exif_width=700,
    exif_camera_model="iPhone 12 Pro",
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1215%3A40%3A47.389471.jpg"

)

i2 = Image(
    upload_filename="catty.jpg",
    exif_height=1000,
    exif_width=1200,
    exif_camera_model="iPhone 12 Pro",
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1215%3A40%3A58.761935.jpg"
)

i3 = Image(
    upload_filename="cats.jpg",
    exif_height=1000,
    exif_width=1200,
    exif_camera_model="iPad Pro",
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1215%3A41%3A06.324822.jpg"
)

i4 = Image(
    upload_filename="kitten.jpg",
    exif_height=1000,
    exif_width=1200,
    exif_camera_model="Samsung Galaxy S22",
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1215%3A41%3A15.567303.jpg"
)

i5 = Image(
    upload_filename="kittens.jpg",
    exif_height=1000,
    exif_width=1200,
    exif_camera_model="Google Pixel 6 Pro",
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1215%3A41%3A26.104517.jpg"
)

i6 = Image(
    upload_filename="kits.jpg",
    exif_height=1000,
    exif_width=1200,
    exif_camera_model="Samsung Galaxy S22",
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1215%3A41%3A33.120265.jpg"
)

i7 = Image(
    upload_filename="kitte.jpg",
    exif_height=1000,
    exif_width=1200,
    exif_camera_model=None,
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1215%3A41%3A41.362821.jpg"
)


db.session.add_all([i1, i2, i3, i4, i5, i6, i7])
db.session.commit()
