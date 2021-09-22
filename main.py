import os
import json
import requests
from PIL import Image
from flask import Flask, render_template, url_for, request, redirect, \
  send_from_directory
from werkzeug.utils import secure_filename

url = "https://carclassification-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/7e22c873-b892-4b3a-8c64-020a9c551c16/classify/iterations/Car_Classification/image"
headers = {'content-type':'application/octet-stream', 'Prediction-Key':'d37e9f6455e2423a8a4907ee280941c6'}

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

# @app.route('/', methods = ['POST'])
# def identify(filename):
#   prediction = car_identification(filename)
#   return render_template('local_file.html', prediction=prediction)

@app.route('/upload_image', methods = ['POST'])
def car_identification(filename):
  response = requests.post(url, data=open(filename, "rb"), headers=headers)
  response.raise_for_status()

  prediction = response.json()["predictions"]
  return render_template('local_file.html', prediction=prediction)
  # print("\t" + prediction[0]["tagName"] + ": {0:.2f}%".format(prediction[0]["probability"]*100))


if __name__ == '__main__':
  app.run(debug=True)