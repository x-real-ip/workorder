from fastapi import FastAPI

app = FastAPI()


@app.get("/clock")
def index():
    return "Hey"
