import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from pillow_edit_helpers import resize_image
from dotenv import load_dotenv
import urllib.request
from models import Image, db, connect_db
from forms import EditImageForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pixly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ["APP_SECRET_KEY"]
app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

load_dotenv()

connect_db(app)
db.create_all()

#Specify agent for urllib.request, so AWS site does not block access to images
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

#Check if image is .jpeg or .jpg
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get('/')
def show_homepage():
    """redirect to home """

    return redirect("/home")


@app.get('/home')
def show_images():
    """Page that shows all images in the database. Can click images to edit
    Can take a 'q' param in querystring to search by camera model name"""

    search = request.args.get('q')

    if not search:
        images = Image.query.all()
    else:
        images = Image.query.filter(
            Image.exif_camera_model.like(f"%{search}%")).all()

    return render_template('home.html', images=images)


@app.get('/upload')
def render_upload_form():
    """Renders upload form"""

    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def process_upload():
    """Route checks for valid image file. If valid, upload file to AWS and
    write metadeta to DB"""

    if 'file' not in request.files:
        flash('No file found', 'warning')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No image selected for uploading', 'warning')
        return redirect(request.url)

    if not allowed_file(file.filename):
        flash('Please submit image type of either .jpg or .jpeg', 'warning')
        return redirect(request.url)

    else:
        #TODO: refactor to include in Image.upload_image? line 84-88
        filename = secure_filename(file.filename)
        resized_image = resize_image(file)
        temp_filepath = f"{app.config['UPLOAD_FOLDER']}/{filename}"

        resized_image.save(temp_filepath)

        Image.upload_image(temp_filepath)

        db.session.commit()

        flash('Image successfully uploaded and displayed below', 'success')
        return redirect("/home")


@app.route('/images/<int:id>/edit', methods=['GET', "POST"])
def show_edit_page(id):
    """Handle routing for image editing. Render form for GET. Process edits and save new image on valid submission. """

    image = Image.query.get_or_404(id)
    form = EditImageForm()

    if form.validate_on_submit():

        temp_filepath = f"{app.config['UPLOAD_FOLDER']}/temp.jpg"

        form_data = {
            "sketchify": form.sketchify.data,
            "sepia": form.sepia.data,
            "frame": form.frame.data,
        }

        # retrieve aws url and store it on our server temporarily
        urllib.request.urlretrieve(image.url, temp_filepath)

        Image.make_edits(temp_filepath, form_data)

        db.session.commit()

        flash('Image successfully edited and displayed below', 'success')
        return redirect("/home")

    return render_template('edit.html', image=image, form=form)


# TODO: If time, view one photo at a time route
@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
