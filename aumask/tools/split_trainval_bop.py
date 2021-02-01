import os
import random

BOP_PATH = "/home/seung/BOP"
DATASETS = ("hb", "icbin", "icmi", "itodd", "lm", "ruapc", "tless", "tudl", "tyol", "ycbv")


TRAIN_RATIO = 0.8

for dataset in DATASETS:
    if dataset == "tless":
        object_ids = os.listdir(BOP_PATH + '/' + dataset + '/models_reconst')
    else:
        object_ids = os.listdir(BOP_PATH + '/' + dataset + '/models')
    object_ids = [x for x in object_ids if x.split('.')[-1]=="ply"]
    n_objects = len(object_ids)
    print("{}: {} objects".format(dataset, n_objects))
    random.shuffle(object_ids)
    n_train = int(n_objects * TRAIN_RATIO)
    n_val = n_objects - n_train
    print("n_train: {}, n_val: {}".format(n_train, n_val))
    train_object_ids = object_ids[:n_train]
    val_object_ids = object_ids[n_train:]

    with open(BOP_PATH + '/' + dataset + "/train_obj.txt", 'w') as f:
        for obj_id in train_object_ids:
            f.write(obj_id + '\n')
    with open(BOP_PATH + '/' + dataset + "/val_obj.txt", 'w') as f:
        for obj_id in val_object_ids:
            f.write(obj_id + '\n')





    