from fastapi import APIRouter, HTTPException
from models.item import Item
from models.user_clockin import ClockInRecord
from schemas.schema import clockin_serial, list_clockin_serial
from config.database import items_collection, user_clockin_collection
from schemas.schema import item_serial, list_item_serial
from bson import ObjectId
from typing import Optional
from datetime import datetime
router = APIRouter()

# Part A
@router.get("/")
async def read_root():
    return {"message":"Hello There"}

# POST/items input: Name, Email, ItemName, Quantity, EXP_DATE
@router.post('/items')
async def post_item(item: Item):
    try:
        obj = items_collection.insert_one(dict(item))
        return {"status_code": 200, "id": str(obj.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occured: {str(e)}")


# GET/items
@router.get('/items')
async def get_items():
    try:
        items = list_item_serial(items_collection.find())
        return items
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"error: {str(e)}")


# GET/item{id}
@router.get('/item/{id}')
async def get_item(id: str):
    try:
        item = item_serial(items_collection.find_one({"_id": ObjectId(id)}))
        return item
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Item not found : {str(e)}")


# GET/item/filter
@router.get("/items/filter")
async def filter_items(
        email: Optional[str] = None,
        expiry_date: Optional[datetime] = None,
        insert_date: Optional[datetime] = None,
        quantity: Optional[int] = None
                      ):
    query = {}

    # Email match
    if email:
        query["email"] = str(email)

    # EXP_DATE after filter date { "expiry_date": {"$gt": expiry_date} }
    if expiry_date:
        query["expiry_date"] = {"$gt": expiry_date}

    # Items Inserted Date after filter date
    if insert_date:
        query["insert_date"] = {"$gt": insert_date}

    # Quantity greater than or equal to filter value
    if quantity is not None:
        query["quantity"] = {"$gt": quantity}
    try:
        items = list_item_serial(items_collection.find(query))
        return items
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error: {str(e)}")


# PUT/item/{id}
@router.put('/item/{id}')
async def update_item(id: str, item: Item):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="invalid ObjectId")
    # Removing insert date from dict
    data = dict(item)
    del data["insert_date"]
    try:
        obj = items_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": data}
            )
        return {"updated Item": f"{str(obj["_id"])}"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error {str(e)}")
        # Exclude Inserted Date


# Delete/item/{id}
@router.delete('/item/{id}')
async def delete_item(id: str):
    try:
        items_collection.find_one_and_delete({"_id": ObjectId(id)})
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error {str(e)}")


# MongoDB Aggregate data to return count of items by each email
@router.get("/email-counts")
async def get_email_item_counts():
    pipeline = [
        {
            "$group": {
                "_id": "$email",
                "itemCount": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "email": "$_id",
                "itemCount": 1
            }
        }
    ]
    results = items_collection.aggregate(pipeline).to_list(length=None)
    return results


# PartB

# POST/clockin
@router.post('/clockin')
async def post_clockin(clockin: ClockInRecord):
    try:
        resp = user_clockin_collection.insert_one(dict(clockin))
        return {"status_code": 200, "id": str(resp.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get('/clockin')
async def get_clockins():
    try:
        resp = list_clockin_serial(user_clockin_collection.find())
        return resp

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error {str(e)}")


# GET/clockin{id}
@router.get('/clockin/{id}')
async def get_clockin(id: str):
    try:
        resp = clockin_serial(user_clockin_collection.find_one({"_id": ObjectId(id)}))
        return resp
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error: {str(e)}")


# GET/clockin/filter
@router.get("/clockinfilter")
async def filter_clockin(
    email: Optional[str] = None,
    location: Optional[str] = None,
    clockins: Optional[datetime] = None,
                        ):
    query = {}
    if email:
        query["email"] = str(email)
    if location:
        query["location"] = str(location)
    if clockins:
        query["clockin"] = {"$gt": clockins}
    try:
        resp = list_clockin_serial(user_clockin_collection.find(query))
        return resp
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error {str(e)}")


# Delete/clockin{id}
@router.delete('/clockin/{id}')
async def delete_clockin(id: str):
    try:
        user_clockin_collection.find_one_and_delete({"_id": ObjectId(id)})
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error {str(e)}")


# PUT/clockin{id}
@router.put('/clockin/{id}')
async def update_clockin(id: str, clockin: ClockInRecord):
    data = dict(clockin)
    del data["clockin"]
    try:
        obj = user_clockin_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": data}
            )
        return {"updated clockin": f"{str(obj["_id"])}"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error {str(e)}")
        # Exclude Inserted Date
