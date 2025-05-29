from fastapi import FastAPI ,UploadFile
 
app=FastAPI()



# Query Parameter ?
@app.get('/item')
async def product(item:str):
    return {"items":item}


@app.get("/search")
def search(term: str, limit: int = 10):
    return {"term": term, "limit": limit}

# URL: /search?term=apple&limit=5

# path parameter
@app.get("/product/{items}")
async def items(items:int):
    return {"items":items}

@app.post("/upload")
async def upload_files(file:UploadFile):
    return {"message": file}