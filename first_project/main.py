from fastapi import FastAPI, Request ,Form , HTTPException ,Depends
from fastapi.responses import HTMLResponse , JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel ,EmailStr
import sqlite3
import os
import smtplib
import bcrypt

app=FastAPI()

app.add_middleware(SessionMiddleware, secret_key="1834t3vyf63fvsi")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def db_connection():
    return sqlite3.connect("database.db")
    
def current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

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
        if user :
            request.session["user"] = {"id": user[0], "username": user[1]}
            return RedirectResponse(url="/", status_code=303)
        else:
            context= {"request": request, "error": "Invalid username or password"}
            return templates.TemplateResponse("login.html", context)
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
async def root(request: Request,user = Depends(current_user)):
    try:
        conn=db_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM product")
        products=cursor.fetchall()
        conn.close()
        context={"request": request, "products": products,"user": user}
        return templates.TemplateResponse("index.html", context)
    except Exception as e:
        return {"error": str(e)}
    # 'user' will be dict from session, e.g. {"id": ..., "username": ...}
    


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
    
cart=[]



@app.post("/cart/add")
async def add_cart(req: Request, product_id: int = Form(...)):
    user = req.session.get("user")

    if not user:
        return JSONResponse(content={"error": "User not authenticated"}, status_code=401)

    user_id = user.get("id")

    try:
        conn = db_connection()
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        # Check if product exists
        cursor.execute("SELECT * FROM product WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        if not product:
            conn.close()
            return JSONResponse(content={"error": "Product not found"}, status_code=404)

        # Check if product already in cart
        cursor.execute(
            "SELECT quantity FROM carts WHERE user_id = ? AND product_id = ?",
            (user_id, product_id)
        )
        existing = cursor.fetchone()

        if existing:
            # Update quantity
            cursor.execute(
                "UPDATE carts SET quantity = quantity + 1 WHERE user_id = ? AND product_id = ?",
                (user_id, product_id)
            )
        else:
            # Insert new cart item
            cursor.execute(
                "INSERT INTO carts (user_id, product_id, quantity) VALUES (?, ?, ?)",
                (user_id, product_id, 1)
            )

        conn.commit()
        conn.close()
        return RedirectResponse(url="/cart", status_code=303)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    


# path parameter
@app.get('/product/{i}')
async def items(i):
    return {"items": i}

# Query Parameter 
@app.get('/item')
async def product(item: str):
    return {"items": item}



@app.get("/logout")
def logout(request: Request):
    request.session.pop("user")
    return RedirectResponse(url="/login", status_code=303) 


@app.get("/cart", response_class=HTMLResponse)
async def view_cart(req: Request):
    user = req.session.get("user")

    if not user:
        # Redirect to login instead of rendering login.html directly
        return RedirectResponse(url="/login", status_code=303)

    user_id = user.get("id")

    try:
        conn = db_connection()
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        # Join carts and product tables
        cursor.execute("""
            SELECT 
                product.id,             -- 0
                product.name,           -- 1
                product.description,    -- 2
                product.price,          -- 3
                product.stock,          -- 4
                product.image,          -- 5
                product.category,       -- 6
                carts.quantity          -- 7
            FROM carts
            JOIN product ON carts.product_id = product.id
            WHERE carts.user_id = ?
        """, (user_id,))
        
        cart_items = cursor.fetchall()
        conn.close()
        print("Cart data",cart_items)
        return templates.TemplateResponse("cart.html", {
            "request": req,
            "cart": cart_items,
            "user": user
        })

    except Exception as e:
        return {"error": str(e)}
    

    

    
@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})



# Your email credentials (use environment variables or a secrets manager in production)
SENDER_EMAIL = "example@gmail.com"
SENDER_PASSWORD = "app password"  # Use an App Password if using Gmail


@app.post("/email/sender")
async def send_email(
    name: str = Form(...),
    email: EmailStr = Form(...),
    subject: str = Form(...),
    message: str = Form(...)
):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = email
        msg["Subject"] = subject

        body = f"""
        Hello {name},

        {message}

        Regards,
        Your Team
        """
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())

        return JSONResponse(content={
            "success": True,
            "message": f"Email sent to {email}"
        }, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)