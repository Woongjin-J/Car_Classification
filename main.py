from __future__ import print_function
import os
import requests
import json
from PIL import Image
from flask import Flask, render_template, url_for, request, redirect, \
  send_from_directory, jsonify
from werkzeug.utils import secure_filename

prediction_url = "https://carclassification-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/7e22c873-b892-4b3a-8c64-020a9c551c16/classify/iterations/Car_Classification/image"
headers = {'content-type':'application/octet-stream', 'Prediction-Key':'d37e9f6455e2423a8a4907ee280941c6'}

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['VALID_EXTENSIONS'] = ['jpg', 'jpeg', 'png']
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER

# home page with two button (camera & local file)
@app.route('/')
def home():
  return render_template('home.html')

# local file page where one can upload local image
@app.route('/local_file')
def local_file():
  return render_template('local_file.html')

# Make prediction of the image uploaded
@app.route('/local_file', methods=['POST'])
def upload_image():
   if request.method == 'POST':
      # Receives POST request and save the uploaded image to the FLask's uploads folder
      img_file = request.files['file']
      filename = secure_filename(img_file.filename)
      img_path = os.path.join(app.config['UPLOAD_PATH'], filename)
      img_file.save(img_path)

      # Sends the image in a format of byte array to the API for predictions saved in json
      response = requests.post(prediction_url, data=open(img_path, "rb"), headers=headers)
      response.raise_for_status()
      prediction = response.json()["predictions"][0]
      return render_template('local_file.html', prediction=prediction, img_path=img_path)

# Save the image to /uploads folder
@app.route('/uploads/<filename>')
def upload(filename):
  return send_from_directory(app.config['UPLOAD_PATH'], filename)

# Camera page
@app.route('/camera')
def camera():
  return render_template('/camera.html')

@app.route('/camera', methods=['POST'])
def upload_camera():
   if request.method == 'POST':
      # Receives POST request and save the uploaded image to the FLask's uploads folder
      img_file = request.files['file']
      filename = secure_filename(img_file.filename)
      img_path = os.path.join(app.config['UPLOAD_PATH'], filename)
      img_file.save(img_path)
      print("it's working")
      # Sends the image in a format of byte array to the API for predictions saved in json
      response = requests.post(prediction_url, data=open(img_path, "rb"), headers=headers)
      response.raise_for_status()
      prediction = response.json()["predictions"][0]
      return render_template('camera.html', prediction=prediction, img_path=img_path)

if __name__ == '__main__':
  app.run(debug=True)