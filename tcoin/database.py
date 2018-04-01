from pymongo import MongoClient

client = MongoClient()

db = client.UserData
    
def file_insert(name_of_file, file_data):
    db.Data.insert_one({
        "file_name": name_of_file,
        "file_data": file_data
    })
