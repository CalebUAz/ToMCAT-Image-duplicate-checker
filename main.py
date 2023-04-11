from PIL import Image
import os
import csv
import imagehash
import multiprocessing
import numpy as np

# Define a function to compare two images using MSE and write to CSV file
def images_are_similar_mse(image1_path, image2_path, csv_file_path):
    image1 = Image.open(image1_path).resize((100, 100), Image.ANTIALIAS)
    image2 = Image.open(image2_path).resize((100, 100), Image.ANTIALIAS)
    image1_np = np.asarray(image1)[:,:,0]  # Extract the Red channel
    image2_np = np.asarray(image2)[:,:,0]  # Extract the Red channel
    mse = np.mean((image1_np.astype("float") - image2_np.astype("float")) ** 2)
    print(mse)
    if mse == 0:
        with open(csv_file_path, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([image1_path])
            # Remove the file
            # os.remove(image1_path) 

def worker(args):
    image_paths, method, csv_file_path = args
    process_list(image_paths, method, csv_file_path)

# Define a function to delete similar images using parallel processing
def delete_similar_images(directory, num_processes=None, batch_size=10):
    csv_files = {"images_are_similar_mse": "duplicate_images.csv"}
    image_paths = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')])

    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    batch_size = min(batch_size, len(image_paths))
    num_batches = (len(image_paths) + batch_size - 1) // batch_size
    image_path_batches = [image_paths[i:i + batch_size] for i in range(0, len(image_paths), batch_size)]

    csv_file_handles = {}
    for method, csv_file_path in csv_files.items():
        csv_file_handles[method] = open(csv_file_path, "w", newline="")
        writer = csv.writer(csv_file_handles[method])
        writer.writerow(["image_path"])

    with multiprocessing.Pool(num_processes) as pool:
        tasks = [(batch, method, csv_file_path) for batch in image_path_batches for method, csv_file_path in csv_files.items()]
        for _ in pool.imap_unordered(worker, tasks):
            pass
        pool.close()
        pool.join()

    for csv_file_handle in csv_file_handles.values():
        csv_file_handle.close()

# Define a function to run the comparison functions on a list of images
def process_list(image_paths, method, csv_file_path):
    for i in range(len(image_paths)):
        for j in range(i+1, len(image_paths)):
            if method == "images_are_similar_mse":
                images_are_similar_mse(image_paths[i], image_paths[j], csv_file_path)

if __name__ == '__main__':
    delete_similar_images("/Users/calebjonesshibu/Desktop/tom/exp_2023_02_21_14/lion/face_images", num_processes=10, batch_size=2)
