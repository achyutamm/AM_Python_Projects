import os
import logging
from datetime import datetime, timezone
import socket
import time
from pymongo import MongoClient
from gridfs import GridFS
import config_reader
from bson import ObjectId
from gridfs.errors import NoFile
import base64

# Constants
PRODUCTION = "production"
DEVELOPMENT = "development"

# Configuration
class AppConfig:
    def __init__(self, environment, config_data):
        self.environment = environment
        self.mongoclient = config_data[environment]['database']['mongoclient']
        self.db_name = config_data[environment]['database']['db_name']
        self.collection_name = config_data[environment]['database']['collection_name']
        self.downloaded_images = config_data[environment]['file_path']['downloaded_images']
        self.log_file_path = config_data[environment]['file_path']['log_path']
        self.log_file_path = config_data[environment]['file_path']['log_path']


def create_timestamped_log_folder(log_file_path):
    today = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join(log_file_path, today)

    try:
        os.makedirs(folder_path)
        return folder_path
    except FileExistsError:
        return folder_path
    except Exception as e:
        logging.error(f"Error creating log folder: {e}")
        return None


def setup_logging(log_folder_path, machine_name):
    logging.basicConfig(
        filename=os.path.join(log_folder_path, "process_log.txt"),
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    logging.info(f"WBZ Work_Anniversary Greetings Automation Process has started on {machine_name}.")


def connect_to_mongodb(mongoclient, db_name):
    try:
        client = MongoClient(mongoclient)
        db = client[db_name]
        logging.info("Connected to MongoDB successfully!")
        return client, db
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {e}")
        return None, None


def process_work_anniversaries(db, collection_name, downloaded_images, log_folder_path):
    today_date = datetime.utcnow().strftime("%Y-%m-%d")
    logging.info(f"Today's Date: {today_date}")
    query = {"Work_Anniversary": today_date}
    logging.info(f"Generated Query: {query}")

    collection = db[collection_name]
    documents = collection.find(query)
    total_documents = collection.count_documents(query)
    logging.info(f"Found {total_documents} documents to process for today's work anniversaries.")

    start_download_time = time.time()

    for document in documents:
        document_id = document["_id"]
        logging.info(f"Processing document for ID: {document_id}")

        image_data_base64 = document.get("Image_Data", None)
        if image_data_base64:
            try:
                # Decode Base64 string into bytes
                image_bytes = base64.b64decode(image_data_base64)

                employee_name = document["Employee_Name"]
                local_image_path = os.path.join(downloaded_images, f"{employee_name}.jpg")

                with open(local_image_path, "wb") as image_file:
                    image_file.write(image_bytes)

                current_download_time = time.time()
                logging.info(f"Image downloaded for {employee_name} in {(current_download_time - start_download_time):.2f} seconds.")
            except Exception as e:
                logging.error(f"Error downloading image for {employee_name}: {e}")
        else:
            logging.warning(f"Image data is missing for document ID: {document_id}")


def main():
    start_time = time.time()
    machine_name = socket.gethostname()
    config_data = config_reader.load_config("C:/Python/WBZ_Work_Anniversary_Greetings_Automation/Config/appconfig.yaml")
    environment = DEVELOPMENT  # Change to PRODUCTION if needed

    app_config = AppConfig(environment, config_data)
    log_folder_path = create_timestamped_log_folder(app_config.log_file_path)
    setup_logging(log_folder_path, machine_name)

    client, db = connect_to_mongodb(app_config.mongoclient, app_config.db_name)

    if client is not None and db is not None:
        try:
            process_work_anniversaries(db, app_config.collection_name, app_config.downloaded_images, log_folder_path)
        finally:
            client.close()

        end_time = time.time()
        logging.info(f"Total execution time: {(end_time - start_time):.2f} seconds")
        logging.info(f"WBZ Work_Anniversary Greetings Automation Process has been completed on {machine_name}.")


if __name__ == "__main__":
    main()
