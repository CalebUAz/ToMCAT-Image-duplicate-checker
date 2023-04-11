import argparse
import csv
import os
from PIL import Image
import multiprocessing

def create_gif_from_csv(args):
    animal, exp_dir, num_images_to_read = args
    csv_file_path = os.path.join(exp_dir, animal, "face_images", "duplicate_images.csv")
    output_gif_path = os.path.join(exp_dir, animal, "face_images", "output.gif")

    print(output_gif_path)
    image_paths = []
    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for i, row in enumerate(reader):
            if i >= num_images_to_read:
                break
            image_paths.append(row["image_path"])

    # print(len(image_paths))

    # Open the images
    images = [Image.open(image_path) for image_path in image_paths[1:]]

    # Save the images as a GIF
    images[0].save(output_gif_path, save_all=True, append_images=images[1:], duration=50, loop=0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a GIF from duplicate images listed in CSV files.")
    parser.add_argument("--exp_dir", type=str, required=True, help="Experiment directory path containing leopard, lion, and tiger subdirectories.")
    parser.add_argument("--num_images_to_read", type=int, default=5000, help="Number of images to read from the CSV file. Default is 5000.")
    args = parser.parse_args()

    animal_folders = ["leopard", "lion", "tiger"]
    
    tasks = [(animal, args.exp_dir, args.num_images_to_read) for animal in animal_folders]
    
    num_processes = min(multiprocessing.cpu_count(), len(animal_folders))

    with multiprocessing.Pool(num_processes) as pool:
        pool.map(create_gif_from_csv, tasks)
