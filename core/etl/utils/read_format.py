import csv
import json

def read_csv(file_name):
    data = []
    with open(file_name, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

def read_txt(file_name):
    data = []
    with open(file_name, 'r') as txt_file:
        for line in txt_file:
            json_data = json.loads(line.strip())
            data.append(json_data)
    return data