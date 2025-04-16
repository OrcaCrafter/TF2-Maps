import json
import shutil
import os

print("Process Began")

mapsrc = "../mapsrc/"
mapcol = "map_collection/"

extensions = [
    ".bsp",
    ".prt",
    ".vmf",
    ".vmx"
];

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return f"Error: File not found at path: {file_path}"
    except json.JSONDecodeError:
        return "Error: Invalid JSON format in the file."

if (not os.path.exists(mapcol)):
        os.mkdir(mapcol);

data = read_json_file('map_list.json')

for map in data :
    print("Processing map: " + map["name"]);
    
    #Create Folder for Map
    col_path = mapcol + map["name"];
    tar_path = col_path + "/" + map["name"];

    print(tar_path)

    if (not os.path.exists(col_path)):
        os.mkdir(col_path);

    #Get Files for Map
    file_path = mapsrc + map["path"] + map["file"]

    for ext in extensions:
        cur_src = file_path + ext
        cur_tar = tar_path + ext
        
        if (os.path.exists(cur_src)):
            shutil.copy(cur_src, cur_tar);
        else:
            print(f"Path: {cur_src} does not exist")
    #Pack map?
    #Compile map
    #3D Model map

input("Done Processing")
