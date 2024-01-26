from flask import Flask, render_template, jsonify,  request
from PIL import Image
from werkzeug.datastructures import FileStorage

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        image = Image.open(file)
        # Aquí puedes procesar la imagen con Python.
        # Por ejemplo, vamos a obtener sus dimensiones:
        width, height = image.size
        return jsonify({ 'width': width, 'height': height })

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)