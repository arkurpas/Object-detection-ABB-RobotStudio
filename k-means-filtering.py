import os
import cv2
import numpy as np
from sklearn.cluster import KMeans

num_clusters = 10

def kmeans_segmentation(image, num_clusters):
    """
    Perform k-means segmentation on the given image.

    Args:
        image (numpy.ndarray): Input image array.
        num_clusters (int): Number of clusters.

    Returns:
        numpy.ndarray: Segmented image.
    """
    # Convert image to RGB color space
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Reshape image to pixel vector
    pixels = image.reshape((-1, 3))

    # Initialize k-means model
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    # Fit model to data
    kmeans.fit(pixels)

    # Assign labels to pixels
    labels = kmeans.labels_
    # Convert centroids to pixel values
    centers = np.uint8(kmeans.cluster_centers_)
    # Transform image to image with assigned clusters
    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(image.shape)

    return segmented_image


def process_folder(folder_path, output_folder='../iCloud-Photos/'):
    """
    Process images in the specified folder.

    Args:
        folder_path (str): Path to the folder containing images.
        output_folder (str): Output folder for processed images.
    """
    files = os.listdir(folder_path)
    for file_name in files:
        if file_name.endswith('.JPEG') or file_name.endswith('.png'):
            image_path = os.path.join(folder_path, file_name)
            image = cv2.imread(image_path)
            if image is not None:
                if 'onion' in folder_path:
                    num_clusters = 10
                    # Perform k-means segmentation only if number of clusters is provided
                    segmented_image = kmeans_segmentation(image, num_clusters)
                    segmented_image = segmented_image.astype('uint8')
                    cv2.imwrite(os.path.join(output_folder, f"{file_name.split('.')[0]}_segmented.JPEG"),
                                cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))
                elif 'pepper' in folder_path:
                    num_clusters = 10
                    # Otherwise, save the original image
                    segmented_image = kmeans_segmentation(image, num_clusters)
                    segmented_image = segmented_image.astype('uint8')
                    cv2.imwrite(os.path.join(output_folder, f"{file_name.split('.')[0]}_segmented.JPEG"),
                                cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))


# Perform k-means operation for images in the 'segmented_images' folder with 10 clusters
process_folder('../iCloud-Photos/onion')

# Leave images in the 'original_images' folder unchanged
process_folder('../iCloud-Photos/pepper')
