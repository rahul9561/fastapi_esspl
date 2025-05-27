from fastapi import FastAPI, Request ,Form , HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def db_connection():
    return sqlite3.connect("database.db")
    


@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup")
async def signup_to(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})






@app.post("/login_post")
async def login_post(request: Request,username: str=Form(...), password: str=Form(...)):
    try:
        conn=db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                        (username, password))
        user=cursor.fetchone()
        conn.close()
        return RedirectResponse(url="/")
    except Exception as e:
        return {"error":str(e)}
    
@app.post("/register")
async def signup(req:Request,username:str=Form(...), password:str=Form(...), email:str=Form(...)):
    try:
        conn=db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                        (username, password, email))
        conn.commit()
        conn.close()
        return {"message":"User registered successfully"}
    except sqlite3.IntegrityError:
        return {"error":"Username or email already exists"}
    except Exception as e:
        return {"error":str(e)}



@app.get("/")
async def root():
    return {"message": "Hello, World!"}


import json

@app.get("/products")
async def products(request: Request):
    with open("product.json","r") as f:
        products=json.load(f)
    return templates.TemplateResponse("product.html", {"request": request,"products":products})


@app.get("/api/products")
async def api_products(req:Request):
    try:
        conn=db_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM product")
        products=cursor.fetchall()
        conn.close()
        # if rows:
        #     products = dict(rows)
        #     return products

        # return {"products": products}
        return templates.TemplateResponse("api_products.html", {"request": req, "products": products})
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/api/products/{product_id}")
async def api_product_detail(req:Request, product_id:int):
    try:
        conn=db_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM product WHERE id=?", (product_id,))
        product=cursor.fetchone()
        conn.close()
        # if row:
        #     product_dict = dict(row)
        #     return product_dict
        # else:
        #     raise HTTPException(status_code=404, detail="Product not found")
        # return {"product": product}
        if product:
            return templates.TemplateResponse("api_product_detail.html", {"request": req, "products": product})
        else:
            return {"error": "Product not found"}
    except Exception as e:
        return {"error": str(e)}
    





@app.post("/api/products/{product_id}")
async def delete_product(req:Request, product_id:int):
    try:
        conn=db_connection()
        cursor=conn.cursor()
        cursor.execute("DELETE FROM product WHERE id=?",(product_id,))
        conn.commit()
        conn.close()
        return {"message": "Product deleted successfully"}
    except Exception as e:
        return {"error": str(e)}