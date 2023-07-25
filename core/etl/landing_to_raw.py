from datetime import datetime

from etl.utils.read_format import read_csv
from etl.utils.write_format import write_txt

class LandingToRaw:

    @staticmethod
    def csv_to_txt(csv_file, metadata_columns):

        date = datetime.now().date()

        #Read CSV from landing Zone
        csv_data = read_csv(csv_file)

        #Write TxT on Raw Zone
        write_txt(csv_data, f"./db/raw/orders_{date}.txt", metadata_columns)