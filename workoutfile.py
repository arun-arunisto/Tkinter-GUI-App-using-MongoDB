from pymongo import MongoClient
import os
from dotenv import load_dotenv
import random

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client.recipes
collection_names = db.list_collection_names() #list out the collections
#print(collection_names)
#recipes
recipes_collection = db.recipes
count_doc = recipes_collection.count_documents({}) #to count the total length of the collection
#print(count_doc)
#going to select one random integer for selecting a recipe
index = random.randint(0, count_doc-1)
recipe = recipes_collection.find_one({"primary_key":{"$eq":index}})
print("Random Recipe:",recipe['title'])

#ingredients
ingredients_collection = db.ingredients
ingredient = ingredients_collection.find({"recipe_key":{"$eq":index}})
print("Ingredients:")
"""
for ing in ingredient:
    print(ing)
"""
ingredients = [str(ing["qty"])+" "+str(ing["unit"])+" "+"of "+ing['name'] for ing in ingredient]
print(ingredients)
client.close()
