from fastapi import APIRouter, HTTPException
from models.schemas import PurchaseCreate
from services import data_service

router = APIRouter()

# Endpoint to retrieve all products or a specific product
@router.get("/products")
def get_products(product: str | None = None):
    """Return all products, optionally filtered by name."""
    return data_service.get_products(product)

# Endpoint to retrieve a specific product by its ID (using the row index)
@router.get("/products/{product_id}")
def get_product(product_id: int):
    """Return a specific product by ID, or None if it doesn't exist."""
    product_details = data_service.get_product(product_id)
    if not product_details:
        # Return a 404 Not Found HTTP error
        raise HTTPException(status_code=404, detail="Product not found")
    return product_details

@router.post("/products", status_code=201)
def create_purchase(purchase: PurchaseCreate):

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
    data_service.add_purchase(new_record)
    
    return new_record