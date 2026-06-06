from fastapi import APIRouter, HTTPException
from models.schemas import PurchaseCreate
from services import data_service

router = APIRouter(tags=["Products"])

@router.get("/products", summary="Retrieve all products")
def get_products(product: str | None = None):
    """Returns all products in the database. Can optionally be filtered by a specific product name."""
    return data_service.get_products(product)

@router.get("/products/{product_id}", summary="Retrieve a specific product by ID")
def get_product(product_id: int):
    """Fetches a specific product using its row index. Returns a 404 error if the ID does not exist in the dataset."""
    product_details = data_service.get_product(product_id)
    if not product_details:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_details

@router.post("/products", status_code=201, summary="Register a new purchase")
def create_purchase(purchase: PurchaseCreate):
    """Calculates total price, unit price, and month from the provided purchase data, then adds it to the database."""

    total_price = purchase.price_per_package * purchase.packages
    total_units = purchase.packages * purchase.units_per_package
    unit_price = purchase.price_per_package / purchase.units_per_package
    month = purchase.date.split("-")[1].capitalize()

    # Mapping the fields from our Pydantic model to a dictionary
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

    data_service.add_purchase(new_record)
    
    return new_record