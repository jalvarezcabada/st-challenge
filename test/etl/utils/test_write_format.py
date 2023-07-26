import pytest
from polars import DataFrame
import polars as pl
import tempfile
import os

from core.etl.utils.write_format import write_txt, write_df_on_parquet

@pytest.mark.parametrize("data, metadata_columns", [
    ([{"name": "Pedro", "age": 30}, {"name": "Joaquin", "age": 25}], ["age"]),
])
def test_write_txt(data, metadata_columns):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "test_data.txt")

            write_txt(data, temp_file_path, metadata_columns)

            with open(temp_file_path, 'r') as txt_file:
                lines = txt_file.readlines()
                assert len(lines) == len(data)

    except Exception as e:
        pytest.fail(f"Exception: {e}")


@pytest.mark.parametrize("data, file_path, compression", [
    ([{"name": "Pedro", "age": 30}, {"name": "Juan", "age": 25}], "test_data_1.parquet", "snappy"),
    ([{"name": "Joaquin", "age": 40}, {"name": "Carlos", "age": 35}], "test_data_2.parquet", "gzip"),
])
def test_write_df_on_parquet(data, file_path, compression):
    try:
        df = DataFrame(data)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, file_path)

            write_df_on_parquet(df, temp_file_path, compression)

            df_read = pl.read_parquet(temp_file_path)
            assert df_read.frame_equal(df)

    except Exception as e:
        pytest.fail(f"Exception: {e}")