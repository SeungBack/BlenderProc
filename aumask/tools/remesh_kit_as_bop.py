import glob
import os
import trimesh
from tqdm import tqdm
from plyfile import PlyData, PlyElement


# load kit object models and convert it to bop format
KIT_PATH = '/home/seung/Workspace/datasets/UOIS/object_models/kit/unzips'
OUTPUT_PATH = '/home/seung/BOP/kit'

no_materials = ['SmallGlass', 'WhiteCup', 'Pitcher', 'Sprayflask', 'CokePlasticLarge', 
                'CokePlasticSmall', 'VitalisCereals', 'SmacksCereals', 'CoffeeFilters', 
                'ChoppedTomatoes', 'Wineglass', 'Waterglass', 'Glassbowl', 'Pinsel', 'Schraubenschluessel']
                # Schlitzschraubenzieher ==> texture error when convert texture to vertex color

if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

id = 1
for i, obj_folder in enumerate(tqdm(sorted(glob.glob(KIT_PATH + '/*')))):
    paths = sorted(glob.glob(obj_folder + '/meshes/*_tex.obj'))
    if len(paths) == 0:
        print("no unzip files in ", obj_folder)
        continue
    object_name = paths[0].split('/')[-1].split('_')[0]
    file_name = 'obj_{:06d}.ply'.format(id)

    if object_name in no_materials:
        print("No material files. Skip", object_name)
        continue
    else:
        id += 1
        target_paths = []
        for p in paths:
            if "Orig" in p:
                target_paths.append(p)
            elif "25k" in p:
                target_paths.append(p)
        target_path = target_paths[-1]
        
    # load mesh and convert uv texture to vertex color
    # load mesh and convert uv texture to vertex color
    mesh = trimesh.load_mesh(target_path)
    mesh.visual = mesh.visual.to_color()
    mesh.export(OUTPUT_PATH + '/models/tmp.ply')
    with open(OUTPUT_PATH + '/models/tmp.ply', 'rb') as f:
        plydata = PlyData.read(f)
        PlyData(plydata.elements, text=True).write(OUTPUT_PATH + '/models/' + file_name)
    print("Converted ", object_name, file_name)
    os.remove(OUTPUT_PATH + '/models/tmp.ply')
    with open(OUTPUT_PATH + '/object_id_to_name.txt', 'a') as f:
        f.write("{},{}\n".format(file_name, object_name))


