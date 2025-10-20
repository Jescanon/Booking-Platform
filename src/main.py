from fastapi import FastAPI
from src.routers import user
from src.routers import business
from src.routers import worker
from src.routers import service
from src.routers import booking



app = FastAPI(title="КУ")

app.include_router(user.router)
app.include_router(business.router)
app.include_router(worker.router)
app.include_router(service.router)
app.include_router(booking.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}


