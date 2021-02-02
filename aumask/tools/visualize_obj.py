import os
import random
import glob
# import trimesh
import imgviz
from pyglet import gl
from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm
import vedo
from PIL import Image, ImageChops

def trim(im, border):
  bg = Image.new(im.mode, im.size, border)
  diff = ImageChops.difference(im, bg)
  bbox = diff.getbbox()
  if bbox:
    return im.crop(bbox)

def create_thumbnail(path, size):
  image = Image.open(path)
  name, extension = path.split('.')
  options = {}
  if 'transparency' in image.info:
    options['transparency'] = image.info["transparency"]
  
  image.thumbnail((size, size), Image.ANTIALIAS)
  image = trim(image, 255) ## Trim whitespace
  return image

OBJECT_MODEL_PATH = '/home/seung/BOP'
OUTPUT_PATH = '/home/seung/BOP'
DATASETS = ("lm", "tless", "tudl", "icmi", "tyol",  "ruapc", "itodd", "hb", "ycbv", "kit", "bigbird")

if __name__ == "__main__":

    # get mesh paths
    obj_mesh_paths = {}
    for dataset in DATASETS:
        if dataset == 'tless':
            paths = sorted(glob.glob(OBJECT_MODEL_PATH + '/' + dataset + '/models_reconst/*.ply'))
        else:
            paths = sorted(glob.glob(OBJECT_MODEL_PATH + '/' + dataset + '/models/*.ply'))
        
        # exclude objects of WISDOM-Real-test
        if dataset == 'ycbv':
            paths.remove(OBJECT_MODEL_PATH + '/' + dataset + '/models/obj_000002.ply') # 
            paths.remove(OBJECT_MODEL_PATH + '/' + dataset + '/models/obj_000010.ply') # 011_banana

        elif dataset == 'ruapc':
            paths.remove(OBJECT_MODEL_PATH + '/' + dataset + '/models/obj_000003.ply') # crayola crayon
            paths.remove(OBJECT_MODEL_PATH + '/' + dataset + '/models/obj_000004.ply') # school glue
            paths.remove(OBJECT_MODEL_PATH + '/' + dataset + '/models/obj_000005.ply') # school glue
        elif dataset == 'hb':
            paths.remove(OBJECT_MODEL_PATH + '/' + dataset + '/models/obj_000002.ply') # crayola crayon
            paths.remove(OBJECT_MODEL_PATH + '/' + dataset + '/models/obj_000007.ply') # crayola crayon
            paths.remove(OBJECT_MODEL_PATH + '/' + dataset + '/models/obj_000021.ply') # crayola crayon

        # visualization
        imgs = []
        print("Loading", dataset)
        for path in tqdm(paths):

            m = vedo.load(path)
            if dataset in ["ycbv", "ruapc", "kit", "bigbird"]:
                m = m.texture(path[:-3] + "png")

            m.show(interactive=False, viewup='z')
            vedo.screenshot('tmp.png')

            img = create_thumbnail('tmp.png', 256)
            imgs.append(np.uint8(img))
        
        tiled = imgviz.tile(imgs=imgs, border=(255, 255, 255), cval=(255, 255, 255))
        plt.figure(dpi=700)
        plt.title(dataset)
        plt.imshow(tiled)
        plt.axis("off")
        img = imgviz.io.pyplot_to_numpy()
        plt.close()
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(OUTPUT_PATH + '/' + dataset + '.png', img)


    