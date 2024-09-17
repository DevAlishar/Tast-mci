from fastapi import FastAPI
from app.module import say_hello

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": say_hello()}
