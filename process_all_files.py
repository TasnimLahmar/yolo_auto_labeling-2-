import os
from shapely.geometry import Polygon


def polygon_to_bbox(polygon_coords):

    polygon = Polygon(polygon_coords)


    minx, miny, maxx, maxy = polygon.bounds


    return minx, miny, maxx, maxy


# Directory containing the input files
input_dir = r"C:\Users\ASUS\Desktop\lot10\try_pred"
output_dir = r"C:\Users\ASUS\Desktop\lot10\try_proc"

os.makedirs(output_dir, exist_ok=True)

# Process each file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.txt'):
        input_file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, filename)

        with open(input_file_path, 'r') as file:
            lines = file.readlines()

        all_bbox_coords = []

        for line in lines:
            parts = line.strip().split()
            class_id = parts[0]
            coords = list(map(float, parts[1:]))
            polygon_coords = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
            bbox_coords = polygon_to_bbox(polygon_coords)
            all_bbox_coords.append((class_id, bbox_coords))

        # Save the bounding box coordinates back to a file
        with open(output_file_path, 'w') as file:
            for class_id, bbox_coords in all_bbox_coords:
                file.write(
                    f"{class_id} {bbox_coords[0]} {bbox_coords[1]} {bbox_coords[2]} {bbox_coords[1]} {bbox_coords[2]} {bbox_coords[3]} {bbox_coords[0]} {bbox_coords[3]}\n")

print("Bounding box coordinates for all polygons in all files have been processed and saved.")

