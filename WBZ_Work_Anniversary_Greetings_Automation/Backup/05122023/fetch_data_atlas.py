
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
from pymongo import MongoClient

# uri = "mongodb+srv://amehta:%40Sharanam2050_@cluster0.m1phpod.mongodb.net/?retryWrites=true&w=majority"
# MONGODB_URI = "mongodb+srv://samriddha_biswas:samriddha1418@sammbase.kmu7oej.mongodb.net/?retryWrites=true&w=majority"
MONGODB_URI = "mongodb+srv://achyutammehta:7WvgmzWySS2wCLin@workannivcluster.cbvgni6.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



# Specify the collection name
collection_name = "EmployeeAnniversaryRecords"

# Retrieve all documents from the collection
cursor = db[collection_name].find()

# Iterate through the documents and print the data
for document in cursor:
    print(document)

