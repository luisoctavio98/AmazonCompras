import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class PurchaseCreate(BaseModel):
    """
    Schema for creating a new purchase record via POST.
    """
    product: str
    date: str
    price_per_package: float
    packages: int = 1
    units_per_package: float = 1

app = FastAPI(title="Amazon Purchases AI")

# Load the cleaned Amazon products dataset into a DataFrame
df = pd.read_csv("data/Amazon Products Clean.csv")

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

@app.post("/products", status_code=201)
def create_purchase(purchase: PurchaseCreate):
    global df

    # Fill derived fields to match the DataFrame structure
    total_price = purchase.price_per_package * purchase.packages
    total_units = purchase.packages * purchase.units_per_package
    unit_price = purchase.price_per_package / purchase.units_per_package
    month = purchase.date.split("-")[1].capitalize()

    # Mapping the fields from our Pydantic model to the DataFrame columns
    new_record = {
        "Producto": purchase.product,
        "Fecha": purchase.date,
        "Precio por Paquete": purchase.price_per_package,
        "Paquetes": purchase.packages,
        "Unidades por Paquete": purchase.units_per_package,
        "Precio por Compra": total_price,
        "Unidades por Compra": total_units,
        "Mes": month,
        "Precio por Unidad": unit_price,
    }

    # Append the new record to the DataFrame
    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)

    return new_record