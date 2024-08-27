from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Supplier

app = FastAPI() # Initialize the object

@app.get("/")
def root() -> None:
    return {"message": "Hello world!"}

@app.get("/getSuppliers")
def get_suppliers() -> list[Supplier]:
    pass