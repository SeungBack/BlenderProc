import glob
import os
import trimesh
from tqdm import tqdm
from plyfile import PlyData, PlyElement
import numpy as np

# load kit object models and convert it to bop format
INPUT_PATH = '/home/seung/BOP/3dnet/models_original'
OUTPUT_PATH = '/home/seung/BOP/3dnet'

id = 1
object_files = sorted(glob.glob(INPUT_PATH + '/*.obj'))


for i, object_file in enumerate(tqdm(object_files)):
    object_name = object_file.split('/')[-1]
    file_name = 'obj_{:06d}.ply'.format(id)
    id += 1
    mesh = trimesh.load_mesh(object_file)
    mesh.apply_scale(1000)
    mesh.export(OUTPUT_PATH + '/models/tmp.ply')
    with open(OUTPUT_PATH + '/models/tmp.ply', 'rb') as f:
        plydata = PlyData.read(f)
        PlyData(plydata.elements, text=True).write(OUTPUT_PATH + '/models/' + file_name)
    print("Converted ", object_name, file_name)
    os.remove(OUTPUT_PATH + '/models/tmp.ply')
    with open(OUTPUT_PATH + '/object_id_to_name.txt', 'a') as f:
        f.write("{},{}\n".format(file_name, object_name))
    if i== 30:
        break
    


