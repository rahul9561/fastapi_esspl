from fastapi import FastAPI
from sqlalchemy import create_engine ,text
from pydantic import BaseModel ,Field
from sqlalchemy.orm import sessionmaker, declarative_base
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

DATABASE_URL = (
    "mssql+pyodbc://DESKTOP-CUC3UNM\\SQLEXPRESS/ecom"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



app=FastAPI()

class User(BaseModel):
    username: str=Field(..., min_length=3, max_length=50)
    email: str=Field(..., min_length=3, max_length=50)
    password: str=Field(..., min_length=3, max_length=50)

@app.post('/api/signup')
async def signup(user:User):
    db=SessionLocal()
    try:
        logger.info(f"Attempting to add product: {user.username}")
        db.execute(text("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",) ,  {
            "username": user.username,
            "email": user.email,
            "password": user.password
          }  )
        
        db.commit()
        logger.info(f"Product '{user.username}' added successfully.")
        return {"message": "User created successfully", "username": user.username}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()




@app.get('/')
async def root():
    return {"message": "Connected to rahuldb on SQLEXPRESS!"}


class Login(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=3, max_length=50)

@app.post('/api/login')
async def login(user: Login):
    db = SessionLocal()
    try:
        logger.info(f"Attempting to add product: {user.username}")
        result = db.execute(
            text("SELECT * FROM users WHERE username = :username AND password = :password"),
            {"username": user.username, "password": user.password}
        ).fetchone()
        logger.info(f"Product '{user.username}' added successfully.")
        if result:
            return {"message": "Login successful", "username": user.username}
        else:
            return {"error": "Invalid username or password"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

