import os


train_imgs = 0
for i in range(1, 13):
    train_imgs += int(os.popen('find ~/BOP/synthetic/bopkitbigbird-bin-train_{}/bop_data/train_pbr/000000/rgb -type f | wc -l'.format(i)).read())
    train_imgs += int(os.popen('find ~/BOP/synthetic/bopkitbigbird-bin-train_{}/bop_data/train_pbr/000001/rgb -type f | wc -l'.format(i)).read())
    train_imgs += int(os.popen('find ~/BOP/synthetic/bopkitbigbird-tabletop-train_{}/bop_data/train_pbr/000000/rgb -type f | wc -l'.format(i)).read())
    train_imgs += int(os.popen('find ~/BOP/synthetic/bopkitbigbird-tabletop-train_{}/bop_data/train_pbr/000001/rgb -type f | wc -l'.format(i)).read())

val_imgs = 0
for i in range(1, 3):
    val_imgs += int(os.popen('find ~/BOP/synthetic/bopkitbigbird-bin-val_{}/bop_data/train_pbr/000000/rgb -type f | wc -l'.format(i)).read())
    val_imgs += int(os.popen('find ~/BOP/synthetic/bopkitbigbird-bin-val_{}/bop_data/train_pbr/000001/rgb -type f | wc -l'.format(i)).read())
    val_imgs += int(os.popen('find ~/BOP/synthetic/bopkitbigbird-tabletop-val_{}/bop_data/train_pbr/000000/rgb -type f | wc -l'.format(i)).read())
    val_imgs += int(os.popen('find ~/BOP/synthetic/bopkitbigbird-tabletop-val_{}/bop_data/train_pbr/000001/rgb -type f | wc -l'.format(i)).read())



print(train_imgs, val_imgs)


