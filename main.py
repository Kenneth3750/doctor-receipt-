from flask import Flask, render_template, jsonify,  request
from PIL import Image
from werkzeug.datastructures import FileStorage
from pytesseract import pytesseract 

app = Flask(__name__)

def read_image(img):
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract 
    text = pytesseract.image_to_string(img) 
    receipt = get_receipt(text)
    user_cc = get_CC(text)
    nap = get_nap(text)
    return receipt, user_cc, nap

def get_receipt(text):
    lines = text.split('\n')
    receipt = lines[1]
    return receipt

def get_CC(text):
    keyword = "DOCUMENTO DE IDENTIDAD"
    keyword_position = text.find(keyword)
    if keyword_position != -1:
        next_newline_position = text.find("\n", keyword_position)
        if next_newline_position != -1:
            following_text = text[keyword_position + len(keyword):next_newline_position].strip()
        else:
            following_text = text[keyword_position + len(keyword):].strip()
        return following_text
    else:
        return None
def get_nap(text):
    keyword = 'NAP: '
    position = text.find(keyword)
    nap_start = (position + len(keyword))

    if position != -1:
        nap_end = text.find(" ", nap_start )
        if nap_end != -1:
            nap_value = text[nap_start:nap_end].strip()
        else:
            nap_value = text[nap_start:].strip()
        return nap_value
    else: 
        return None
    


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        receipt, user_cc = read_image(image)
        

        return jsonify({ 'No. de factura': receipt, 'Cédula': user_cc })

if __name__ == '__main__':
    app.run(debug=True)

