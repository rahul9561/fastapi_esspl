# from fastapi import FastAPI
# from pydantic import BaseModel, EmailStr, Field

# app = FastAPI()

# # Define a Pydantic model for request body validation
# class User(BaseModel):
#     id: int = Field(..., gt=0)                # id must be an int greater than 0
#     name: str = Field(..., min_length=3)     # name must be a string with at least 3 characters
#     email: EmailStr                          # validate email format
#     age: int = Field(None, ge=18, le=100)    # optional age between 18 and 100

# @app.post("/users/")
# async def create_user(user: User):
#     return {"message": "User created", "user": user}



# from fastapi import FastAPI, Query

# app = FastAPI()

# @app.get("/search")
# def search_items(q: str = Query(..., min_length=3, max_length=50)):
#     return {"query": q}

# from fastapi import Depends
# from pydantic import BaseModel, constr
# from fastapi import Form

# class LoginForm(BaseModel):
#     username: constr(min_length=3, max_length=50)
#     password: constr(min_length=6, max_length=100)

# def validate_form(
#     username: str = Form(...),
#     password: str = Form(...)
# ) -> LoginForm:
#     return LoginForm(username=username, password=password)

# @app.post("/login")
# async def login_post(
#     request: Request,
#     form_data: LoginForm = Depends(validate_form)
# ):
#     username = form_data.username
#     password = form_data.password
#     # Continue with your login logic
#     return RedirectResponse(url="/", status_code=303)
