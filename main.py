from PIL import Image
import os
import imagehash

# Define a histogram function to compare two images
def images_are_similar_histogram(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    return image1.histogram() == image2.histogram()

# Define a function to compare two images
def images_are_similar_hash(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    hash1 = imagehash.average_hash(image1)
    hash2 = imagehash.average_hash(image2)
    return hash1 == hash2

# Define a function to delete similar images and write to a log file
def delete_similar_images(directory, log_file_path):
    image_paths = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')]
    with open(log_file_path, "w") as log_file:
        for i in range(len(image_paths)):
            for j in range(i+1, len(image_paths)):
                if images_are_similar_histogram(image_paths[i], image_paths[j]):
                    #os.remove(image_paths[j])
                    log_file.write(f"Similar images found (histogram): {image_paths[i]} and {image_paths[j]}\n")
                if images_are_similar_hash(image_paths[i], image_paths[j]):
                    #os.remove(image_paths[j])
                    log_file.write(f"Similar images found (hash): {image_paths[i]} and {image_paths[j]}\n")

# Example usage
delete_similar_images("/space/tomcat/LangLab/experiments/study_3_pilot/group/exp_2023_02_21_14/lion/face_images", "similar_images.log")