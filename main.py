from fastapi import FastAPI

app = FastAPI(title="Amazon Compras AI")

@app.get("/")
def root():
    return {"status": "ok", "message": "Prep day complete!"}