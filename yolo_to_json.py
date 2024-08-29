import json
import os
import torch
from pathlib import Path

import random
import string

from PIL import Image

classes=['batch_number','expiration_date','health_stamp','product_name']

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.size  # (width, height)
def generate_unique_id(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def save_predictions_to_json(predictions, save_dir, image_dimensions):
    json_results = []

    for pred in predictions:
        image_id, polygons = pred
        image_name = Path(image_id).name
        img_width, img_height = image_dimensions[image_id]

        annotations = []

        for polygon in polygons:
            if len(polygon) > 2:
                points = [[polygon[i]*100, polygon[i+1]*100] for i in range(1, len(polygon) - 1, 2)]

                annotation_id = generate_unique_id()
                polygon_dict = {
                    "id": annotation_id,
                    "type": "polygonlabels",
                    "value": {
                        "points": points,
                        "closed": True,
                        "polygonlabels": [classes[int(polygon[0])]]  # Replace with actual label name
                    },
                    "to_name": "image",
                    "from_name": "label",
                    "image_rotation": 0,
                    "original_width": img_width,  # Update with actual width
                    "original_height": img_height  # Update with actual height
                }
                annotations.append(polygon_dict)

        json_result = {
            "data": {
               'image': f'http://localhost:8080/data/local-files/?d=images/{image_name}.jpg'
            },
            "annotations": [{
                "result": annotations,
                "ground_truth": False
            }]
        }
        json_results.append(json_result)

    json_path = os.path.join(save_dir, "data7_200_try_pred.json")
    with open(json_path, 'w') as f:
        json.dump(json_results, f, indent=4)

def main():

    source = r"C:\Users\ASUS\Desktop\lot10\try_img"
    save_dir = r"C:\Users\ASUS\Desktop\lot10\try_proc"  # Change this as needed
    image_dimensions = {}

    for file in os.listdir(source):
        if file.endswith('.jpg') or file.endswith('.png'):
            image_id = file.split('.')[0]
            image_path = os.path.join(source, file)
            img_width, img_height = get_image_dimensions(image_path)
            image_dimensions[image_id] = (img_width, img_height)

    predictions = []
    for file in os.listdir(save_dir):
        if file.endswith('.txt'):
            image_id = file.split('.')[0]
            with open(os.path.join(save_dir, file), 'r') as f:
                polygons = [list(map(float, line.strip().split())) for line in f]
                predictions.append([image_id, polygons])

    # Save predictions to JSON
    save_predictions_to_json(predictions, r"C:\Users\ASUS\Desktop\lot10",image_dimensions)

if __name__ == "__main__":
    main()