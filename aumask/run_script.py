import os, sys
import numpy as np
import argparse
import yaml
import subprocess
import random
from tqdm import tqdm

BOP_PATH = os.environ['BOP_PATH']
BOP_TOOLKIT_PATH = os.path.join(BOP_PATH, "bop_toolkit")
BLENDERPROC_PATH = "/home/seung/Workspace/papers/2021/AUMask/BlenderProc"
DATASETS = ("hb", "icbin", "icmi", "itodd", "lm", "ruapc", "tless", "tudl", "tyol", "ycbv")
TEXTURE_PATH = BLENDERPROC_PATH + "/resources/cctextures"
OUTPUT_PATH = BLENDERPROC_PATH + "/aumask/output"

 
def get_obj_id_by_idx(obj_id_dict, obj_idx):
    idx = 0
    for dataset in DATASETS:
        for obj_id in obj_id_dict[dataset]:
            if obj_idx == idx:
                return obj_id, dataset
            else:
                idx += 1

def build_bop_loader(bop_path, dataset_name, n_objs_to_sample, obj_ids, smooth_shading=True):

    bop_loader = {
        "module": "loader.BopLoader",
        "config": {
            "bop_dataset_path": "{}/{}".format(bop_path, dataset_name),
            "model_type": "",
            "mm2m": True,
            "sample_objects": True,
            "num_of_objs_to_sample": n_objs_to_sample,
            "obj_ids": obj_ids,
            "add_properties": {
            "cp_physics": True
            },
        }
    }
    if smooth_shading:
        bop_loader["config"]["cf_set_shading"] = "SMOOTH"
    return bop_loader

def build_color_material_manipulator(dataset_name,  grey=False):
    return {
      "module": "manipulators.MaterialManipulator",
      "config": {
        "selector": {
          "provider": "getter.Material",
          "conditions": [
          {
            "name": "bop_{}_vertex_col_material.*".format(dataset_name)
          }
          ]
        },
        "cf_set_base_color": {
          "provider": "sampler.Color",
          "grey": grey,
          "min": [0.1, 0.1, 0.1, 1.0],
          "max": [0.9, 0.9, 0.9, 1.0]
        }
      }
    }

def build_specular_rougness_material_manipulator(dataset_names):
    conditions = []
    for dataset_name in dataset_names:
        conditions.append({"name": "bop_{}_vertex_col_matrial.*".format(dataset_name)})
    return {
        "module": "manipulators.MaterialManipulator",
        "config": {
        "selector": {
            "provider": "getter.Material",
            "conditions": conditions
        },
        "cf_set_specular": {
            "provider": "sampler.Value",
            "type": "float",
            "min": 0.0,
            "max": 1.0
        },
        "cf_set_roughness": {
            "provider": "sampler.Value",
            "type": "float",
            "min": 0.0,
            "max": 1.0
        }
        }
    }



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="train", help="train or val")
    parser.add_argument("--start_seq", type=int, default=0, help="sequence number")
    parser.add_argument("--end_seq", type=int, default=1, help="sequence number")
    parser.add_argument("--n_images_per_seq", type=int, default=25, help="sequence number")
    args = parser.parse_args()

    for seq in tqdm(range(args.start_seq, args.end_seq)):
        with open("aumask/configs/template.yaml") as f:
            cfg = yaml.safe_load(f)
        
        # load obj_ids
        obj_id_dict = {}
        render_obj_id_dict = {}
        n_obj = 0
        for dataset in DATASETS:
            idx_path = os.path.join(BOP_PATH, dataset, args.mode + "_obj.txt")
            with open(idx_path) as f:
                file_names = f.readlines()
                obj_ids = []
                for file_name in file_names:
                    obj_id = file_name.split('.')[0][-2:]
                    obj_ids.append(int(obj_id))
                    n_obj += 1
                obj_id_dict[dataset] = sorted(obj_ids)
            render_obj_id_dict[dataset] = []
        print("==>", args.mode, "obj_id_dict \n", obj_id_dict)
        
        # decide the number of objects to render for each dataset
        total_num_of_sample_objs = random.randint(15, 30)
        obj_idexes = np.random.choice(list(range(n_obj)), total_num_of_sample_objs)
        for obj_idx in obj_idexes:
            obj_id, dataset = get_obj_id_by_idx(obj_id_dict, obj_idx)
            render_obj_id_dict[dataset].append(obj_id)
        print("==> total number of sample objects:", total_num_of_sample_objs)
        print("==> target render object \n", render_obj_id_dict)


        CONFIG_PATH = BLENDERPROC_PATH + "/aumask/configs/{}.yaml".format(seq)

        # save configuration file

        # 1. initialize
        modules = []
        initialier = {
        "module": "main.Initializer",
        "config": {
            "global": {
            "output_dir": OUTPUT_PATH,
            "sys_paths": [CONFIG_PATH]
            }
        }
        }
        modules.append(initialier)

        # 2. load bop dataset
        for dataset in DATASETS:
            obj_ids = render_obj_id_dict[dataset]
            n_objs_to_sample = len(obj_ids)
            bop_loader = build_bop_loader(BOP_PATH, dataset, n_objs_to_sample, obj_ids)
            modules.append(bop_loader)

        # 3. material
        modules.append(build_color_material_manipulator("tless"))
        modules.append(build_color_material_manipulator("itodd"))
        modules.append(build_specular_rougness_material_manipulator(list(DATASETS)))

        for module in reversed(modules):
            cfg["modules"].insert(0, module)

        with open("aumask/configs/{}.yaml".format(seq), 'w') as f:
            yaml.dump(cfg, f)
        
        arguments = [CONFIG_PATH, BOP_PATH, TEXTURE_PATH, str(args.n_images_per_seq)]
        command = "python {}/run.py".format(BLENDERPROC_PATH)
        for argument in arguments:
            command += " "
            command += argument
        print("====>", command)
        subprocess.run(command, shell=True)