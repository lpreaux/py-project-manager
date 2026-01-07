from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from src.config import create_db_and_tables
from .routers import router


app = FastAPI()
app.include_router(router)

create_db_and_tables()

# Define a simple root endpoint to check the connection
@app.get("/")
def read_root():
    return {"message": "Connected to the database!"}

print("Server started")