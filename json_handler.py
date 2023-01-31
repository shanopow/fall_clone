# structure of maps.json is very important
# first, we must group by area, each map falling under an area
# second, the ordering of maps within the area is VERY IMPORTANT
# they should be ordered accoring to the minmap reader so it can gernerate the minmap
# typically, this means organise the first one to be the room in the top left corner and work from there

# This file is responsible for reading in from our json file and building our objects or maps
# basically takes functions from map_builder and works with them here

# File imports 
from map_builder import norm_builder, door_maker, vault_sprinkler
from world_actions import populater
# Moduele imports
import json

def file_reader(file_name):
    f = open(file_name)
    raw_data = json.load(f)
    f.close()
    return raw_data

# reads in every map in the json, keeps them seperated
# only chooses one it wants
def map_maker(file_name, chosen, curr_area, object_list):
    to_build = []
    data = file_reader(file_name)
    area = data[curr_area]
    for item in area:
        if item == chosen:
            room = area[chosen]
            # make dimensions here
            start_room = norm_builder(room["dimensions"])        
            # here we make list of items to sprinkle onto the map
            details = []
            details = populater(details, room["people"], object_list)
            details = populater(details, room["enemies"], object_list)
            # add doors on
            details = door_maker(details, room["doors"], start_room, chosen)
            vault_sprinkler(details, start_room)
            return start_room
    print("Could not find this map, exiting now")
    quit()

# Function for joining together nodes as a minimap
def minimap_builder(curr_area):
    f = open(file_name)
    for room in area:
        pass

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