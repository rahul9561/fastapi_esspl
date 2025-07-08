from fastapi import FastAPI, Query
from typing import List

app = FastAPI()

fake_data = [{"id": i, "value": f"Item {i}"} for i in range(1, 101)]

@app.get("/items/")
def get_items(skip: int = Query(0), limit: int = Query(10)):
    return {
        "total": len(fake_data),
        "skip": skip,
        "limit": limit,
        "data": fake_data[skip : skip + limit]
    }
