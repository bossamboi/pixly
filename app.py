from flask import Flask, flash, request, redirect, url_for, render_template
from models import Image, db, connect_db
import os
from dotenv import load_dotenv;
from werkzeug.utils import secure_filename
from helpers import extract_exif

load_dotenv()

"Flask app for Pixly"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pixly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ["APP_SECRET_KEY"]
app.config['UPLOAD_FOLDER'] = "./static/uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

connect_db(app)
db.create_all()

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get('/home')
def show_images():
    """Page that shows all images in the database. Can click images to edit

    Can take a 'q' param in querystring to search by that camera name"""

    search = request.args.get('q')

    if not search:
        images = Image.query.all()
    else:
        # TODO: revisit adding additional filters for width/height
        images = Image.query.filter(Image.exif_camera_model.like(f"%{search}%")).all()

    return render_template('home.html', images=images)


@app.get('/upload')
def upload_form():
    return render_template('upload.html');

@app.route('/upload', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file found')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # exif = extract_exif("static/uploads/test.jpg")
        # print("HELLO")
		print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> jpg, jpeg')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
