# importing the required libraries
import os
from fileinput import filename

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import model

# initialising the flask app
app = Flask(__name__)

# Creating the upload folder
upload_folder = "uploads/"
if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)
# Creating the detected folder
detected_folder = "detected/"
if not os.path.exists(detected_folder):
    os.mkdir(detected_folder)

app.config['UPLOAD_FOLDER'] = upload_folder
app.config['DETECTED_FOLDER'] = detected_folder

# The path for uploading the file
@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def uploadfile():
    if request.method == 'POST':  # check if the method is post
        f = request.files['file']  # get the file from the files object
        # Saving the file in the required destination
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))  # this will secure the file
        model.process_image(f'uploads/{secure_filename(f.filename)}')
        return render_template('upload.html')


if __name__ == '__main__':
    app.run()  # running the flask app