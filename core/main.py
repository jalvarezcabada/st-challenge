from datetime import datetime

from etl.landing_to_raw import LandingToRaw
from etl.raw_to_app import Order
from etl.utils.logger_manager import create_logger

logger = create_logger(__name__)

SOURCE_NAME = "orders"
LANDING_CSV_FILE = "./db/landing/ecommerce/orders/839012383812.csv"
RAW_METADATA_COLUMNS = [
    "_job_user_id", 
    "_job_batch_runtime", 
    "_job_batch_id"
]

if __name__=="__main__":

    date = datetime.now().date()

    logger.info("Moving data from Landing Zone to Raw Zone")
    LandingToRaw.csv_to_txt(
        source_name=SOURCE_NAME,
        csv_file=LANDING_CSV_FILE, 
        metadata_columns = RAW_METADATA_COLUMNS
    )

    logger.info("Creating fact_orders table consuming raw data")
    Order.fact_orders_etl(
        raw_path=f"./db/raw/orders_{date}.txt"
    )

    logger.info("Creating orders aggregation table")
    Order.agg_orders(
        curated_path=f"./db/app/fact_orders.parquet"
    )
