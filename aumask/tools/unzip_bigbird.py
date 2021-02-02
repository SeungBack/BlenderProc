import os
import glob



# INPUT = "/home/seung/BOP/bigbird/original-2"
# OUTPUT = "/home/seung/BOP/bigbird/models"
# for zip in glob.glob(INPUT + '/*.zip'):
#     os.system("unzip {} -d {}".format(zip, OUTPUT))



# INPUT = "/home/seung/BOP/bigbird/models/export"

# for models in glob.glob(INPUT + '/*'):
#     try:
#         os.system("tar -xvf {}/processed.tgz -C {} --overwrite".format(models, models))
#     except:
#         with open("error.txt", "w") as f:
#             f.write('{}\n'.format(models))


A = os.listdir("/home/seung/BOP/bigbird/processed")

B = os.listdir("/home/seung/BOP/bigbird/models/export")

for a in A:
    B.remove(a)
print(B)