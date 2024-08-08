import pymongo

# Connect to local MongoDB instance
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Test connection
db = client.test_database
print("Connected to MongoDB")

client.close()