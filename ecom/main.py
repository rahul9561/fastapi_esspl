from fastapi import FastAPI ,Request ,HTTPException , Form
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Logs to a file named app.log
        logging.StreamHandler()         # Also prints to console
    ]
)

logger = logging.getLogger(__name__)


app=FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key", session_cookie="session_id")
templates = Jinja2Templates(directory="templates")

@app.get('/')
async def root(req:Request):
    try:
        logger.info("Fetching products from the database")
        conn=sqlite3.connect("ecom.db")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM products")
        products=cursor.fetchall()
        conn.close()
        logger.info(f"Fetched {len(products)} products")
        if not products:
            raise HTTPException(status_code=404, detail="No products found")
        return templates.TemplateResponse("index.html", {"request": req,"products":products})
    except HTTPException as e:
        return {"error": str(e)}
    

@app.get("/signup")
async def signup(req:Request):
    return templates.TemplateResponse("signup.html", {"request": req})


@app.get("/login")
async def login(req:Request):
    return templates.TemplateResponse("login.html", {"request": req})

@app.post('/api/login')
async def login_user(req:Request):
    try:
        logger.info("Processing login request")
        form_data = await req.form()
        username = form_data.get("username")
        password = form_data.get("password")
        
        conn = sqlite3.connect("ecom.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        logger.info(f"User {username} login attempt: {'successful' if user else 'failed'}")
        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password are required")
        if user:
            req.session['user'] = {
                'id': user[0],
                'username': user[1]
            }
        
        if user:
            return RedirectResponse(url="/", status_code=303)
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except HTTPException as e:
        return {"error": str(e)}

@app.post('/signup')
async def create_user(req:Request):
    try:
        logger.info("Processing signup request")

        form_data = await req.form()
        username = form_data.get("username")
        email = form_data.get("email")
        password = form_data.get("password")
        
        conn = sqlite3.connect("ecom.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password,email) VALUES (?, ?, ?)", (username,password , email))
        conn.commit()
        conn.close()
        logger.info(f"User {username} created successfully")
        
        return RedirectResponse(url="/login", status_code=303)
    except HTTPException as e:
        return {"error": str(e)}
from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates
import sqlite3

templates = Jinja2Templates(directory="templates")

# @app.get("/cart")
# async def cart(req: Request):
#     try:
#         user = req.session.get("user")
#         if not user:
#             raise HTTPException(status_code=401, detail="User not logged in")

#         conn = sqlite3.connect("ecom.db")
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT carts.id, carts.quantity, products.title, products.img
#             FROM carts
#             JOIN products ON carts.product_id = products.id
#             WHERE carts.user_id = ?
#         """, (user['username'],))
#         carts = cursor.fetchall()
#         conn.close()

#         return templates.TemplateResponse("cart.html", {"request": req, "carts": carts})

#     except HTTPException as e:
#         return {"error": str(e.detail)}
#     except Exception as e:
#         return {"error": str(e)}

    

# @app.post("/add_to_cart")
# async def add_to_cart(req:Request):
#     try:
#         form_data = await req.form()
#         product_id = form_data.get("product_id")
#         user=req.session.get('user')
#         if not user or not product_id:
#             raise HTTPException(status_code=400, detail="Invalid user or product ID")
        

        
#         user_id = user['username']
#         conn = sqlite3.connect("ecom.db")
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM carts WHERE user_id=? AND product_id=?", (user_id, product_id))
#         existing_cart = cursor.fetchone()
#         if existing_cart:
#             cursor.execute("UPDATE carts SET quantity = quantity + 1 WHERE user_id=? AND product_id=?", (user_id, product_id))
#         else:
#             cursor.execute("INSERT INTO carts (user_id, product_id, quantity) VALUES (?, ?, ?)", (user_id,product_id, 1))
#         conn.commit()
#         conn.close()
        
#         return RedirectResponse(url="/cart", status_code=303)
#     except HTTPException as e:
#         return {"error": str(e)}





@app.post('/add/card')
async def add_to_cart(req:Request ,product_id:int=Form(...)):
    try:
        logger.info("Processing add to cart request")
        user=req.session.get('user')
        user_id= user['id'] if user else None
        if not user:
            raise HTTPException(status_code=401, detail="User not logged in")
        
        
        conn=sqlite3.connect("ecom.db")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM carts WHERE user_id=? AND product_id=? ",
                       (user_id,product_id))
        product_exists=cursor.fetchone()
        if product_exists:
            cursor.execute("UPDATE carts SET quantity=quantity+1 WHERE user_id=? AND product_id=? ",
                           )
        else:   
            cursor.execute("INSERT INTO carts (user_id, product_id, quantity) VALUES(?, ?,?)",
                       (user_id,product_id,1))
        conn.commit()
        conn.close()
        logger.info(f"Product {product_id} added to cart for user {user_id}")
        return RedirectResponse(url="/cart", status_code=303)
    except HTTPException as e:
        return {"error": str(e)}
    
@app.get('/cart')
async def cart(req:Request):
    try:
      conn=sqlite3.connect("ecom.db")
      cursor=conn.cursor()
      cursor.execute("SELECT * FROM carts")
      carts=cursor.fetchall()
      conn.close()
      return templates.TemplateResponse("cart.html", {"request": req,"carts":carts})
    except HTTPException as e:
        return {"erorr":str(e)}   