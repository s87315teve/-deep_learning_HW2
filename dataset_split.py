import random
import os
import subprocess


dataset_folder="train_augmentation"
train_folder="~/Desktop/espnet/egs2/aishell/asr1/downloads/data_aishell/wav/train/global"
dev_folder="~/Desktop/espnet/egs2/aishell/asr1/downloads/data_aishell/wav/dev/global"

file_list=[f for f in os.listdir(dataset_folder)]
random.shuffle(file_list)



dev_rate=0.2
split_flag=int(len(file_list)*dev_rate)
print(split_flag)
for i in range(len(file_list)):
    if split_flag>=i:
        subprocess.getstatusoutput("cp {}/{} {}/{}".format(dataset_folder, file_list[i], dev_folder, file_list[i]))
    else:
        subprocess.getstatusoutput("cp {}/{} {}/{}".format(dataset_folder, file_list[i], train_folder,file_list[i]))