from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/booking")
async def rootss():
    return {"message": "Hello World"}