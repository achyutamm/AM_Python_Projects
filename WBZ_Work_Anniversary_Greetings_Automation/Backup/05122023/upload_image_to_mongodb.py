import pymongo
from pymongo import MongoClient
from gridfs import GridFS

# Connect to MongoDB
client = MongoClient("mongodb+srv://achyutammehta:7WvgmzWySS2wCLin@workannivcluster.cbvgni6.mongodb.net/?retryWrites=true&w=majority")
db = client["WorkAnnivDataHub"]

# Define a list of employee data
employee_data = [
    {
        "employee_name": "Shivani Thakral",
        "work_anniversary": "11/23",
        "image_path": "C:/Python/WBZ_WorkAnniversaryGreetings/Data/Work Anniversary Pictures/Shivani Thakral.jpg",
    },
    # Add more employee data as needed
]

# Create a new GridFS instance
fs = GridFS(db, collection="images")

# Iterate through employee data and upload images to MongoDB
for employee in employee_data:
    image_path = employee["image_path"]

    with open(image_path, "rb") as image_file:
        image_id = fs.put(image_file, filename=f"{employee['employee_name']}.jpg")
        
        # Add employee details to the MongoDB collection
        employee_details = {
            "employee_name": employee["employee_name"],
            "work_anniversary": employee["work_anniversary"],
            "image_id": image_id,
        }
        db.EmployeeAnniversaryRecords.insert_one(employee_details)

        print(f"Uploaded image for {employee['employee_name']} with ID: {image_id}")
