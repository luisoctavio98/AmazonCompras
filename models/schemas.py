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