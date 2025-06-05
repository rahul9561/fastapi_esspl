from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
import sqlite3 as sql

app = FastAPI()

# Constants
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database Connection
def create_connection():
    return sql.connect('OAUTHauthentication.db')

# JWT Token Creator
def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic Model for Signup
class User(BaseModel):
    username: str
    email: str
    password: str

# Signup Route
@app.post('/api/signup')
async def signup(user: User):
    conn = create_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                  (user.username, user.email, user.password))
        conn.commit()
    except sql.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    finally:
        conn.close()
    return {"message": f"User {user.username} created successfully"}

# Login Route - returns JWT Token
# OAuth2PasswordRequestForm is used to parse the form data It is a built-in class from fastapi.
# security that expects data submitted using the 
# application/x-www-form-urlencoded format (like regular HTML forms or Postman form fields).
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", 
              (form_data.username, form_data.password))
    user = c.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected Route
@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
