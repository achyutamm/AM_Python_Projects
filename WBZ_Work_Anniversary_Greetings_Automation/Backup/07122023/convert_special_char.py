import pymongo
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb+srv://achyutammehta:7WvgmzWySS2wCLin@workannivcluster.cbvgni6.mongodb.net/?retryWrites=true&w=majority")
db = client["WorkAnnivDataHub"]

# Specify the collection name
collection_name = "EmployeeAnniversaryRecords"

# Retrieve all documents from the collection
cursor = db[collection_name].find()

# Create a new GridFS instance
fs = GridFS(db, collection="images")

# Iterate through the documents and download the image files
for document in cursor:
    image_id = document.get("image_id")

    # Retrieve the image file from GridFS
    image_file = fs.get(image_id)

    # Save the image file locally
    local_image_path = f"C:/Python/WBZ_WorkAnniversaryGreetings/Data/Downloaded_Images/{document['employee_name']}.jpg"
    with open(local_image_path, "wb") as local_file:
        local_file.write(image_file.read())

    # Add the local image path to the document
    document["local_image_path"] = local_image_path

    print(document)
