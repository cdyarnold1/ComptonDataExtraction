import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

import cv2
from matplotlib import pyplot as plt
import json

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of an image containing one table (half page) with column names
img_path = 'C:\\Users\\Sebastian\\Downloads/p33_h1_silver.jpg'

file_name = os.path.abspath(img_path)

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs text detection on the image file
response = client.document_text_detection(image=image)

document = response.full_text_annotation

#img = cv2.imread('C:/Users/Sebastian/Downloads/c_line.jpg')
#im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Open image again for drawing
image = Image.open(img_path)
draw = ImageDraw.Draw(image)

data = []

for page in document.pages:
    for block in page.blocks:
        for paragraph in block.paragraphs:
            draw.polygon([
                paragraph.bounding_box.vertices[0].x, paragraph.bounding_box.vertices[0].y,
                paragraph.bounding_box.vertices[1].x, paragraph.bounding_box.vertices[1].y,
                paragraph.bounding_box.vertices[2].x, paragraph.bounding_box.vertices[2].y,
                paragraph.bounding_box.vertices[3].x, paragraph.bounding_box.vertices[3].y], None, 'blue')
            for word in paragraph.words:
                draw.polygon([
                    word.bounding_box.vertices[0].x, word.bounding_box.vertices[0].y,
                    word.bounding_box.vertices[1].x, word.bounding_box.vertices[1].y,
                    word.bounding_box.vertices[2].x, word.bounding_box.vertices[2].y,
                    word.bounding_box.vertices[3].x, word.bounding_box.vertices[3].y], None, 'red')

                text = ""
                for symbol in word.symbols:
                    text += symbol.text
                # Save vertices and text to analyze
                data.append([
                    (word.bounding_box.vertices[0].x, word.bounding_box.vertices[2].x),
                    (word.bounding_box.vertices[0].y, word.bounding_box.vertices[2].y),
                    text
                ])

# Export to file to be read by parse.py
with open('p33_h1_silver.json', 'w') as f:
    json.dump(data, f)

# Show an image of the text detection
image.show()
image.save("ocr.png")