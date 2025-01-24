import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional


app = FastAPI()

# SQLite database connection
DATABASE_NAME = "expenditure.db"

# SQLite query to create the table (if it doesn't exist)
def create_table():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        item TEXT NOT NULL,
        amount REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()

create_table()

# Pydantic model to define the structure of incoming data
class Item(BaseModel):
    name: str
    item: str
    amount: float


# Endpoint to add an item
@app.post("/items/", status_code=201)
def add_item(item: Item):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO items (name, item, amount) VALUES (?, ?, ?)
        """, (item.name, item.item, item.amount))
        conn.commit()
        conn.close()
##        return {"message": "Item added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error while adding item")


# Endpoint to fetch all items
@app.get("/items", response_model=List[Item])
def get_all_items():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        rows = cursor.fetchall()
        conn.close()
        items = [{"name": row[1], "item": row[2], "amount": row[3]} for row in rows]
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error while fetching items")


# To delete data

@app.delete("/items/{item_id}/")  
def delete_item(item_id: int):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Check if the item exists
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchall()

        if not item:
            conn.close()
            raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found.")

        # Delete the item
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()

        return {"message": f"Item with ID {item_id} has been deleted successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting item: {str(e)}")



# To delete data

@app.delete("/items/")  
def delete_item_by_name(username: Optional[str] = None):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Check if the item exists
        cursor.execute("SELECT * FROM items WHERE name = ?", (username,))
        items = cursor.fetchall()

        if not items:
            conn.close()
            raise HTTPException(status_code=404, detail=f"Item with ID {username} not found.")

        # Delete the item
        cursor.execute("DELETE FROM items WHERE name = ?", (username,))
        conn.commit()
        conn.close()

        return {"message": f"Item with name {username} has been deleted successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting item: {str(e)}")

##from fastapi import FastAPI, HTTPException
##from pydantic import BaseModel
##import sqlite3
##from datetime import date
##
##app = FastAPI()
##
##
##DB_NAME = "contributions.db"
##
##def init_db():
##    #"""Initializ the database and create the table if not exists."""
##    conn = sqlite3.connect(DB_NAME)
##    cursor = conn.cursor()
##    cursor.execute("""
##    CREATE TABLE IF NOT EXISTS contributions (   
##        id INTEGER PRIMARY KEY AUTOINCREMENT,
##        user TEXT NOT NULL,
##        item TEXT NOT NULL,
##        amount REAL NOT NULL,
##        date TEXT NOT NULL
##    )
##    """)   #making making the contents ie id name item amoutn date
##
##    conn.commit()
##    conn.close()
##
##init_db()
##
###pydantic models
##
##class Contribution(BaseModel):
##    user: str
##    item: str
##    amount: float
##    date: str = str(date.today())  # Default to today's date
##
##class ContributionUpdate(BaseModel):
##    user: str
##    item: str
##    amount: float
##
##### CRUD endpoinnts
##@app.post("/contributions/")
##def add_contribution(contribution: Contribution):
##    conn = sqlite3.connect(DB_NAME)
##    cursor = conn.cursor()
##
##    cursor.execute("INSERT INTO contributions (user, item, amount, date) VALUES (?, ?, ?, ?)",
##                   (contribution.user, contribution.item, contribution.amount, contribution.date))
##    conn.commit()
##    conn.close()
##    return {"message": "Contribution added successfully"}
##
##
##@app.get("/contributions/")
##def get_contributions(user: str = None):
##    conn = sqlite3.connect(DB_NAME)
##    cursor = conn.cursor()
##
##    if user:
##        cursor.execute("SELECT * FROM contributions WHERE user = ?", (user,))
##    else:
##        cursor.execute("SELECT * FROM contributions")
##
##    rows = cursor.fetchall()
##    
##    conn.close()
##    return {"contribution": rows, "lenght": len(rows)}
##
##@app.put("/contributions/{contribution_id}/")           ### modify the data
##def update_contribution(contribution_id: int, update: ContributionUpdate):
##    conn = sqlite3.connect(DB_NAME)
##    cursor = conn.cursor()
##    cursor.execute("UPDATE contributions SET user = ?, item = ?, amount = ? WHERE id = ?", (update.user, update.item, update.amount, contribution_id))
##    conn.commit()
##    conn.close()
##    return {"message": "Contribution updated successfully"}
##
##@app.delete("/contributions/{contribution_id}/")        ## to delete data
##def delete_contribution(contribution_id: int, update: ContributionUpdate):
##    conn = sqlite3.connect(DB_NAME)
##    cursor = conn.cursor()
##    cursor.execute("DELETE FROM contributions WHERE user = ?, id = ?", (update.user, contribution_id,))
##    conn.commit()
##    conn.close()
##    return {"message": "Contribution deleted successfully"}
##
##
##
















