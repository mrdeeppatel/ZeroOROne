from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import os

app = FastAPI()

# MongoDB connection
MONGO_URI = os.environ.get("MONGO_URI") or "mongodb+srv://100xDev:i0XUrTfJXBtKTdk4@cluster0.9uh7q.mongodb.net/ZeroOrOne?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["ZeroOrOne"]
collection = db["data"]

# Utility to convert ObjectId to string for JSON
def convert_id(item):
    item["_id"] = str(item["_id"])
    return item

# GET all data
@app.get("/data")
def get_all_data():
    items = list(collection.find({}))
    return [convert_id(i) for i in items]

# GET data by Roll_No
@app.get("/data/roll/{roll_no}")
def get_data_by_roll(roll_no: str):
    item = collection.find_one({"Roll_No": roll_no})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return convert_id(item)

# DELETE data by Roll_No
@app.delete("/data/roll/{roll_no}")
def delete_data_by_roll(roll_no: str):
    result = collection.delete_one({"Roll_No": roll_no})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": f"Item with Roll_No {roll_no} deleted successfully"}
