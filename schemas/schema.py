# Schema for Item
def item_serial(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "itemName": item["itemName"],
        "quantity": item["quantity"],
        "expiry_date": item["expiry_date"],
        "insert_date": item["insert_date"],
    }


def list_item_serial(items) -> list:
    return [item_serial(item) for item in items]


# Schema for Clockin
def clockin_serial(clockin) -> dict:
    return {
        "id": str(clockin["_id"]),
        "email": clockin["email"],
        "location": clockin["location"],
        "clockin": clockin["clockin"]
    }


def list_clockin_serial(clockins) -> list:
    return [clockin_serial(clockin) for clockin in clockins]
