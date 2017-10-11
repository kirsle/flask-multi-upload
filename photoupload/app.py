from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import json
import glob
from uuid import uuid4
import config as cf

#Global Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

#DB Object declarations
class Upload(db.Model):
    __tablename__ = "uploads"
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.Text, nullable=False)

class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    upload_id = db.Column(db.Integer, db.ForeignKey('uploads.id'), nullable=False)
    upload = db.relationship('Upload', backref=db.backref('images', lazy=True))
    filename = db.Column(db.String(1024), nullable=False)

db.create_all()

def is_safe_path(basedir, path, follow_symlinks=True):
  # resolves symbolic links
  if follow_symlinks:
    return os.path.realpath(path).startswith(os.path.realpath(basedir))
  return os.path.abspath(path).startswith(os.path.realpath(basedir))

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of a file."""
    form = request.form
    ul = Upload()

    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())
    ul.uuid=upload_key

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = "{}/{}".format(cf.upload_dir,upload_key)

    try:
        os.mkdir(target)
    except:
        if is_ajax:
            return ajax_response(False, "Couldn't create upload directory: {}".format(target))
        else:
            return "Couldn't create upload directory: {}".format(target)
    if app.debug:
        print("=== Form Data ===")
        for key, value in list(form.items()):
            print(key, "=>", value)

    #Check to make sure a name is provided
    if len(form['name']) == 0:
        if is_ajax:
            return ajax_response(False, "Name is required!")
        else:
            return "Name is required!"

    #Populate upload object fully
    ul.name = form['name']
    ul.desc = form['desc']

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
        db.session.add(Image(filename=filename, upload=ul))

    db.session.commit()
    if is_ajax:
        return ajax_response(True, upload_key)
    else:
        return redirect(url_for("upload_complete", uuid=upload_key))


@app.route("/files/<uuid>")
def upload_complete(uuid):
    """The location we send them to at the end of the upload."""

    # Get files, making sure the path is safe!
    root = "{}/{}".format(cf.upload_dir,uuid)
    
    if not is_safe_path(cf.upload_dir, root):
        return "Error: Path is invalid!"

    if not os.path.isdir(root):
        return "Error: UUID not found!"

    files = []
    for file in glob.glob("{}/*.*".format(root)):
        fname = file.split(os.sep)[-1]
        files.append(fname)

    return render_template("files.html",
        uuid=uuid,
        files=files,
    )


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))
