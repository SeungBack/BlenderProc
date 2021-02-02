import glob
import os
import numpy as np
import pymeshlab
from tqdm import tqdm

# load kit object models and convert it to bop format
INPUT_PATH = '/home/seung/BOP/backup/processed'
OUTPUT_PATH = '/home/seung/BOP/bigbird'


BOP_PATH = "/home/seung/BOP"
DATASETS = ("kit", "bigbird")


for dataset in DATASETS:
    if dataset == "tless":
        object_ids = os.listdir(BOP_PATH + '/' + dataset + '/models_reconst')
    else:
        object_ids = os.listdir(BOP_PATH + '/' + dataset + '/models')
    object_ids = sorted([x[:-4] for x in object_ids if x.split('.')[-1]=="ply"])
    for object_id in tqdm(object_ids):
        ply_path = BOP_PATH + '/' + dataset + '/models/' + object_id + '.ply'
        obj_path = BOP_PATH + '/' + dataset + '/models/' + object_id + '.obj'

        ms = pymeshlab.MeshSet()
        ms.load_new_mesh(ply_path)
        ms.save_current_mesh(obj_path)