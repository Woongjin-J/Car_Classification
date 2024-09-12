"""
This program runs a web-app using Flask for car classification. The dataset used
is Cars Dataset from Stanford that contains 196 categories named as 'Make Model Year",
and the cars are all made on or before 2012.There are 8,144 training images and
8,041 testing images. Data uploaded by running custom_vision.py

Dataset URL: http://ai.stanford.edu/~jkrause/cars/car_dataset.html
azure URL of this project: https://car-classification.azurewebsites.net
"""

import os
import json
import requests
from PIL import Image
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

# API url address and the headers for prediction call
prediction_url = "https://carclassification-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/7e22c873-b892-4b3a-8c64-020a9c551c16/classify/iterations/Car_Classification/image"
headers = {'content-type':'application/octet-stream', 'Prediction-Key':''}

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER

# Car classification page where image can be uploaded both from local folder
# and camera. The result of prediction is presented after the button 'identify'
# is clicked/tapped
@app.route('/')
def classification():
  return render_template('classification.html')

# Stores the chosen image and sends prediction request to the cloud.
# [prediction]: returning the result with the highest probability
# [img_path]: image directory saved in 'uploads' to present on the web-page
@app.route('/', methods=['POST'])
def upload_image():
   if request.method == 'POST':
      # Receives POST request and saves the uploaded image to 'uploads' folder
      img_file = request.files['file']
      filename = secure_filename(img_file.filename)
      img_path = os.path.join(app.config['UPLOAD_PATH'], filename)
      img_file.save(img_path)

      # Sends the image in a format of byte array to the API for predictions that
      # is returned in JSON
      response = requests.post(prediction_url, data=open(img_path, "rb"), headers=headers)
      response.raise_for_status() # error check
      prediction = response.json()["predictions"][0]
      return render_template("classification.html", prediction=prediction, img_path=img_path)

# Saves the image on the server so the image can be retrived later (i.e. remain
# image presentation after 'identify' button clicked)
@app.route('/uploads/<filename>')
def upload(filename):
  return send_from_directory(app.config['UPLOAD_PATH'], filename)

if __name__ == '__main__':
  app.run(debug=True)
