import glob
import yaml
import os 


bop_path = "/home/seung/BOP"
dataset_names = ["hb", "icmi", "itodd", "lm", "ruapc", "tless", "tudl", "tyol", "ycbv", "kit"]
output_path = "/home/seung/BOP/synthetic/path_to_category_id.yaml"
path_to_category = {}
category_id = 0


for dataset_name in dataset_names:
    model_type = "models_cad" if dataset_name == "tless" else "models"
    model_paths = sorted(glob.glob(bop_path + '/' + dataset_name + '/' + model_type + '/*.ply'))
    for model_path in model_paths:
        model_path = model_path.split('/')[4:]
        model_path = '/'.join(model_path)
        category_id += 1
        path_to_category[model_path] = category_id

with open(output_path, 'w') as f:
    yaml.dump(path_to_category, f)

