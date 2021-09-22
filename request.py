import requests
import json
import os
from PIL import Image

url = "https://carclassification-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/7e22c873-b892-4b3a-8c64-020a9c551c16/classify/iterations/Car_Classification/image"

headers = {'content-type':'application/octet-stream', 'Prediction-Key':'d37e9f6455e2423a8a4907ee280941c6'}
img_location = os.path.join (os.path.dirname(__file__), "cars_test")

response = requests.post(url, data=open(os.path.join(img_location, "00021.jpg"), "rb"), headers=headers)
response.raise_for_status()

prediction = response.json()["predictions"]
print("\t" + prediction[0]["tagName"] + ": {0:.2f}%".format(prediction[0]["probability"]*100))
