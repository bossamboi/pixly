from flask_sqlalchemy import SQLAlchemy

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

    exif_height = db.Column(db.Integer,
                    nullable = False)

    exif_width = db.Column(db.Integer,
                    nullable = False)

    exif_camera_model = db.Column(db.Text,
                    nullable = True)

    url = db.Column(db.Text,
                    nullable = False)

