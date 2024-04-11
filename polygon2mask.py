import os
import xml.etree.ElementTree as ET
import numpy as np
import cv2
import matplotlib.pyplot as plt

def parse_xml(xml_file):
    """
    Parse XML annotation file and extract object coordinates.

    Args:
        xml_file (str): Path to the XML annotation file.

    Returns:
        dict: Dictionary containing object coordinates for each class.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    objects_coords = {}

    for obj in root.findall('object'):
        name = obj.find('name').text
        polygons = obj.findall('polygon')
        all_coords = []
        for polygon in polygons:
            coords = []
            for point in polygon:
                if point.tag.startswith('x'):
                    x = float(point.text)
                    y = float(polygon.find('y' + point.tag[1:]).text)
                    coords.append((x, y))
            if coords:
                all_coords.append(coords)
        if all_coords:
            if name in objects_coords:
                objects_coords[name].extend(all_coords)
            else:
                objects_coords[name] = all_coords

    return objects_coords


def create_mask(mask, class_name, polygons):
    """
    Create mask for given class and polygons.

    Args:
        mask (numpy.ndarray): Input mask array.
        class_name (str): Class name.
        polygons (list): List of polygons for the class.

    Returns:
        numpy.ndarray: Updated mask array.
    """
    class_colors = {'crunchips': 80,  #
                    'lays': 255,  #
                    }  #

    color = class_colors[class_name]
    for polygon in polygons:
        pts = np.array(polygon, np.int32)
        mask = cv2.fillPoly(mask, pts=[pts], color=color)
    return mask


def process_folder(folder_path):
    """
    Process all XML annotation files in the specified folder.

    Args:
        folder_path (str): Path to the folder containing XML files.
    """
    files = os.listdir(folder_path)
    for file_name in files:
        if file_name.endswith('.xml'):
            image_file = os.path.join(folder_path, file_name.replace('.xml', '.jpg'))
            xml_file = os.path.join(folder_path, file_name)
            image = cv2.imread(image_file, 1)
            objects_coords = parse_xml(xml_file)

            # Initialize empty mask for all classes
            mask = np.zeros(image.shape[:2], dtype=np.uint8)

            # Iterate over all classes and their polygons
            for name, polygons in objects_coords.items():
                # Create mask for the class and add it to the overall mask
                class_mask = create_mask(mask, name, polygons)

            # Save the overall mask
            cv2.imwrite(os.path.join(folder_path, f"{file_name.replace('.xml', '_mask.png')}"), class_mask)


folder_path = "../show"
process_folder(folder_path)
