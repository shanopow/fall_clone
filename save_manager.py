# Module imports
import shutil
import os
import json

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

# Function for deleting file from local so we can refresh it back to original state
def file_deleter(to_delete):
    os.remove(to_delete)

# Function to take list of enemies and remove from the loaded json
# Will make the locals unreadable but orig in assets still fine as not modified at all
def file_modifier(save_prefix, to_modify, file, map_location):
    file = save_prefix + file
    f = open(file)
    raw = json.load(f)
    found_it = raw["vault1"][map_location]["enemies"]
    #print(found_it.items())
    for item in to_modify:
        if item.form_id in found_it.values():
            found_it.pop(list(found_it.keys())[list(found_it.values()).index(item.form_id)])
    # save the modified file
    raw["vault1"][map_location]["enemies"] = found_it
    out = open(file, "w")
    json.dump(raw, out, indent=1)