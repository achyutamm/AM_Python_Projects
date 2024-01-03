from pymongo import MongoClient
import config_reader


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


# Connect to MongoDB
client = MongoClient(mongoclient) 
db = client[db_name]
collection = db[collection_name]

# Remove all documents from the collection
result = collection.delete_many({})

# Check the number of documents deleted
print(f"{result.deleted_count} documents removed from the collection.")
