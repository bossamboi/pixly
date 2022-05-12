Pix.ly

UI

First Visit

1. User can upload photos (upload form) to AWS (Metadata is stored in Database)
2. User can view and select ANY photos stored in system.
3. Users can search image data with EXIF fields (PSQL full-text search)
4. User can edit: Color -> Sepia -> B&W

After Editing, Options:

1. Download
2. Save the File to AWS
3. Cancel

REACT - COMPONENTS

1. APP
2. NAVBAR - Home, Search Photos, View Random Photos, Upload Photos
3. UPLOAD PHOTO FORM? (look into file upload AWS, strip the metadata to put in database)
4. PHOTO DISPLAY PAGE FILLED (infinite scroll, pagination)
5. FOOTER

PYTHON - BACKEND

1. Manipulate the photos?
2. Strip Metadata to store in DB
3. Use PILLOW or alt for image processing abilities (https://pypi.org/project/Pillow/)(https://www.alixaprodev.com/2021/10/python-libraries-for-image-processing.html)

RESTFUL API: CREATE READ UPDATE DELETE -- SQL
post / get / put:patch / delete

POST /images {id, url}
store photo in backend (temp) -- address reversion (CANCEL)
strip metadata from photo(?)
upload to AWS script, return URL back
store it as new record on DB.
GET ALL /images [{id, url}, {id, url}...]
grab all url in DB and feed into front-end
GET filtered /images [{id, url}, {id, url}...]
grab all url in DB by query parameters and feed into front-end
GET ONE /images/<int:id> {id, url}
grab one url in DB and feed into front-end
DELETE /images/<int:id> {id, message}
grab one url
script to delete in AWS
EDIT:
grab one url in DB
download a copy ?
edit photo with PILLOW python library
POST new editted photo

<!-- ** OPTIONAL - PUT/PATCH   /images/<int:id> -- add edited photo as separate file? (PUT? - optional)
    grab one url in DB
    download a copy ?
    edit photo with PILLOW python library  -->

const AWS_BASE_URL = https://pixlyrithm25.s3.amazonaws.com/
DATABASE

PHOTO_ID | EXIF WIDTH | EXIF HEIGHT | Model | IMG_URL_AWS
a.jpeg 500 800 iPhone 12 Pro aws.com...

EDIT FUNCTIONS:

COLOR:
b/w: https://holypython.com/python-pil-tutorial/how-to-convert-an-image-to-black-white-in-python-pil/
sepia: https://www.codementor.io/@isaib.cicourel/intermediate-image-filters-mj6y7abx4

Re-Size: https://www.tutorialspoint.com/python_pillow/python_pillow_resizing_an_image.htm

Border:

Strip Metadata: https://medium.com/nerd-for-tech/script-to-extract-image-metadata-using-python-and-pillow-library-53a6ae56ccc3

Radio Buttons with a Submit Button after choices are made.

GOAL:
Done: SQL database,

Wednesday -
-python backend CRUD routes
-finish off scripts to do editing functions.
-download file from AWS to use in backend.
-Get AWS file upload/download working today.



Thursday -
1. Users can search image data from the EXIF fields (you can learn about PostgreSQL full-text search)
2. CSS styling
    - fix logo on edit page
    - make prettier (form, etc)
3. Resize images for server capacity
4. Populate with beautiful images of cats
5. Add more editing functions (sketch, vignette, etc PILLOW)


Friday -

