from etl.landing_to_raw import LandingToRaw

CSV_FILE = "./db/landing/ecommerce/orders/839012383812.csv"
METADATA_FIELDS = ["_job_user_id", "_job_batch_runtime", "_job_batch_id"]
METADATA_NAMES = ["daton_user_id", "daton_batch_runtime", "daton_batch_id"]

if __name__=="__main__":

    LandingToRaw.csv_to_txt(csv_file=CSV_FILE, metadata_fields=METADATA_FIELDS, metadata_names=METADATA_NAMES)