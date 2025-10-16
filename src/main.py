from fastapi import FastAPI
from src.routers import user
from src.routers import business


app = FastAPI(title="КУ")

app.include_router(user.router)
app.include_router(business.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}


