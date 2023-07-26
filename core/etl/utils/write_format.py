import json
from datetime import datetime
from typing import List, Dict, Any
from polars import DataFrame

def write_txt(
    data:List[Dict[str, Any]],
    file_path:str, 
    metadata_columns:List[str]
)-> None:

    try:
        with open(file_path, 'w') as txt_file:
            for row in data:
                json_data = {field: row[field] for field in row if field not in metadata_columns}
                metadata_values = [row[column] for column in metadata_columns]
                metadata = {metadata_columns[i]: metadata_values[i] for i in range(len(metadata_values))}

                metadata["creation_ts"] = datetime.now().isoformat()
                output_data = {
                    "data_raw": json.dumps(json_data),
                    **metadata
                }
                line = json.dumps(output_data) + "\n"
                txt_file.write(line)
    except Exception as e:
        raise Exception(e)

def write_df_on_parquet(
    df:DataFrame, 
    path:str,  
    compression:str = "snappy"
)-> None:

    try:
        df.write_parquet(path, compression=compression)

    except Exception as e:
        raise Exception(e)

    