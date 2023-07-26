import csv
import json
from typing import List, Dict, Any

def read_csv(
    file_path:str
)-> List[Dict[str, Any]]:

    data = []
    try:
        with open(file_path, newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)
        return data
    except Exception as e:
        raise Exception(e)

def read_txt(
    file_path:str
)-> List[Dict[str, Any]]:

    data = []

    try:
        with open(file_path, 'r') as txt_file:
            for line in txt_file:
                json_data = json.loads(line.strip())
                data.append(json_data)
        return data
    except Exception as e:
        raise Exception(e)