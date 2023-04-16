from PIL import Image
import os
import csv
import imagehash
import multiprocessing
import numpy as np
import argparse

def images_are_similar_mse(image1_path, image2_path, csv_file_path, delete_images):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    image1_np = np.asarray(image1)[:,:,:]
    image2_np = np.asarray(image2)[:,:,:]
    mse = np.mean((image1_np.astype("float") - image2_np.astype("float")) ** 2)
    # print(mse)
    if mse == 0:
        if delete_images:
            os.remove(image1_path)
        else:
            with open(csv_file_path, "a", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([image1_path])

def worker(args):
    image_paths, method, csv_file_path, delete_images = args
    process_list(image_paths, method, csv_file_path, delete_images)

def delete_similar_images(directory, delete_images, csv_output_dir=None, num_processes=None, batch_size=10, exp_folder=None, imac_folder=None):
    csv_files = {"images_are_similar_mse": "duplicate_images.csv"}
    
    image_paths = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')])

    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    batch_size = min(batch_size, len(image_paths))
    num_batches = (len(image_paths) + batch_size - 1) // batch_size
    image_path_batches = [image_paths[i:i + batch_size] for i in range(0, len(image_paths), batch_size)]

    csv_file_paths = {}
    for method, csv_file_name in csv_files.items():
        if csv_output_dir:
            output_dir = os.path.join(csv_output_dir, exp_folder, imac_folder, "face_images")
            os.makedirs(output_dir, exist_ok=True)
            csv_file_path = os.path.join(output_dir, csv_file_name)
        else:
            csv_file_path = os.path.join(directory, csv_file_name)
        csv_file_paths[method] = csv_file_path
        print(csv_file_path)
        with open(csv_file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["image_path"])

    with multiprocessing.Pool(num_processes) as pool:
        tasks = [(batch, method, csv_file_path, delete_images) for batch in image_path_batches for method, csv_file_path in csv_file_paths.items()]
        for _ in pool.imap_unordered(worker, tasks):
            pass
        pool.close()
        pool.join()

def process_list(image_paths, method, csv_file_path, delete_images):
    for i in range(len(image_paths)):
        for j in range(i+1, len(image_paths)):
            if method == "images_are_similar_mse":
                images_are_similar_mse(image_paths[i], image_paths[j], csv_file_path, delete_images)

    for i in range(len(image_paths)):
        for j in range(i+1, len(image_paths)):
            if method == "images_are_similar_mse":
                images_are_similar_mse(image_paths[i], image_paths[j], csv_file_path, delete_images)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find and remove duplicate images.')
    parser.add_argument('--exp_dir', type=str, required=True, help='Experiment directory path which has lion, tiger, leopard which contains the image folders.')
    parser.add_argument('--delete', action='store_true', help='Delete duplicate images instead of writing to CSV.')
    parser.add_argument('--csv_output_dir', type=str, help='Output directory for CSV file, if not deleting images.')
    args = parser.parse_args()
    
    exp_dir = str(args.exp_dir)
    delete_images = args.delete
    csv_output_dir = args.csv_output_dir
    imac_folders = ["lion", "tiger", "leopard"]
    
    exp_folder_name = os.path.basename(exp_dir)

    for imac in imac_folders:
        folder_path = os.path.join(exp_dir, imac, "face_images")
        delete_similar_images(
            folder_path,
            num_processes=10,
            batch_size=2,
            delete_images=delete_images,
            csv_output_dir=csv_output_dir,
            exp_folder=exp_folder_name,
            imac_folder=imac
        )