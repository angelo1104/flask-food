import tensorflow.keras
from flask import Flask, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps
import numpy as np

model = tensorflow.keras.models.load_model('keras_model.h5')
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

classes = ["apples", "apricots", "avocados", "bananas", "blackberries", "blueberries", "cantaloupes", "cherries",
           "coconuts", "figs", "grapefruits", "grapes", "guava", "kiwifruit", "lemons", "limes", "mangos", "olives",
           "oranges", "passionfruit", "peaches", "pears", "pineapples", "plums", "pomegranates", "raspberries",
           "strawberries", "tomatoes", "watermelons"]

ALLOWED_EXTENSIONS = [
    "jpg",
    "jpeg",
    "png"
]


def process_file(file, filename):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(file)

    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)

    return {
        "message": "success",
        "fruit": str(classes[prediction.argmax()])
    }


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
@cross_origin()
def process_image():
    if request.method == "POST":
        # check if the post request has the file part

        file = request.files['file']

        
        filename = secure_filename(file.filename)
        return process_file(file, filename)

    return 'Hello World!'


if __name__ == '__main__':
    app.run()
