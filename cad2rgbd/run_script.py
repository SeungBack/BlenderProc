import os, sys
import numpy as np
import argparse
import yaml
import subprocess
import random
from tqdm import tqdm
from tools.cfg_builder import *
import glob
from pathlib import Path
import math

num_of_objects_per_datasets = {
    "lm": 15,
    "tless": 30,
    "tudl": 3,
    "icmi": 6,
    "tyol": 21,
    "ruapc": 11,
    "itodd": 28,
    "hb": 30,
    "ycbv": 20,
    "kit": 121,
    "bigbird": 110,
}


def get_num_of_objs_to_sample_per_dataset(opt, num_of_objs_to_sample):
    
    n_objs = []
    n_total = 0
    for dataset_name in opt["dataset_names"]:
        n_obj = num_of_objects_per_datasets[dataset_name]
        n_objs.append(n_obj)
        n_total += n_obj
    weights = [n_obj/n_total for n_obj in n_objs]
    choices = np.random.choice(opt["dataset_names"], num_of_objs_to_sample, p=weights)
    num_of_objs_to_sample_per_dataset = {}
    for dataset_name in opt["dataset_names"]:
        num_of_objs_to_sample_per_dataset[dataset_name] = int(np.sum(np.where(choices==dataset_name, 1, 0)))
        print(num_of_objs_to_sample, dataset_name, num_of_objs_to_sample_per_dataset[dataset_name])
    return num_of_objs_to_sample_per_dataset

def get_camera_intrinsic_matrix(opt):

    min_f = opt["camera"]["focal_length"]["min"]
    max_f = opt["camera"]["focal_length"]["max"]
    mean_cx = float(opt["camera"]["resolution"]["x"]-1) / 2 
    mean_cy = float(opt["camera"]["resolution"]["y"]-1) / 2 
    min_delta_c = opt["camera"]["delta_optical_center"]["min"]
    max_delta_c = opt["camera"]["delta_optical_center"]["max"]
    min_cx = mean_cx + min_delta_c
    max_cx = mean_cx + max_delta_c
    min_cy = mean_cy + min_delta_c
    max_cy = mean_cy + max_delta_c


    focal = random.uniform(min_f, max_f)
    cx = random.uniform(min_cx, max_cx)
    cy = random.uniform(min_cy, max_cy)

    K = [focal, 0, cx, 0, focal, cy, 0, 0, 1]

    opt["camera"]["cam_K"] = K
    return opt

def get_target_obj_ids(opt):

    object_idexes = {}
    for dataset_name in opt["dataset_names"]:
        idx_path = os.path.join(opt["bop_path"], dataset_name, opt["mode"] + "_obj.txt")
        model_type = "models_cad" if dataset_name == "tless" else "models"
        object_idexes[dataset_name] = []
        with open(idx_path) as f:
            for file_name in f.readlines():
                object_idx = int(file_name.split('.')[0].split('_')[1])
                object_idexes[dataset_name].append(object_idx)
    return object_idexes

if __name__ == "__main__":

    # load args and opt 
    parser = argparse.ArgumentParser()
    parser.add_argument("--opt", type=str, default="test", help="file name of opt file")
    parser.add_argument("--pid", type=int, default=1, help="process id")
    args = parser.parse_args()
    file_path = Path(__file__).parent.absolute()
    opt_path = os.path.join(file_path, "opts/{}.yaml".format(args.opt))
    with open(opt_path, 'r') as f:
        opt = yaml.safe_load(f)
    
    print("Rendering options: \n", opt)
    opt["output_path"] = os.path.join(opt["output_path"], args.opt + '_' + str(args.pid))
    print("Saving to", opt["output_path"])
    os.makedirs(opt["output_path"], exist_ok=True) 

    for seq in tqdm(range(opt["start_seq"], opt["end_seq"])):
        
        # load target obj_ids
        total_num_of_sample_objs = np.random.poisson(lam=opt["object"]["num_of_sample_objs"]["lam"])
        total_num_of_sample_objs = int(np.clip(total_num_of_sample_objs,
                                        opt["object"]["num_of_sample_objs"]["min"], 
                                        opt["object"]["num_of_sample_objs"]["max"]))
        num_of_objs_to_sample_per_dataset = get_num_of_objs_to_sample_per_dataset(opt, total_num_of_sample_objs)
        object_idexes = get_target_obj_ids(opt)

        opt = get_camera_intrinsic_matrix(opt)

        # save configuration file
        cfg_path = os.path.join(file_path, "cfgs/{}_{}.yaml".format(args.opt, seq))
        print("==>", cfg_path)
        cfg = initialize_cfg(opt["output_path"], cfg_path)
        modules = []
        # Load bop dataset
        for dataset_name, num_of_objs_to_sample in num_of_objs_to_sample_per_dataset.items():
            modules += build_bop_loader(opt, dataset_name, num_of_objs_to_sample, object_idexes[dataset_name])
        if opt["bin"]["is_used"]:
            modules += build_bin_loader(opt)
        modules += build_plane_loader(opt)
        modules += build_object_pose_sampler(opt)
        modules += build_light_sampler(opt)
        modules += build_camera_sampler(opt)
        modules += build_object_material_manipulator(opt)
        modules += build_rgb_render(opt)
        modules += build_bop_writer(opt)
        cfg["modules"] += modules

        with open(cfg_path, 'w') as f:
            yaml.dump(cfg, f)
        
        command = "python {}/run.py {}".format(opt["blenderproc_path"], cfg_path)
        print("========> ", command)
        subprocess.run(command, shell=True)