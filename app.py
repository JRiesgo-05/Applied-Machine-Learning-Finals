from flask import Flask, flash, request, redirect, url_for, render_template , send_from_directory
import urllib.request
import os
from werkzeug.utils import secure_filename
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
 
UPLOAD_FOLDER = '/content/Applied-Machine-Learning-Finals/static/uploads'
DARKNET_FOLDER = '/content/darknet'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DARKNET_FOLDER'] = DARKNET_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
run_with_ngrok(app)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        #print(os.path.join(app.config['UPLOAD_FOLDER'] + filename))
        #os.system("./content/darknet/darknet detect cfg/custom-yolov4-detector.cfg '/content/drive/MyDrive/Copy of custom-yolov4-detector_12000.weights' {img_path} -dont-show")
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    to_be_filename = app.config["UPLOAD_FOLDER"] +"/" + filename
    command = ("/content/darknet/darknet detect cfg/custom-yolov4-detector.cfg '/content/drive/MyDrive/Copy of custom-yolov4-detector_12000.weights' '%(img_path)s' -dont-show" % {'img_path':to_be_filename})
    os.system(command)
    return send_from_directory(app.config["DARKNET_FOLDER"] +"/", filename='predictions.jpg')
 
if __name__ == "__main__":
    app.run()