from app import app
from models import db, Image

db.drop_all()
db.create_all()

i1 = Image(
    exif_height=500,
    exif_width=700,
    exif_camera_model="iPhone 12 Pro",
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1120%3A55%3A21.605527.jpg"
)

i2 = Image(
    exif_height=1000,
    exif_width=1200,
    exif_camera_model=None,
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1120%3A55%3A29.730320.jpg"
)

i3 = Image(
    exif_height=1000,
    exif_width=1200,
    exif_camera_model=None,
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1120%3A58%3A15.648381.jpg"
)

i4 = Image(
    exif_height=1000,
    exif_width=1200,
    exif_camera_model=None,
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1121%3A01%3A49.232730.jpg"
)

i5 = Image(
    exif_height=1000,
    exif_width=1200,
    exif_camera_model=None,
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1121%3A02%3A10.172556.jpg"
)

i6 = Image(
    exif_height=1000,
    exif_width=1200,
    exif_camera_model=None,
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1121%3A08%3A22.723306.jpg"
)

i7 = Image(
    exif_height=1000,
    exif_width=1200,
    exif_camera_model=None,
    url="https://pixlyrithm25.s3.amazonaws.com/2022-05-1121%3A09%3A59.553793.jpg"
)


db.session.add_all([i1, i2, i3, i4, i5, i6, i7])
db.session.commit()
