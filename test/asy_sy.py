from fastapi import FastAPI
import time
import asyncio

app = FastAPI()

# 🐢 Blocking (sync) endpoint
@app.get("/sync")
def sync_sleep():
    time.sleep(5)  # Blocks the whole thread for 5 seconds
    return {"message": "Finished sync sleep"}

# ⚡ Non-blocking (async) endpoint
@app.get("/async")
async def async_sleep():
    await asyncio.sleep(5)  # Does not block the event loop
    return {"message": "Finished async sleep"}

   