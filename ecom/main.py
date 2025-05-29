from fastapi import FastAPI ,Request ,HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3

app=FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get('/')
async def root(req:Request):
    try:
        conn=sqlite3.connect("ecom.db")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM products")
        products=cursor.fetchall()
        conn.close()
        return templates.TemplateResponse("index.html", {"request": req,"products":products})
    except HTTPException as e:
        return {"error": str(e)}
    

@app.get("/signup")
async def signup(req:Request):
    return templates.TemplateResponse("signup.html", {"request": req})
