import os
import json
from core.etl.utils.read_format import read_csv, read_txt

def create_test_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

csv_test_data = """id,name,age
1,Joaquin,30
2,Pedro,25
3,Luis,28"""

txt_test_data = [
    {"id": 1, "name": "Joaquin", "age": 30},
    {"id": 2, "name": "Pedro", "age": 25},
    {"id": 3, "name": "Luis", "age": 28}
]

def test_read_csv():
    test_file_path = "test_data.csv"
    create_test_file(test_file_path, csv_test_data)

    try:
        data = read_csv(test_file_path)

        assert len(data) == 3
        assert data[0]["id"] == "1"
        assert data[1]["name"] == "Pedro"
        assert data[2]["age"] == "28"
    finally:
        os.remove(test_file_path)

def test_read_txt():
    test_file_path = "test_data.txt"
    with open(test_file_path, 'w') as file:
        for item in txt_test_data:
            json_line = json.dumps(item)
            file.write(json_line + '\n')

    try:
        data = read_txt(test_file_path)

        assert len(data) == 3
        assert data[0]["id"] == 1
        assert data[1]["name"] == "Pedro"
        assert data[2]["age"] == 28
    finally:
        os.remove(test_file_path)