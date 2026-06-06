from fastapi import FastAPI
from routers import products

app = FastAPI(title="Amazon Purchases AI")

# Register product endpoints from the products router module
app.include_router(products.router)