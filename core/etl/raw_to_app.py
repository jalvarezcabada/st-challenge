import polars as pl
from datetime import datetime

from etl.utils.read_format import read_txt
from etl.utils.write_format import write_df_on_parquet
from etl.utils.logger_manager import create_logger

logger = create_logger(__name__)

class OrderMananger:

    def __init__(self,
        output_save: str
    ):

        self.output_save = output_save

    def fact_orders_etl(self,
        raw_path:str
    )-> None:

        logger.info(f"Reading raw data from: {raw_path}")
        raw_data = read_txt(file_path=raw_path)

        df = pl.DataFrame(raw_data)
        
        #Fields mapping in nested Json
        map_fields = df.with_columns([
            pl.col('data_raw').str.json_path_match(r"$.id").cast(pl.Float64).alias('id'),
            pl.col('data_raw').str.json_path_match(r"$.order_number").alias('order_number'),
            pl.col('data_raw').str.json_path_match(r"$.user_id").alias('user_id'),
            pl.col('data_raw').str.json_path_match(r"$.total_price_usd").alias('total_price_usd'),
            pl.col('data_raw').str.json_path_match(r"$.total_price").alias('total_price'),
            pl.col('data_raw').str.json_path_match(r"$.created_at").alias('created_at')
        ])

        #Appling data types
        orders = map_fields.with_columns([
            pl.col('id').cast(pl.Int64),
            pl.col('order_number').cast(pl.Int16),
            pl.col('user_id').cast(pl.Int32),
            pl.col('total_price_usd').cast(pl.Float32),
            pl.col('total_price').cast(pl.Float32),
            pl.col('created_at').str.strptime(pl.Datetime,strict=False),
            pl.col('creation_ts').str.strptime(pl.Datetime,strict=False)
        ])

        fact_orders = orders.select([
            "id", 
            "order_number", 
            "user_id", 
            "total_price_usd", 
            "total_price",
            "created_at", 
            "creation_ts"
        ])

        curated_path = f"{self.output_save}/fact_orders.parquet"
        logger.info(f"Wrinting curated data in: {curated_path}")
        write_df_on_parquet(
            df=fact_orders,
            path=curated_path
        )

        logger.info("The writing process completed successfully")

    def agg_orders(self,
        curated_path: str
    )-> None:
        
        now = datetime.now()

        logger.info(f"Reading curated data from: {curated_path}")
        fact_orders = pl.read_parquet(source=curated_path)

        agg_orders = fact_orders.with_columns([
            pl.col('created_at').cast(pl.Date).alias("creation_dt")
        ]) \
        .groupby("creation_dt") \
        .agg(
            pl.col('order_number').count().alias("total_orders_qty"), 
            pl.col('total_price').sum().alias("total_sales_amount")
        ) \
        .with_columns(creation_ts = now)

        write_path = f"{self.output_save}/agg_orders.parquet"
        logger.info(f"Wrinting in: {write_path}")
        write_df_on_parquet(
            df=agg_orders,
            path=write_path
        )

        logger.info("The writing process completed successfully")