from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import text
from datetime import datetime
from pydantic import BaseModel


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
    "mssql+pyodbc://DESKTOP-CUC3UNM\\SQLEXPRESS/rahuldb"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)




engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

app = FastAPI()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Connected to rahuldb on SQLEXPRESS!"}

# @app.post("/add_product/")
# def add_product_nex():
#     db = SessionLocal()
#     try:
#         new_product = Product(
#             name="Test Product",
#             description="Test Description",
#             price=199.99,
#             stock=5,
#             image_url="https://example.com/test.jpg"
#         )
#         db.add(new_product)
#         db.commit()
#         db.refresh(new_product)
#         return {"message": "Product added", "product": new_product.name}
#     finally:
#         db.close()

@app.get("/products/")
def get_products():
    db = SessionLocal()
    try:
        logger.info("Fetching all products")
        result = db.execute(text("SELECT * FROM products"))
        products = [dict(row._mapping) for row in result.fetchall()]
        logger.info(f"Fetched {len(products)} products")
        return {"products": products}
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return {"error": str(e)}
    finally:
        db.close()
    
class product(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    image_url: str


@app.post("/product/add/")
async def add_product(product: product):
    db = SessionLocal()
    try:
        logger.info(f"Attempting to add product: {product.name}")
        db.execute(
            text(
                "INSERT INTO products (name, description, price, stock, image_url) "
                "VALUES(:name, :description, :price, :stock, :image_url)"
            ),
            {
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "image_url": product.image_url,
            },
        )
        db.commit()
        logger.info(f"Product '{product.name}' added successfully.")
        return {"message": "Product added successfully"}
    except Exception as e:
        logger.error(f"Error adding product: {e}")
        return {"error": str(e)}
    finally:
        db.close()


@app.get("/product/{product_id}")
def get_product(product_id: int):
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT * FROM products WHERE id = :id"), {"id": product_id})
        product = result.fetchone()
        if product:
            return {"product": dict(product._mapping)}
        else:
            return {"message": "Product not found"}
    finally:
        db.close()