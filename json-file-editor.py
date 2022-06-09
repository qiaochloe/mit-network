import json

def name_json_lists(json_file, list_name):
    
    output = {}
    
    with open(json_file, 'r') as file: 
        file_data = json.load(file)
        output[f"{list_name}"] = file_data
        
    with open(json_file, 'w+') as file:
        json.dump(output, file, indent=2)
    

def add_json(file_one_name, file_two_name, output_file_name=None):
    """
    Args:
        file_one_name (str): path to json file with data
        file_two_name (str): path to json file with data
        output_file_name (str): path to json file to be overwritten; equal to file_one_name by default
        
    Returns: 
        dict: combined json data of the two files
        
    """
    
    output_dict = {}
    with open(file_one_name, 'r') as file_one, open(file_two_name, 'r') as file_two: 
        #file_one_data = []
        
        #for json_obj in file_one:
        #    data = json.loads(json_obj) # load into dict
        #    file_one_data.append(data)
        
        #file_two_data = []
        
        #for json_obj in file_two:
        #    data = json.loads(json_obj) # load into dict
        #    file_two_data.append(data)
        
        file_one_data = json.load(file_one)
        file_two_data = json.load(file_two)
                
        output = file_two_data + file_one_data 
                
    if output_file_name is None: 
        output_file_name = file_one_name
        
    with open(output_file_name, 'r+') as output_file:
        json.dump(output, output_file, indent=2) # convert back to json

add_json("./data/nodes.json", "./data/gir-nodes.json")