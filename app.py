from flask import Flask, render_template, request
from models import Image, db, connect_db
import os
from dotenv import load_dotenv;

load_dotenv()

"Flask app for Pixly"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pixly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ["APP_SECRET_KEY"]

connect_db(app)
db.create_all()


@app.get('/home')
def show_images():
    """Page that shows all images in the database. Can click images to edit"""

    search = request.args.get('q')

    if not search:
        images = Image.query.all()
    else:
        # TODO: revisit adding additional filters for width/height
        images = Image.query.filter(Image.exif_camera_model.like(f"%{search}%")).all()
    
    return render_template('home.html', images=images)