import json
from datetime import datetime

def write_txt(data, file_name, metadata_columns, metadata_names):
    with open(file_name, 'w') as txt_file:
        for row in data:
            json_data = {field: row[field] for field in row if field not in metadata_columns}
            metadata_values = [row[column] for column in metadata_columns]
            metadata = {metadata_names[i]: metadata_values[i] for i in range(len(metadata_values))}

            metadata["creation_ts"] = datetime.now().isoformat()

            output_data = {
                "data_raw": json.dumps(json_data),
                **metadata
            }
            line = json.dumps(output_data) + "\n"
            txt_file.write(line)