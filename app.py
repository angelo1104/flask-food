from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

ALLOWED_EXTENSIONS = [
    "jpg",
    "jpeg",
    "png"
]


def process_file(file, filename):
    print(file, filename)
    return {
        "message": "success",
        "filename": filename
    }


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
def process_image():
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            return {
                       "message": "Please upload file"
                   }, 400

        file = request.files['file']

        if file.filename == '':
            return {
                       "message": "Please upload file"
                   }, 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            return process_file(file, filename)

        return {
                   "message": "Error"
               }, 400
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
