from PIL import Image
import os
import csv
import imagehash
import multiprocessing

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

# Define a function to run the comparison functions on a pair of images
def process_pair(image_paths, csv_file_path):
    images_are_similar_histogram(image_paths[0], image_paths[1], csv_file_path)
    images_are_similar_hash(image_paths[0], image_paths[1], csv_file_path)

# Define a function to delete similar images using parallel processing
def delete_similar_images(directory, csv_file_path, num_processes=None):
    image_paths = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')])

    # Split the list of image paths into chunks for parallel processing
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    chunk_size = len(image_paths) // num_processes
    image_path_chunks = [image_paths[i:i+chunk_size] for i in range(0, len(image_paths), chunk_size)]

    # Run the comparison functions on each pair of images in parallel processes
    with multiprocessing.Pool(num_processes) as pool:
        for chunk in image_path_chunks:
            args_list = [(pair, csv_file_path) for pair in zip(chunk, chunk[1:])]
            pool.starmap(process_pair, args_list)

# Example usage
csv_file_path = "similar_images.csv"
with open(csv_file_path, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["method", "image1_path", "image2_path"])
delete_similar_images("/space/tomcat/LangLab/experiments/study_3_pilot/group/exp_2023_02_21_14/lion/face_images", csv_file_path, num_processes=4)
