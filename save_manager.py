import shutil
import os

def file_collector(rel_path):
    for filename in os.listdir(rel_path):
        f = os.path.join(rel_path, filename)
        if os.path.isfile(f):
            file_mover(f)

def file_mover(f):
    dest = "local_" + f
    a = dest.split('/')
    if len(a) > 2:
        a[1] = "local_" + a[1]
    dest = "/".join(a)
    shutil.copyfile(f, dest)

file_collector("assets/")
file_collector("assets/enemies/")