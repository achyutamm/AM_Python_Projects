from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime


MONGODB_URI = "mongodb+srv://achyutammehta:7WvgmzWySS2wCLin@workannivcluster.cbvgni6.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db_name = "WorkAnnivDataHub"  # Replace with your actual database name
db = client[db_name]
collection_name = "EmployeeAnniversaryRecords"

def fetch_records_by_current_date(db, collection_name, date_field, filter_conditions=None):
    # Retrieve all records from the collection
    cursor = db[collection_name].find()

    # Get the current system date
    current_date = datetime.now().strftime('%m/%d')

    # Define the filter conditions
    filter_conditions = filter_conditions or {}

    # Filter records based on the "work_anniversary" field
    filtered_records = [
        record for record in cursor
        if record[date_field] and record[date_field].startswith(current_date)
    ]

    # Return the filtered documents
    return filtered_records

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Example usage of the function with dynamic filter conditions
date_field = "work_anniversary"

# Define dynamic filter conditions based on user input or other factors
dynamic_filter = {"employee_name": "Gaurav Tripathi"}

filtered_records = fetch_records_by_current_date(db, collection_name, date_field, dynamic_filter)


records_list = []


for document in filtered_records:
    print(document)
    records_list.append(document)

for record in records_list:
    print(f"Employee: {record['employee_name']}, Anniversary Date: {record['work_anniversary']}")


all_records_cursor = db[collection_name].find()

print("\nAll Records:")
for document in all_records_cursor:
    print(document)
