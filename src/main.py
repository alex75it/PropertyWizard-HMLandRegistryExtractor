import sys

from extractor import config
from extractor.logger import Logger
from extractor.process import Process
from extractor.fileReader import FileReader
from extractor.repositories.saleRawDataMongoRepository import SaleRawDataMongoRepository
from extractor.repositories.saleMongoRepository import SaleMongoRepository
from extractor.saleDataProcessor import SaleDataProcessor


logger = Logger.create(__name__)

def run(csv_file: str):
    logger.info(f"Run. CSV file: {csv_file}")

    file_reader = FileReader()
    connection_string = config.mongo_connection_string
    database_name = config.mongo_database_name
    sale_raw_data_repository = SaleRawDataMongoRepository(connection_string, database_name)
    sale_repository = SaleMongoRepository(connection_string, database_name)
    sale_data_processor = SaleDataProcessor(sale_raw_data_repository, sale_repository)

    process = Process(file_reader, sale_raw_data_repository, sale_data_processor)

    try:
        process.run(csv_file)
    except Exception as error:
        logger.fatal(f'Fail to run process on CSV file "{csv_file}". {error}')


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("CSV file argument missing")
        sys.exit(1)

    file_ = sys.argv[1]

    import os
    if not os.path.exists(file_):
        file_ = os.path.join(os.getcwd(), file_)
        if not os.path.exists(file_):
            print(f'File not found: "{file_}".')
            sys.exit(1)

    run(file_)

