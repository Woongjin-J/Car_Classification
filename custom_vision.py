"""
Creates a Custom Vision project on Azure and upload the training images to their
corresponding tags.
Starter code instruction for creating CV project and some part of uploading
process followed through the link below
https://docs.microsoft.com/zh-cn/azure/cognitive-services/custom-vision-service/quickstarts/image-classification?tabs=visual-studio&pivots=programming-language-python
"""

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid
import scipy.io as sio
import pandas as pd

## <snippet_creds>
# API credentials
# Replace with valid values
ENDPOINT = ""
training_key = ""
prediction_key = ""
prediction_resource_id = ""
## </snippet_creds>

## <snippet_auth>
# Authenticates the API credentials entered earlier
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
## </snippet_auth>

## <snippet_create>
credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)

# Create a new project
print ("Creating project...")
project_name = "Car_Classification"
project = trainer.create_project(project_name)
## </snippet_create>

## <snippet_matConvert>
# Converts the MATLAB file into python readable list
mat = sio.loadmat('devkit/cars_train_annos.mat') # training image labeled with its corresponding class number
class_mat = sio.loadmat('devkit/cars_meta.mat') # class full name

# Converting into pandas data frame (probably don't need to following three lines)
# data = [[row.flat[0] for row in line] for line in mat['annotations'][0]]
# columns = ['bbox_x1', 'bbox_y1', 'bbox_x2', 'bbox_y2', 'class', 'fname']
# df_train = pd.DataFrame(data, columns=columns)

class_num = [i.flat[0] for i in mat['annotations'][0]['class']]
fname = [i.flat[0] for i in mat['annotations'][0]['fname']]
## </snippet_matConvert>

## <snippet_upload>
base_image_location = os.path.join (os.path.dirname(__file__), "cars_train")

print("Adding images...")

image_list = []
car_tag = []

# Saves tag name in an array
for i in range(0, 196):
    car_tag.append(trainer.create_tag(project.id, class_mat['class_names'][0][i].flat[0]))

# Assign each image to its corresponding tag
for i in range(0, len(fname)):
    file_name = fname[i]
    classStr = class_num[i] - 1
    with open(os.path.join (base_image_location, file_name), "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), tag_ids=[car_tag[classStr].id]))

# Group images into a chunk of 64 images (64 image is the max limit to upload images each time)
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

batchedimg = chunks(image_list, 64)

# Upload batched images chunks by chunks
for batch in batchedimg:
    upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=batch))

if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print("Image status: ", image.status)
    exit(-1)
# </snippet_upload>
