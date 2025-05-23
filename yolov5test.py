import torch
from PIL import ImageGrab


# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Image
im = ImageGrab.grab()  # take a screenshot

# Inference
results = model(im)

results.show()