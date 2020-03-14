import logging
import os
import csv

# Set loglevel
log_level = os.environ.get('LOG_LEVEL', 'DEBUG')
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
logger = logging.getLogger(__name__)

keys=['uuid','name','date']

def put_data_to_dict(keys):
    # Read the Inventory CSV file
    with open("codes.csv") as csvfile:
        # Change delimiter accordingly
        reader = csv.DictReader(csvfile, delimiter=';')
        # Read each row in the file
        rowCount = 0
        for row in reader:
            rowCount += 1
            # print(row)
            try:
                item={}
                for m, n in zip(keys,row):
                    item[m] = row[n]
                print(item)
            except Exception as e:
                logger.info(e)
                logger.info("Putting data to dictornary failed")
                raise e

if __name__ == "__main__":
    logger.info("Starting dynamic dict creatoin")
    try: 
        put_data_to_dict(keys=keys)
    except Exception as e:
        logger.info(e)
        logger.info("Dict creation failed")
        raise e