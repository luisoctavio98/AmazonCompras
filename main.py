from fastapi import FastAPI
from routers import products

app = FastAPI(
    title="Amazon Purchases API",
    description="API for managing and querying Amazon purchase records.",
    version="1.0.0",
)

# Register product endpoints from the products router module
app.include_router(products.router)