from app import app
from models import db, Image

db.drop_all()
db.create_all()

i1 = Image(
    exif_height=500,
    exif_width=700,
    exif_camera_model="iPhone 12 Pro",
    url="https://images.pexels.com/photos/2071873/pexels-photo-2071873.jpeg?cs=srgb&dl=pexels-wojciech-kumpicki-2071873.jpg&fm=jpg"
)

i2 = Image(
    exif_height=1000,
    exif_width=1200,
    exif_camera_model=None,
    url="https://pixlyrithm25.s3.amazonaws.com/eric.png"
)

db.session.add_all([i1, i2])
db.session.commit()
