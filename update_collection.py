import json
import shutil
import os
import numpy as np
import trimesh
import transformations as trans
import concurrent.futures

# Header

map_src = "../mapsrc/"
map_col = "map_collection/"

tf_root = "../../../tf/"
hl_root = "../../../hl2/"

asset_dirs = [
    tf_root + "tf2_misc_dir.vpk",
    tf_root + "tf2_textures_dir.vpk",
    hl_root + "hl2_misc_dir.vpk",
    hl_root + "hl2_textures_dir.vpk"
]

extensions = [
    ".bsp",
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

# Rotates the model to fix the vertical axis
# Rotate around x by -90
axis_fix = trans.rotation_matrix(-np.pi / 2, (1, 0, 0))

# Scales the model to 1u = 1m, instead of 1u = 1hu
# 16hu = 1ft; 1ft = 0.3048m; 1hu = 0.01905m
scale_fix = trans.scale_matrix(0.01905, (0, 0, 0))

def convert_model (src, dest):
        """Converts an OBJ file to GLB format.
    
        Args:
            obj_filepath: Path to the input OBJ file.
            glb_filepath: Path to save the output GLB file.
        """
                
        e = trimesh.load(src);
        
        e.apply_transform(axis_fix)
        e.apply_transform(scale_fix)
        
        e.export(dest);

def handle_map (map_data):
    print("Processing map: " + map_data["name"]);
    
    #Create Folder for map_data
    col_path = map_col + map_data["name"];
    tar_path = col_path + "/" + map_data.get("file", map_data["name"]);

    if (not os.path.exists(col_path)):
        os.mkdir(col_path);

    #Get Files for map_data
    #TODO get custom assets
    file_path = map_src + map_data.get("path", "") + map_data.get("file", map_data["name"])

    for ext in extensions:
        cur_src = file_path + ext
        cur_tar = tar_path + ext
        
        if (os.path.exists(cur_src)):
            shutil.copy(cur_src, cur_tar);
        else:
            print(f"Path: {cur_src} does not exist")
    
    #Pack map_data?
    #Compile map_data
    #Generate model as obj
    if (map_data.get("gen_obj", defaults["gen_obj"])):
        if (not os.path.exists(tar_path + ".obj") or map_data.get("force_gen_obj", defaults["force_gen_obj"])): 
            print("Generating Model");
            
            asset_dir_str = "";

            for asset_dir in asset_dirs:
                asset_dir_str += asset_dir + ";"

            if "custom_assets" in map_data:
                for asset_dir in map_data["custom_assets"]:
                    asset_dir_str += asset_dir + ";"
            
            command = f"java -jar ./vmf2obj.jar {file_path}.vmf -o ./{tar_path} -r \"{asset_dir_str}\" -t"
            
            os.system(command);

    #Convert obj to glb
    if (map_data.get("convert", True)):
        print("Converting obj to " + map_data.get("convert_type", defaults["convert_type"]))
        convert_model(tar_path + ".obj", tar_path + "." + map_data.get("convert_type", defaults["convert_type"]))

        #Cleanup obj files
        if (map_data.get("clear_obj", defaults["clear_obj"])):
            print("Clearing obj")
            shutil.rmtree(col_path + "/materials");
            os.remove(tar_path + ".obj");
            os.remove(rat_path + ".mtl");

# Code Starts
print("Process Began")

# Make map collection directory
if (not os.path.exists(map_col)):
        os.mkdir(map_col);

#Read info file
data = read_json_file('map_list.json')

if (type(data) is str):
    input("Error: " + data)

defaults = data["defaults"]

thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=len(data["maps"]))



#Itterate over all maps in the info file
for map_data in data["maps"] :
    thread_pool.submit(handle_map, map_data)

thread_pool.shutdown(wait=True)

"""
TODO setup dev shots

#Linearaly itterate over all map to take dev shots
if (data.get("dev-shot", false)):
    for map_data in data["maps"] :
        print("Taking dev Shots for map: " + map-map_data["name"])

        
        #Setup game open command

        #Launch Team Fortress 2
        command = "steam://rungameid/440"
"""



    

input("Done Processing")
