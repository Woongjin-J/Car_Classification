from __future__ import print_function
import os
import requests
import json
import sys
from PIL import Image
from flask import Flask, render_template, url_for, request, redirect, \
  send_from_directory, jsonify
from werkzeug.utils import secure_filename

url = "https://carclassification-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/7e22c873-b892-4b3a-8c64-020a9c551c16/classify/iterations/Car_Classification/image"
headers = {'content-type':'application/octet-stream', 'Prediction-Key':'d37e9f6455e2423a8a4907ee280941c6'}

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['VALID_EXTENSIONS'] = ['jpg', 'jpeg', 'png']
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/local_file')
def local_file():
  file = os.listdir(app.config['UPLOAD_PATH'])
  return render_template('local_file.html', file=file)

@app.route('/local_file', methods = ['POST'])
def upload_image():
   if request.method == 'POST':
      img_file = request.files['file']
      filename = secure_filename(img_file.filename)
      img_path = os.path.join(app.config['UPLOAD_PATH'], filename)
      img_file.save(img_path)

      response = requests.post(url, data=open(img_path, "rb"), headers=headers)
      response.raise_for_status()
      prediction = response.json()["predictions"]
      print("\t" + prediction[0]["tagName"] + ": {0:.2f}%".format(prediction[0]["probability"]*100))
      return render_template('local_file.html', prediction=prediction, img_path=img_path)

#Save the image to /uploads
@app.route('/uploads/<filename>')
def upload(filename):
  return send_from_directory(app.config['UPLOAD_PATH'], filename)

# with app.test_request_context():
#         print(url_for('local_file'))

if __name__ == '__main__':
  app.run(debug=True)