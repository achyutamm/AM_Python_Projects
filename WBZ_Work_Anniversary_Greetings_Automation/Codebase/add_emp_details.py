import pymongo
import base64


client = pymongo.MongoClient("mongodb+srv://achyutammehta:7WvgmzWySS2wCLin@workannivcluster.cbvgni6.mongodb.net/?retryWrites=true&w=majority")  
db = client["WorkAnnivDataHub"] 
collection = db["EmployeeAnniversaryRecords"]  

# Path to your image
image_path = "C:\Python\WBZ_Work_Anniversary_Greetings_Automation\Data\Work Anniversary Pictures\Ayisha Hajisa.jpg"

# Read the image and convert to Base64
with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

# Create or update the document
document = {
    "Employee_Name": "Employee Name", 
    "Work_Anniversary": "18-12-2023",
    "Image_Data": encoded_string
}


collection.insert_one(document)  


client.close()
