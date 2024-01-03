import pymongo
import base64
from bson.objectid import ObjectId  # Import ObjectId

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://achyutammehta:7WvgmzWySS2wCLin@workannivcluster.cbvgni6.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB connection string
db = client["WorkAnnivDataHub"]  # Replace with your database name
collection = db["EmployeeAnniversaryRecords"]  # Replace with your collection name

# Replace 'your_document_id' with the actual document ID
document_id = "658432af607509b69447f7df"  # Example: "5f50c31e1c4ae837423e6df1"

# Find the document with the image
document = collection.find_one({"_id": ObjectId(document_id)})

if document:
    # Extract the image data
    image_data_base64 = document.get("Image_Data", None)

    if image_data_base64:
        # Decode Base64 string into bytes
        image_bytes = base64.b64decode(image_data_base64)

        # Save the image to a file
        with open("output_image.jpg", "wb") as image_file:
            image_file.write(image_bytes)

        print("Image saved successfully.")
    else:
        print("Image data not found in the document.")
else:
    print(f"Document not found for ID '{document_id}'.")

# Close the MongoDB connection
client.close()
