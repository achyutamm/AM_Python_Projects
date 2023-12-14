from pymongo import MongoClient
from pymongo.server_api import ServerApi
from gridfs import GridFS  # Fix this line
from bson import ObjectId
from datetime import datetime
import os
from gridfs import errors as gridfs_errors



MONGODB_URI = "mongodb+srv://achyutammehta:7WvgmzWySS2wCLin@workannivcluster.cbvgni6.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db_name = "WorkAnnivDataHub"
db = client[db_name]
collection_name = "EmployeeAnniversaryRecords"
download_path = r"C:\Python\WBZ_WorkAnniversaryGreetings\Data\Image Download"

def fetch_records_by_current_date(db, collection_name, date_field, filter_conditions=None):
    cursor = db[collection_name].find()
    current_date = datetime.now().strftime('%m/%d')
    filter_conditions = filter_conditions or {}
    filtered_records = [
        record for record in cursor
        if record[date_field] and record[date_field].startswith(current_date)
    ]
    return filtered_records

def download_images(records, download_path):
    fs = GridFS(db)
    for record in records:
        if 'image_id' in record:
            image_id = record['image_id']
            
            try:
                file = fs.get(ObjectId(image_id))
                
                # Create a timestamped folder
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                folder_path = os.path.join(download_path, timestamp)
                os.makedirs(folder_path, exist_ok=True)

                # Save the image with the employee's name
                image_filename = f"{record['employee_name']}_image.jpg"
                image_path = os.path.join(folder_path, image_filename)

                with open(image_path, "wb") as image_file:
                    image_file.write(file.read())
                    
            except gridfs_errors.NoFile:  # Correct the exception here
                print(f"File not found in GridFS for image_id: {image_id}")

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

date_field = "work_anniversary"
dynamic_filter = {"employee_name": "Gaurav Tripathi"}

filtered_records = fetch_records_by_current_date(db, collection_name, date_field, dynamic_filter)

records_list = []
for document in filtered_records:
    print(document)
    records_list.append(document)

for record in records_list:
    print(f"Employee: {record['employee_name']}, Anniversary Date: {record['work_anniversary']}")

download_images(filtered_records, download_path)

all_records_cursor = db[collection_name].find()

print("\nAll Records:")
for document in all_records_cursor:
    print(document)