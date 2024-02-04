from PIL import Image
from imagehash import average_hash
from pprint import pprint

def are_images_similar(image_path1, image_path2):
    hash1 = average_hash(Image.open(image_path1))
    hash2 = average_hash(Image.open(image_path2))
    return hash1 == hash2, hash1, hash2