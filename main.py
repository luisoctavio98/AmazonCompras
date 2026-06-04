import pandas as pd
from fastapi import FastAPI, HTTPException

# Load the cleaned Amazon products dataset into a DataFrame
df = pd.read_csv("data/Amazon Products Clean.csv")

app = FastAPI(title="Amazon Purchases AI")

# Endpoint to retrieve all products or a specific product
@app.get("/products")
def get_products(product: str | None = None):

    # Filter the dataset when a product query parameter is provided
    if product:
        filtered_df = df[df['Producto'] == product]
        return filtered_df.to_dict(orient="records")

    # Return the entire dataset
    return df.to_dict(orient="records")

# Endpoint to retrieve a specific product by its ID (using the row index)
@app.get("/products/{product_id}")
def get_product(product_id: int):
    # Check if the requested ID (row index) exists in our dataset
    if product_id < 0 or product_id >= len(df):
        # Return a 404 Not Found HTTP error
        raise HTTPException(status_code=404, detail="Product not found")
        
    # Extract the specific row and convert it to a dictionary
    product_details = df.iloc[product_id]
    return product_details.to_dict()
