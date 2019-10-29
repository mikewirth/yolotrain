import os

p = "Annotations_HiRes/YOLO"
files = [f for f in  os.listdir(".") if 'txt' in f]
print(files)


#for file in files:
print(len(files))

n = int(len(files)*0.8)
train_set = files[:n]
valid_set = files[n:]

"""
for file in train_set:
    os.popen("cp %s train/%s"%(file, file))

for file in valid_set:
    os.popen("cp %s valid/%s"%(file, file))
"""

with open("train.txt", 'w') as f:
    for file in train_set:
        f.write(file[:-3]+'JPG\n')

with open("valid.txt", 'w') as f:
    for file in valid_set:
        f.write(file[:-3]+'JPG\n')

