import os
import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pymongo import MongoClient
import yaml
import logging
from datetime import datetime
from bson import Binary
import config_reader

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
        self.data_add_loader_log = config_data[environment]['file_path']['data_add_loader_log']
        self.data_loader = config_data[environment]['file_path']['data_add_loader']
        self.backup_folder = config_data[environment]['file_path']['loader_backup']

def create_timestamped_log_folder(data_add_loader_log):
    today = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join(data_add_loader_log, today)

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
    logging.info(f"WBZ Employee Adding Data on MongoDB Process has started on {machine_name}.")

class ExcelHandler(FileSystemEventHandler):
    def __init__(self, app_config):
        self.app_config = app_config
        self.mongo_client = MongoClient(self.app_config.mongoclient)
        self.db = self.mongo_client[self.app_config.db_name]
        self.collection = self.db[self.app_config.collection_name]
        self.backup_folder = self.app_config.backup_folder
        self.processed_files = set()

    def process_existing_files(self, folder_to_watch):
        # List all existing files in the folder
        existing_files = [os.path.join(folder_to_watch, file) for file in os.listdir(folder_to_watch) if file.endswith(".xlsx")]

        # Process existing files
        for file_path in existing_files:
            if file_path not in self.processed_files:
                logging.info(f"Existing Excel file detected: {file_path}")
                self.process_excel_file(file_path)

    def process_excel_file(self, excel_path):
        try:
            # Read Excel file into a pandas DataFrame
            df = pd.read_excel(excel_path)

            # Get employee name from the first row
            employee_name = df.columns[0]
            for index, row in df.iterrows():
                image_path = row.get("Image_Path", "")
                if image_path and os.path.exists(image_path):
                    with open(image_path, "rb") as image_file:
                        image_binary = Binary(image_file.read())

                    record = row.to_dict()
                    record["Image_Data"] = image_binary


                    self.collection.insert_one(record)
                    logging.info(f"Inserted record with image into MongoDB for {employee_name}.")

                    # Log entry for the added image
                    logging.info(f"Added image for {employee_name}. Image file: {os.path.basename(image_path)}")

            logging.info(f"Processed {len(df)} records with images in total for {employee_name}.")

            timestamped_folder = create_timestamped_log_folder(self.backup_folder)
            if timestamped_folder:
                backup_path = os.path.join(timestamped_folder, f"backup_{datetime.now().strftime('%H%M%S')}_{os.path.basename(excel_path)}")
                os.rename(excel_path, backup_path)
                logging.info(f"Moved Excel file to the backup folder: {backup_path}")

                self.processed_files.add(backup_path)

        except Exception as e:
            logging.error(f"Error processing Excel file: {excel_path}. Error: {e}")

    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith(".xlsx"):
            logging.info(f"New Excel file detected: {event.src_path}")
            self.process_excel_file(event.src_path)

if __name__ == "__main__":
    config_file_path = "C:/Python/WBZ_Work_Anniversary_Greetings_Automation/Config/appconfig.yaml"
    config_data = config_reader.load_config(config_file_path)
    environment = DEVELOPMENT  # Change this based on your needs
    app_config = AppConfig(environment, config_data)

    log_folder_path = create_timestamped_log_folder(app_config.data_add_loader_log)
    if log_folder_path:
        setup_logging(log_folder_path, machine_name=os.environ['COMPUTERNAME'])

    folder_to_watch = app_config.data_loader

    event_handler = ExcelHandler(app_config)
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)

    logging.info("Observer is starting to watch for new events.")
    observer.start()

    event_handler.process_existing_files(folder_to_watch)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
