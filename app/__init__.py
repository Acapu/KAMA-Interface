from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os, pickle
from fastbook import load_learner

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/upload"
app.secret_key = "very-secret-key"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        upload_file()
    # test.predict(r"app\static\upload\L7160037.JPG")
    return render_template("index.html")

def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.root_path,
                  app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
