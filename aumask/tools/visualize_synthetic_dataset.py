import cv2
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import imgviz


INPUT_PATH = '/home/seung/BOP/SAW/train'


file_names = sorted(os.listdir(os.path.join(INPUT_PATH + '/rgb')))

for file_name in file_names:
    img_id = file_name.split('.')[0]
    rgb = cv2.imread(os.path.join(INPUT_PATH, 'rgb', file_name))
    rgb = cv2.resize(rgb, (640, 480))
    rgb_noise = cv2.imread(os.path.join(INPUT_PATH, 'rgb_noise', file_name))
    rgb_noise = cv2.resize(rgb_noise, (640, 480))
    depth = cv2.imread(os.path.join(INPUT_PATH, 'depth', file_name))
    depth = cv2.resize(depth, (640, 480))
    visib_mask_paths = sorted(glob.glob(os.path.join(INPUT_PATH, 'visib_mask/') + img_id + '_*'))
    amodal_mask_paths = sorted(glob.glob(os.path.join(INPUT_PATH, 'amodal_mask/') + img_id + '_*'))
    
    instance_ids = []
    visib_masks = []
    for i, visib_mask_path in enumerate(visib_mask_paths):
        visib_mask = cv2.imread(visib_mask_path)
        visib_mask = cv2.resize(visib_mask, (640, 480))
        visib_mask = np.array(visib_mask[:, :, 0], dtype=np.bool)
        instance_ids.append(i)
        visib_masks.append(visib_mask)
        
    amodal_masks = []
    for i, amodal_mask_path in enumerate(amodal_mask_paths):
        amodal_mask = cv2.imread(amodal_mask_path)
        amodal_mask = cv2.resize(amodal_mask, (640, 480))
        amodal_mask = np.array(amodal_mask[:, :, 0], dtype=np.bool)
        amodal_masks.append(amodal_mask)
    instance_ids = list(range(len(instance_ids)))
    instviz = imgviz.instances2rgb(
        image = rgb,
        masks = visib_masks,
        labels = instance_ids,
        alpha = 0.5,
        line_width = 5,
        boundary_width = 1
    )

    amodalinstviz = imgviz.instances2rgb(
        image = rgb,
        masks = amodal_masks,
        labels = instance_ids,
        alpha = 0.5,
        line_width = 5,
        boundary_width = 1,
    )
    
    color_map = imgviz.label_colormap(len(instance_ids))
    for i, amodal_mask in enumerate(amodal_masks):
        if i == 0:
            amodalinstviz = rgb
        amodalinstviz = imgviz.instances2rgb(
            image = amodalinstviz,
            masks = [amodal_mask],
            labels = [instance_ids[i]],
            alpha = 0.9,
            line_width = 5,
            boundary_width = 1,
            colormap=np.uint8([(0,0,0), color_map[i]])
        )

    plt.figure(dpi=400)

    plt.subplot(3, 3, 1)
    plt.title("rgb")
    plt.imshow(rgb)
    plt.axis("off")

    plt.subplot(3, 3, 2)
    plt.title("rgb_noise")
    plt.imshow(rgb_noise)
    plt.axis("off")

    plt.subplot(3, 3, 3)
    plt.title("depth")
    plt.imshow(depth)
    plt.axis("off")

    plt.subplot(3, 3, 4)
    plt.title("instance")
    plt.imshow(instviz)
    plt.axis("off")
    
    plt.subplot(3, 3, 5)
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





