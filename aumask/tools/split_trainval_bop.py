import os
import random

BOP_PATH = "/home/seung/BOP"
DATASETS = ("lm", "tless", "tudl", "icmi", "tyol",  "ruapc", "itodd", "hb", "ycbv", "kit", "bigbird")


TRAIN_RATIO = 0.8

n_train_total = 0
n_val_total = 0
for dataset in DATASETS:
    if dataset == "tless":
        object_ids = os.listdir(BOP_PATH + '/' + dataset + '/models_reconst')
    else:
        object_ids = os.listdir(BOP_PATH + '/' + dataset + '/models')
    object_ids = sorted([x for x in object_ids if x.split('.')[-1]=="ply"])

    if dataset == "ruapc":
        object_ids.remove('obj_000003.ply') # Crayola in WISDOM-Real-test
        object_ids.remove('obj_000004.ply') # Schoool Glue in WISDOM-Real-test 
        object_ids.remove('obj_000005.ply') # Expo in APC-MT
    elif dataset == "hb":
        object_ids.remove('obj_000002.ply') # 2 in LINEMOD
        object_ids.remove('obj_000007.ply') # 8 in LINEMOD
        object_ids.remove('obj_000021.ply') # 15 in LINEMOD
    elif dataset == "ycbv":
        object_ids.remove('obj_000010.ply') # Banana in WISDOM-Real-test
    # KIT, BigBird => redundant ply files were removed in pre-processing stage

    n_objects = len(object_ids)
    print("{}: {} objects".format(dataset, n_objects))
    random.shuffle(object_ids)
    n_train = round(n_objects * TRAIN_RATIO)
    n_val = n_objects - n_train
    n_train_total += n_train
    n_val_total += n_val
    print("n_train: {}, n_val: {}".format(n_train, n_val))
    train_object_ids = object_ids[:n_train]
    val_object_ids = object_ids[n_train:]

    with open(BOP_PATH + '/' + dataset + "/train_obj.txt", 'w') as f:
        for obj_id in train_object_ids:
            f.write(obj_id + '\n')
    with open(BOP_PATH + '/' + dataset + "/val_obj.txt", 'w') as f:
        for obj_id in val_object_ids:
            f.write(obj_id + '\n')

print("total train", n_train_total, "total val", n_val_total)




    