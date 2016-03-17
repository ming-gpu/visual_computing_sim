# -*- coding: utf-8 -*-
"""

Installation of needed libraries

sudo apt-get install -y python-pip
sudo pip install PIL numpy

"""

import os, time, math, operator
from numpy import average, linalg, dot
from PIL import Image
import numpy
import functools
import logging

format = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s() - %(message)s'
format = '%(asctime)s - %(filename)s:%(lineno)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=format)
logger = logging.getLogger(__name__)

img_cache_dict={}


def main():
    begin_similarty_compare('photos')


def begin_similarty_compare(photo_directory):
    image_filepath1 = '/tue/Q3_VISUAL_COMPUTING/similarity/photos/GED0000.JPG'
    image_filepath2 = '/tue/Q3_VISUAL_COMPUTING/similarity/photos/GED0001.JPG'

    t1 = time.time()

    similarity = histogram_similarity(image_filepath1, image_filepath2)

    duration = "%0.1f" % ((time.time() - t1) * 1000)
    logger.debug("Histogram distance => %s took %s ms" % (similarity, duration))


    t1 = time.time()

    similarity = histogram_similarity(image_filepath1, image_filepath2)

    duration = "%0.1f" % ((time.time() - t1) * 1000)
    logger.debug("Histogram distance => %s took %s ms" % (similarity, duration))

    t1 = time.time()
    similarity = pixel_cosine_similarity(image_filepath1, image_filepath2)
    duration = "%0.1f" % ((time.time() - t1) * 1000)
    logger.debug("Cosine distance %s took %s ms" % (similarity, duration))

    t1 = time.time()
    similarity = pixel_cosine_similarity(image_filepath1, image_filepath2)
    duration = "%0.1f" % ((time.time() - t1) * 1000)
    logger.debug("Cosine distance %s took %s ms" % (similarity, duration))


def histogram_similarity(p1_path, p2_path):

    resize_size = (50,50)

    if p1_path in img_cache_dict:
        imgA = img_cache_dict[p1_path]
    else:
        imgA = Image.open(p1_path)
        imgA = imgA.resize(resize_size)
        img_cache_dict[p1_path] = imgA
        print("adding to cache: "+p1_path)

    if p2_path in img_cache_dict:
        imgB = img_cache_dict[p2_path]
    else:
        imgB = Image.open(p2_path)
        imgB = imgB.resize(resize_size)
        img_cache_dict[p2_path] = imgB
        print("adding to cache: "+p2_path)

    h1 = imgA.histogram()
    h2 = imgB.histogram()

    rms = math.sqrt(functools.reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    return rms


def pixel_cosine_similarity(p1_path, p2_path):

    resize_size = (50,50)

    if p1_path in img_cache_dict:
        imgA = img_cache_dict[p1_path]
    else:
        imgA = Image.open(p1_path)
        imgA = imgA.resize(resize_size)
        img_cache_dict[p1_path] = imgA
        print("adding to cache: "+p1_path)

    if p2_path in img_cache_dict:
        imgB = img_cache_dict[p2_path]
    else:
        imgB = Image.open(p2_path)
        imgB = imgB.resize(resize_size)
        img_cache_dict[p2_path] = imgB
        print("adding to cache: "+p2_path)

    resize_size = (50,50)

    if p1_path in img_cache_dict:
        imgA = img_cache_dict[p1_path]
    else:
        imgA = Image.open(p1_path)
        imgA = imgA.resize(resize_size)
        img_cache_dict[p1_path] = imgA
        print("adding to cache: "+p1_path)

    if p2_path in img_cache_dict:
        imgB = img_cache_dict[p2_path]
    else:
        imgB = Image.open(p2_path)
        imgB = imgB.resize(resize_size)
        img_cache_dict[p2_path] = imgB
        print("adding to cache: "+p2_path)

    images = [imgA, imgB]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in image.getdata():
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    res = dot(a / a_norm, b / b_norm)
    return res


def get_thumbnail(image, size=(10, 10), stretch_to_fit=False, greyscale=False):
    " get a smaller version of the image - makes comparison much faster/easier"
    if not stretch_to_fit:
        image.thumbnail(size, Image.ANTIALIAS)
    else:
        image = image.resize(size);  # for faster computation
    if greyscale:
        image = image.convert("L")  # Convert it to grayscale.
    return image


if __name__ == "__main__":
    main()