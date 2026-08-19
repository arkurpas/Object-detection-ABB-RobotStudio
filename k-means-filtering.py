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


def process_folder(folder_path, output_folder, num_clusters=10):
    """
    Run k-means color segmentation on every image in a folder.

    Args:
        folder_path (str): Path to the folder containing source images.
        output_folder (str): Output folder for segmented images.
        num_clusters (int): Number of color clusters to use.
    """
    os.makedirs(output_folder, exist_ok=True)
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_path, file_name)
            image = cv2.imread(image_path)
            if image is not None:
                segmented_image = kmeans_segmentation(image, num_clusters).astype('uint8')
                cv2.imwrite(os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_segmented.jpg"),
                            cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))


if __name__ == "__main__":
    # Example: segment the training images used for annotation.
    process_folder('my_pictures.v8i.voc/train', 'my_pictures.v8i.voc/train_segmented', num_clusters)
