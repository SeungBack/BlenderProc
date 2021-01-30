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

OBJECT_MODEL_PATH = '/home/seung/BOP'
OUTPUT_PATH = '/home/seung/BOP'
# DATASETS = (
#     'hb', 'icmi', 'lm', 'kit',
#     'ruapc', 'tless', 'tudl', 'tyol', 'ycbv',
# )
DATASETS = (
    'ruapc', 'ycbv',
)

if __name__ == "__main__":

    # get mesh paths
    obj_mesh_paths = {}
    for dataset in DATASETS:
        if dataset == 'tless':
            paths = sorted(glob.glob(OBJECT_MODEL_PATH + '/' + dataset + '/models_cad/*.ply'))
        else:
            paths = sorted(glob.glob(OBJECT_MODEL_PATH + '/' + dataset + '/models/*.ply'))
        
        # exclude objects of WISDOM-Real-test
        if dataset == 'ycbv':
            paths.remove(OBJECT_MODEL_PATH + '/' + dataset + '/models/obj_000010.ply') # 011_banana
        elif dataset == 'ruapc':
            paths.remove(OBJECT_MODEL_PATH + '/' + dataset + '/models/obj_000003.ply') # crayola crayon
            paths.remove(OBJECT_MODEL_PATH + '/' + dataset + '/models/obj_000004.ply') # school glue

        # visualization
        imgs = []
        print("Loading", dataset)
        for path in tqdm(paths):
            import open3d
            open3d.visualization.draw([ open3d.io.read_triangle_mesh(path)])
            exit()

            mesh = trimesh.load(path)    
            mesh.show()
            if "dataset" == "kit":
                mesh.visual = mesh.visual.to_color()
            scene = mesh.scene()
            window_conf = gl.Config(double_buffer=True, depth_size=24)
            img = scene.save_image(resolution=[128, 128], visible=True, window_conf=window_conf)
            img = np.array(Image.open(BytesIO(img)).convert('RGB'))
            imgs.append(img)
        
        tiled = imgviz.tile(imgs=imgs, border=(255, 255, 255), cval=(255, 255, 255))
        plt.figure(dpi=500)
        plt.title(dataset)
        plt.imshow(tiled)
        plt.axis("off")
        img = imgviz.io.pyplot_to_numpy()
        plt.close()
        cv2.imwrite(OUTPUT_PATH + '/' + dataset + '.png', img)


    