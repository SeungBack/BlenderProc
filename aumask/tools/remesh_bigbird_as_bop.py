import glob
import os
import numpy as np
import pymeshlab
from tqdm import tqdm

# load kit object models and convert it to bop format
INPUT_PATH = '/home/seung/BOP/backup/processed'
OUTPUT_PATH = '/home/seung/BOP/bigbird'



if not os.path.exists(OUTPUT_PATH + '/models'):
    os.mkdir(OUTPUT_PATH+ '/models')
id = 1
for i, input_folder_path in enumerate(tqdm(sorted(glob.glob(INPUT_PATH + '/*')))):
    input_obj_path = input_folder_path + '/textured_meshes/optimized_poisson_texture_mapped_mesh.obj'
    input_texture_path = input_folder_path + '/textured_meshes/optimized_poisson_texture_mapped_mesh.png'
    object_name = input_folder_path.split('/')[-1]
    output_file_name = 'obj_{:06d}.ply'.format(id)
    output_ply_path = os.path.join(OUTPUT_PATH, 'models', output_file_name)
    output_png_name = 'obj_{:06d}.png'.format(id)
    output_png_path = os.path.join(OUTPUT_PATH, 'models', output_png_name)
    id += 1
    print("Processing", object_name, output_file_name)

    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_obj_path)
    ms.save_current_mesh(output_ply_path, binary=False, save_vertex_normal=True)
    with open(output_ply_path, 'r+') as f:
        lines = f.readlines()

    
    lines.insert(3, "comment TextureFile {}\n".format(output_png_name))
    with open(output_ply_path, 'r+') as f:
        f.writelines(lines)
    os.system("cp {} {}".format(input_texture_path, output_png_path))
   
    with open(OUTPUT_PATH + '/object_id_to_name.txt', 'a') as f:
        f.write("{},{}\n".format(output_file_name, object_name))

