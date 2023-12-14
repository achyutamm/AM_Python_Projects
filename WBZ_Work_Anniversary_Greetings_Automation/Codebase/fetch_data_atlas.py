import pymongo
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
import config_reader
import os, platform, logging
from datetime import datetime
import socket
import time
import logging


start_time = time.time()
machine_name = socket.gethostname()
config_data = config_reader.load_config("C:/Python/WBZ_Work_Anniversary_Greetings_Automation/Config/appconfig.yaml")
environment = "Development"

if environment == "Production":
    mongoclient = config_data['production']['database']['mongoclient']
    db_name = config_data['production']['database']['db_name']
    collection_name = config_data['production']['database']['collection_name']
    downloaded_images = config_data['production']['file_path']['downloaded_images']
    log_file_path = config_data['production']['file_path']['log_path']
elif environment == "Development":
    mongoclient = config_data['development']['database']['mongoclient']
    db_name = config_data['development']['database']['db_name']
    collection_name = config_data['development']['database']['collection_name']
    downloaded_images = config_data['development']['file_path']['downloaded_images']
    log_file_path = config_data['development']['file_path']['log_path']




def create_timestamped_log_folder(log_file_path):
    """
    Creates a date-timestamped folder for log files.

    Args:
        log_file_path: The base path for the log files.

    Returns:
        The absolute path to the newly created folder.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join(log_file_path, today)

    try:
        os.makedirs(folder_path)
        # logging.info(f"Log folder created: {folder_path}")
        return folder_path
    except FileExistsError:
        # logging.info(f"Log folder already exists: {folder_path}")
        return folder_path
    except Exception as e:
        # logging.error(f"Error creating log folder: {e}")
        return None


# Create the date-timestamped folder
log_folder_path = create_timestamped_log_folder(log_file_path)


logging.basicConfig(
    filename=os.path.join(log_folder_path, "process_log.txt"),
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


# Update the logging configuration
logging.info(f"WBZ Work_Anniversary Greetings Automation Process has started on {machine_name}.")

# Connect to MongoDB
logging.info("Connecting to MongoDB...")
client = MongoClient(mongoclient)
db = client[db_name]
logging.info("Connected to MongoDB successfully!")

# Specify the collection name
collection_name = collection_name

# Retrieve documents where work_anniversary is equal to today's date
today_date = datetime.now().strftime("%m/%d")
query = {"work_anniversary": today_date}

# Get the total number of documents
total_documents = db[collection_name].count_documents(query)
logging.info(f"Found {total_documents} documents to process for today's work anniversaries.")

# Start timer for image download
start_download_time = time.time()

# Create a new GridFS instance
logging.info("Creating GridFS instance...")
fs = GridFS(db, collection="images")
logging.info("GridFS instance created successfully!")

# Iterate through the documents and download the image files
count = 0
for document in db[collection_name].find(query):
    # Add these lines before retrieving the image
    employee_name = document["employee_name"]
    work_anniversary_date = document["work_anniversary"]

    logging.info(f"Processing document for employee: {employee_name} ({work_anniversary_date})")

    image_id = document.get("image_id")

    # Download the image from GridFS
    logging.info(f"Retrieving image with ID {image_id}...")
    image_file = fs.get(image_id)

    # Generate the local image path
    local_image_path = os.path.join(downloaded_images, f"{employee_name}.jpg")

    # Save the image to the local file system
    logging.info(f"Saving image to {local_image_path}...")
    with open(local_image_path, "wb") as f:
        f.write(image_file.read())

    # Add the local image path to the document
    document["local_image_path"] = local_image_path

    # Update download time
    current_download_time = time.time()
    logging.info(f"Image download time for {employee_name}: {(current_download_time - start_download_time):.2f} seconds.")

    print(document)

end_time = time.time()
logging.info(f"Total execution time: {(end_time - start_time):.2f} seconds")
logging.info(f"WBZ Work_Anniversary Greetings Automation Process has been completed on {machine_name}.")

client.close()