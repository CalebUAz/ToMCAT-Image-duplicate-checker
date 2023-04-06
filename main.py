from PIL import Image
import os
import csv
import imagehash

# Define a function to compare two images using histogram and write to CSV file
def images_are_similar_histogram(image1_path, image2_path, csv_file_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    if image1.histogram() == image2.histogram():
        with open(csv_file_path, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["images_are_similar_histogram", image1_path, image2_path])

# Define a function to compare two images using hash and write to CSV file
def images_are_similar_hash(image1_path, image2_path, csv_file_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    hash1 = imagehash.average_hash(image1)
    hash2 = imagehash.average_hash(image2)
    if hash1 == hash2:
        with open(csv_file_path, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["images_are_similar_hash", image1_path, image2_path])

# Define a function to delete similar images
def delete_similar_images(directory, csv_file_path):
    image_paths = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')]
    for i in range(len(image_paths)):
        for j in range(i+1, len(image_paths)):
            images_are_similar_histogram(image_paths[i], image_paths[j], csv_file_path)
            images_are_similar_hash(image_paths[i], image_paths[j], csv_file_path)

# Example usage
csv_file_path = "similar_images.csv"
with open(csv_file_path, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["method", "image1_path", "image2_path"])
delete_similar_images("/space/tomcat/LangLab/experiments/study_3_pilot/group/exp_2023_02_21_14/lion/face_images", csv_file_path)
