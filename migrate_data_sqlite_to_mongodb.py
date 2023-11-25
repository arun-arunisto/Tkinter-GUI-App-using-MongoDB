import sqlite3
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import time

def data_transfer(data, column_names, collection_name):
    no = 0
    for i in range(len(data)):
        sample_data = {}
        for j in range(len(data[i])):
            sample_data[column_names[j]] = data[i][j]
        result = collection_name.insert_one(sample_data)
        #print(sample_data)
        no+=1
        print("Data Count:",no,"Document id:",result.inserted_id)
    print(f"Successfully Migrated {no} Documents!!")

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client.recipes
recipes_collection = db.recipes
ingredients_collection = db.ingredients

conn = sqlite3.connect("recipes.db")
cur = conn.cursor()

cur.execute("SELECT * FROM ingredients")
data = cur.fetchall()
column_names = [column[0] for column in cur.description]
#print(column_names)
#print(data)
"""
start_time = time.time()
data_transfer(data, column_names, recipes_collection)
end_time = time.time()
print("Time take to migrate [recipes]:",end_time - start_time)"""
"""
start_time = time.time()
data_transfer(data, column_names, ingredients_collection)
end_time = time.time()
print("Time take to migrate [ingredients]:",round((end_time - start_time)/60),"Minutes")
"""
#filtering None data to blank
"""
doc_to_filter = {"qty":{"$eq":None}}
update_field = {"$set":{"qty":" "}}
result = ingredients_collection.update_many(doc_to_filter, update_field)
print("Document Matched:",result.matched_count)
print("Updated Count:",result.modified_count)
"""

"""doc_to_filter = {"unit":{"$eq":None}}
update_field = {"$set":{"unit":" "}}
result = ingredients_collection.update_many(doc_to_filter, update_field)
print("Document Matched:",result.matched_count)
print("Updated Count:",result.modified_count)"""

"""none_data = ingredients_collection.find({"qty":{"$eq":" "}})
for i in none_data:
    print(i)"""


"""for i in range(len(data)):
    sample_data = {}
    for j in range(len(data[i])):
        sample_data[column_names[j]] = data[i][j]
    print(sample_data)"""

cur.close()
conn.close()
client.close()