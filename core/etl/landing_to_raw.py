from datetime import datetime
from typing import List

from etl.utils.read_format import read_csv
from etl.utils.write_format import write_txt
from etl.utils.logger_manager import create_logger

logger = create_logger(__name__)

class LandingToRaw:

    @staticmethod
    def csv_to_txt(
        source_name:str,
        csv_file:str, 
        metadata_columns:List[str]
    )-> None:

        date = datetime.now().date()
        write_path = f"./db/raw/{source_name}_{date}.txt"

        logger.info(f"Reading data from: {csv_file} \n Writing in: {write_path}")

        #Read CSV from landing Zone
        csv_data = read_csv(file_path=csv_file)

        #Write TxT on Raw Zone
        write_txt(
            data=csv_data, 
            file_path=write_path, 
            metadata_columns=metadata_columns
        )

        logger.info("The writing process completed successfully")