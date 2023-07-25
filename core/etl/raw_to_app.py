import polars as pl

from etl.utils.read_format import read_txt
from etl.utils.write_format import write_df_on_parquet

class Order:

    @staticmethod
    def fact_orders_etl(raw_path):

        raw_data = read_txt(raw_path)

        df = pl.DataFrame(raw_data)

        #Mapping fields in nested Json
        map_fields = df.with_columns([
            pl.col('data_raw').str.json_path_match(r"$.id").cast(pl.Float64).alias('id'),
            pl.col('data_raw').str.json_path_match(r"$.order_number").alias('order_number'),
            pl.col('data_raw').str.json_path_match(r"$.user_id").alias('user_id'),
            pl.col('data_raw').str.json_path_match(r"$.total_price_usd").alias('total_price_usd'),
            pl.col('data_raw').str.json_path_match(r"$.total_price").alias('total_price')
        ]) \

        #Appling data type
        orders = map_fields.with_columns([
            pl.col('id').cast(pl.Int64),
            pl.col('order_number').cast(pl.Int16),
            pl.col('user_id').cast(pl.Int32),
            pl.col('total_price_usd').cast(pl.Float32),
            pl.col('total_price').cast(pl.Float32),
            pl.col('creation_ts').str.strptime(pl.Datetime,strict=False)
        ]) \

        fact_orders = orders.select(["id", "order_number", "user_id", "total_price_usd", "total_price", "creation_ts"])

        #Writing in Parquet Format
        write_df_on_parquet(df=fact_orders,path="./db/app/fact_orders.parquet")
