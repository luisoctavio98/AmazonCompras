import pandas as pd

# Load the cleaned Amazon products dataset into a DataFrame
df = pd.read_csv("data/Amazon Products Clean.csv")

def get_products(product: str | None = None):
    
    # Filter the dataset when a product query parameter is provided
    if product:
        filtered_df = df[df['Producto'] == product]
        return filtered_df.to_dict(orient="records")

    # Return the entire dataset
    return df.to_dict(orient="records")

def get_product(product_id: int):
    
    # Check if the requested ID (row index) exists in our dataset
    if product_id < 0 or product_id >= len(df):
        return None

    # Extract the specific row and convert it to a dictionary
    product_details = df.iloc[product_id]
    return product_details.to_dict()

# Avoid needing importing pandas in the routers
def add_purchase(record: dict):
    """Append a new purchase record to the in-memory DataFrame."""
    global df
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
