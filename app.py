import os
from venv import create
from flask import Flask, flash, request, redirect, url_for, render_template
from models import Image, db, connect_db
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from utils_helpers import prep_img_for_db, create_temp_folder
from pillow_edit_helpers import convert_sepia, open_image, resize_image, sketchify_image, add_border
from forms import EditImageForm
import urllib.request

#Specify agent for urllib.request, so AWS site does not block access to images
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

load_dotenv()

""" Flask app for Pixly """ #TODO: Should this be in separate config file?
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pixly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ["APP_SECRET_KEY"]
app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

connect_db(app)
db.create_all()

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get('/')
def show_homepage():
    """redirect to home """

    return redirect("/home")

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
    """Renders upload form"""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """Route checks for valid image file. If valid, uploads file to aws and writes metadeta to DB"""

    if 'file' not in request.files:
        flash('No file found')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        resized_image = resize_image(file)
        temp_filepath = f"{app.config['UPLOAD_FOLDER']}/{filename}"

        resized_image.save(temp_filepath)


        image = prep_img_for_db(temp_filepath)

        db.session.add(image)
        db.session.commit()
        os.remove(temp_filepath)

        flash('Image successfully uploaded and displayed below')
        return redirect("/home")

    else:
        flash('Allowed image types are -> jpg, jpeg')
        return redirect(request.url)

@app.route('/<int:id>/edit', methods=['GET', "POST"])
def show_edit_page(id):
    """Handle routing for image editing. Render form for GET. Process edits and save new image on valid submission. """

    image = Image.query.get_or_404(id)
    form = EditImageForm()

    if form.validate_on_submit():

        temp_filepath = f"{app.config['UPLOAD_FOLDER']}/temp.jpg"

        # retrieve aws url and store it on our server temporarily
        urllib.request.urlretrieve(image.url, temp_filepath)

        image = open_image(temp_filepath)

        # image editing
        if form.sketchify.data:
            image = sketchify_image(image)

        if form.sepia.data:
            image = convert_sepia(image)

        if form.frame.data:
            image = add_border(image)

        image.save(temp_filepath)

        new_image = prep_img_for_db(temp_filepath)

        db.session.add(new_image)
        db.session.commit()
        os.remove(temp_filepath)

        return redirect("/home")

    return render_template('edit.html', image=image, form=form)


# TODO: If time, view one photo at a time route
@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
