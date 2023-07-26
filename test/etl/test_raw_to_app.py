import pytest
import polars as pl

@pytest.fixture
def curated_data():
    curated_path = "./db/app/fact_orders.parquet"
    return pl.read_parquet(curated_path)

def test_data_types(curated_data):

    # Check if the columns exist in the curated data
    assert "id" in curated_data.columns
    assert "order_number" in curated_data.columns
    assert "user_id" in curated_data.columns
    assert "total_price_usd" in curated_data.columns
    assert "total_price" in curated_data.columns
    assert "created_at" in curated_data.columns
    assert "creation_ts" in curated_data.columns

    # Check the data types of the columns
    assert curated_data["id"].dtype() == pl.Int64
    assert curated_data["order_number"].dtype() == pl.Int16
    assert curated_data["user_id"].dtype() == pl.Int32
    assert curated_data["total_price_usd"].dtype() == pl.Float32
    assert curated_data["total_price"].dtype() == pl.Float32
    assert curated_data["created_at"].dtype == pl.Datetime
    assert curated_data["creation_ts"].dtype == pl.Datetime