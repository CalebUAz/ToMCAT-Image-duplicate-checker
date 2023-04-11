from PIL import Image
import os
import csv
import imagehash
import multiprocessing
import numpy as np

def images_are_similar_mse(image1_path, image2_path, csv_file_path):
    image1 = Image.open(image1_path).resize((100, 100), Image.ANTIALIAS)
    image2 = Image.open(image2_path).resize((100, 100), Image.ANTIALIAS)
    image1_np = np.asarray(image1)[:,:,0]
    image2_np = np.asarray(image2)[:,:,0]
    mse = np.mean((image1_np.astype("float") - image2_np.astype("float")) ** 2)
    print(mse)
    if mse == 0:
        with open(csv_file_path, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([image1_path])

def worker(args):
    image_paths, method, csv_file_path = args
    process_list(image_paths, method, csv_file_path)

def delete_similar_images(directory, num_processes=None, batch_size=10):
    csv_files = {"images_are_similar_mse": "duplicate_images.csv"}
    
    image_paths = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')])

    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    batch_size = min(batch_size, len(image_paths))
    num_batches = (len(image_paths) + batch_size - 1) // batch_size
    image_path_batches = [image_paths[i:i + batch_size] for i in range(0, len(image_paths), batch_size)]

    csv_file_paths = {}
    for method, csv_file_name in csv_files.items():
        csv_file_path = os.path.join(directory, csv_file_name)
        csv_file_paths[method] = csv_file_path
        with open(csv_file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["image_path"])

    with multiprocessing.Pool(num_processes) as pool:
        tasks = [(batch, method, csv_file_path) for batch in image_path_batches for method, csv_file_path in csv_file_paths.items()]
        for _ in pool.imap_unordered(worker, tasks):
            pass
        pool.close()
        pool.join()

def process_list(image_paths, method, csv_file_path):
    for i in range(len(image_paths)):
        for j in range(i+1, len(image_paths)):
            if method == "images_are_similar_mse":
                images_are_similar_mse(image_paths[i], image_paths[j], csv_file_path)


if __name__ == '__main__':
    base_dir = "/Users/calebjonesshibu/Desktop/tom/exp_2023_02_21_14"
    imac_folders = ["lion", "tiger", "leopard"]
    
    for imac in imac_folders:
        folder_path = os.path.join(base_dir, imac, "face_images")
        delete_similar_images(folder_path, num_processes=10, batch_size=2)
