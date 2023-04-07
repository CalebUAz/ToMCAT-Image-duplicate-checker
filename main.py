from PIL import Image
import os
import csv
import imagehash
import multiprocessing
import numpy as np

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

# Define a function to compare two images using MSE and write to CSV file
def images_are_similar_mse(image1_path, image2_path, csv_file_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    image1_np = np.asarray(image1)
    image2_np = np.asarray(image2)
    mse = np.mean((image1_np.astype("float") - image2_np.astype("float")) ** 2)
    # mse /= float(image1_np.shape[0] * image2_np.shape[1])
    # print(mse)
    if mse < 70:
        with open(csv_file_path, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["images_are_similar_mse", image1_path, image2_path])


# Define a function to delete similar images using parallel processing
def delete_similar_images(directory, num_processes=None, batch_size=10):
    csv_files = {
        "images_are_similar_histogram": "similar_images_histogram.csv",
        "images_are_similar_hash": "similar_images_hash.csv",
        "images_are_similar_mse": "similar_images_mse.csv"
    }
    image_paths = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')])

    # Split the list of image paths into batches for parallel processing
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    batch_size = min(batch_size, len(image_paths))
    num_batches = (len(image_paths) + batch_size - 1) // batch_size
    image_path_batches = [image_paths[i*batch_size:(i+1)*batch_size] for i in range(num_batches)]

    # Open the CSV files in "w" mode
    csv_file_handles = {}
    for method, csv_file_path in csv_files.items():
        csv_file_handles[method] = open(csv_file_path, "w", newline="")
        writer = csv.writer(csv_file_handles[method])
        writer.writerow(["method", "image1_path", "image2_path"])

    # Run the comparison functions on each list of images in parallel processes
    with multiprocessing.Pool(num_processes) as pool:
        for batch in image_path_batches:
            for method, csv_file_path in csv_files.items():
                pool.apply_async(process_list, args=(batch, method, csv_file_path))  # Use the correct CSV file path for each method
        pool.close()
        pool.join()

    # Close the CSV files
    for csv_file_handle in csv_file_handles.values():
        csv_file_handle.close()

# Define a function to run the comparison functions on a list of images
def process_list(image_paths, method, csv_file_path):
    for i in range(len(image_paths)):
        for j in range(i+1, len(image_paths)):
            if method == "images_are_similar_histogram":
                # print("images_are_similar_histogram")
                images_are_similar_histogram(image_paths[i], image_paths[j], csv_file_path)
            elif method == "images_are_similar_hash":
                # print("images_are_similar_hash")
                images_are_similar_hash(image_paths[i], image_paths[j], csv_file_path)
            elif method == "images_are_similar_mse":
                # print("images_are_similar_mse")
                images_are_similar_mse(image_paths[i], image_paths[j], csv_file_path)

delete_similar_images("/space/tomcat/LangLab/experiments/study_3_pilot/group/exp_2023_02_21_14/lion/face_images", num_processes=10, batch_size=100)

