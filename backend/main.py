from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "NBA AI Predictor API Running"}