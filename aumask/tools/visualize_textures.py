import glob
import cv2
import os

cctexture_path = "/home/seung/Workspace/papers/2021/AUMask/BlenderProc/resources/cctextures"
keyword = "Fabric"

target_image_folders = []
for image_folder in glob.glob(cctexture_path + '/*'):
    if keyword in image_folder:
        target_image_folders.append(image_folder)



for i, image_folder in enumerate(sorted(target_image_folders)):
    print(image_folder)
    
    for img in glob.glob(image_folder + '/*'):
        if "Color" in img:
            color_img = img
    cv2.imshow(str(i), cv2.imread(color_img))
    while True:
        ch = cv2.waitKey()
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            exit()
        elif ch == ord('x'):
            print("remove", image_folder)
            os.system("rm -r {}".format(image_folder))
            cv2.destroyAllWindows() 
            break
        else:
            cv2.destroyAllWindows() 
            break

