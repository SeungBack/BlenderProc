import cv2
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import imgviz


OUTPUT_PATH = '/home/seung/Workspace/datasets/UOIS/aumask/bop_data/train_pbr/000000'


file_names = sorted(os.listdir(os.path.join(OUTPUT_PATH + '/rgb')))

for file_name in file_names:
    rgb = cv2.imread(os.path.join(OUTPUT_PATH, 'rgb', file_name))
    depth = cv2.imread(os.path.join(OUTPUT_PATH, 'depth', file_name))
    modal_mask_paths = sorted(glob.glob(os.path.join(OUTPUT_PATH, 'mask_visib/') + file_name[:-4] + '_*'))
    amodal_mask_paths = sorted(glob.glob(os.path.join(OUTPUT_PATH, 'mask/') + file_name[:-4] + '_*'))
    
    # obj_ids = np.unique(instance_mask)[1:]
    # mask = instance_mask[:, :, 0]
    # masks = mask == obj_ids[:, None, None]

    obj_ids = []
    modal_masks = []
    for i, modal_mask_path in enumerate(modal_mask_paths):
        modal_mask = np.array(cv2.imread(modal_mask_path)[:, :, 0], dtype=np.bool)
        if np.sum(modal_mask) != 0:
            obj_ids.append(i)
            modal_masks.append(modal_mask)

    amodal_masks = []
    for i, amodal_mask_path in enumerate(amodal_mask_paths):
        amodal_mask = np.array(cv2.imread(amodal_mask_path)[:, :, 0], dtype=np.bool)
        if np.sum(amodal_mask) != 0 and i in obj_ids:
            amodal_masks.append(amodal_mask)
    obj_ids = list(range(len(obj_ids)))

    instviz = imgviz.instances2rgb(
        image = rgb,
        masks = modal_masks,
        labels = obj_ids,
        alpha = 0.7,
        line_width = 3,
        boundary_width = 3
    )

    amodalinstviz = imgviz.instances2rgb(
        image = rgb,
        masks = amodal_masks,
        labels = obj_ids,
        alpha = 0.7,
        line_width = 3,
        boundary_width = 3
    )


    plt.figure(dpi=500)

    plt.subplot(2, 2, 1)
    plt.title("rgb")
    plt.imshow(rgb)
    plt.axis("off")

    plt.subplot(2, 2, 2)
    plt.title("depth")
    plt.imshow(depth)
    plt.axis("off")

    plt.subplot(2, 2, 3)
    plt.title("instance")
    plt.imshow(instviz)
    plt.axis("off")
    
    plt.subplot(2, 2, 4)
    plt.title("amodal")
    plt.imshow(amodalinstviz)
    plt.axis("off")


    img = imgviz.io.pyplot_to_numpy()
    h, w, _ = img.shape
    cv2.putText(img, file_name, (int(0.75*w), int(0.75*h)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, "n: next image / q: quit", (int(0.75*w), int(0.8*h)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow('test.png', img)
    cv2.imwrite('test.png', img)
    
    while True:
        if cv2.waitKey(0) == ord('q'):
            exit()
        elif cv2.waitKey(0) == ord('n'):
            cv2.destroyAllWindows()
            plt.close()
            break





