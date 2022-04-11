# UNFINISHED

import csv
import json

def make_json(csvFilePath, jsonFilePath):
    data = {}
    
    with open(csvFilePath, encoding="utf-8") as csvf:
        csvf = csv.reader(csvf, delimiter='\t') # Remove this line for csv files
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            key = rows['course_code']
            data[key]
            
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, intdent=4))
        
csvFilePath = r'eecs/eecs.csv'
jsonFilePath = r'eecs/eecs.json'

make_json(csvFilePath, jsonFilePath)