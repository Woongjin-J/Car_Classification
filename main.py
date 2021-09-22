import os
from flask import Flask, render_template, url_for, request, redirect, \
  send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
# app.config['SECRET_KEY'] = '7a82f51512f29fbb0f91937c0441bc5c'
app.config['VALID_EXTENSIONS'] = ['jpg', 'jpeg', 'png']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/local_file')
def local_file():
  return render_template('local_file.html')

@app.route('/upload_iamge', methods = ['GET', 'POST'])
def upload_image():
   if request.method == 'POST':
      img_file = request.files['file']
      img_file.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(img_file.filename)))
      return 'file uploaded successfully'

if __name__ == '__main__':
  app.run(debug=True)