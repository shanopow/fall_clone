# This file is responsible for reading in from our json file and building our objects or maps
import json

def file_reader(file_name):
    f = open(file_name)
    raw_data = json.load(f)
    f.close()
    return raw_data

# reads in every map in the json, keeps them seperated
# only chooses one it wants
# WANT THIS TO BE A MAP-STITCHER, TAKES ARRAY OF CHOICES THEN STITCHES THEM TOGETHER
# WOULD BE COOL, MAYBE STINKY TO IMPLEMENT
def map_maker(file_name, chosen):
    to_build = []
    data = file_reader(file_name)
    for item in data:
        if item == chosen:
            return data[chosen]
    print("Could not find this map, exiting now")
    quit()


# for converting name of class in str to actual class, used in normal object builder, DO NOT USE ALONE
def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m

# makes big list of all objects of same class
def object_builder(file_name, class_type, keyword):
    data = file_reader(file_name)
    D = get_class(class_type)
    big = []
    for item in data[keyword]:
        adder = D(item)
        big.append(adder)
    return big

# For creating the megalist of objects to index to quickly access
def final_object_builder(mashed_list):
    final_dict = {}
    for item in mashed_list:
        final_dict[item.form_id] = item
    return final_dict