"""
Simple FastAPI server for product search demo.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Optional
import sys
import os

# Add parent directory to path to import api modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="Product Search API")

# Enable CORS for browser demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data for demo (since we don't have Elasticsearch set up)
MOCK_PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "description": "Premium noise-cancelling headphones", "price": 199.99, "category": "Electronics", "stock_quantity": 15, "rating": 4.5},
    {"id": 2, "name": "Python Programming Book", "description": "Learn Python from scratch", "price": 49.99, "category": "Books", "stock_quantity": 8, "rating": 4.8},
    {"id": 3, "name": "Cotton T-Shirt", "description": "Comfortable everyday t-shirt", "price": 24.99, "category": "Clothing", "stock_quantity": 0, "rating": 4.2},
    {"id": 4, "name": "Coffee Maker", "description": "Programmable coffee maker", "price": 89.99, "category": "Home", "stock_quantity": 12, "rating": 4.6},
    {"id": 5, "name": "Smartphone", "description": "Latest model smartphone", "price": 699.99, "category": "Electronics", "stock_quantity": 5, "rating": 4.7},
    {"id": 6, "name": "JavaScript Guide", "description": "Complete guide to modern JavaScript", "price": 39.99, "category": "Books", "stock_quantity": 20, "rating": 4.9},
    {"id": 7, "name": "Running Shoes", "description": "Lightweight running shoes", "price": 129.99, "category": "Clothing", "stock_quantity": 7, "rating": 4.4},
    {"id": 8, "name": "Stand Mixer", "description": "Professional stand mixer", "price": 299.99, "category": "Home", "stock_quantity": 3, "rating": 4.7},
]

@app.get("/")
async def root():
    """Serve the demo HTML file."""
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "demo.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"message": "Demo API", "endpoints": ["/api/products/search", "/docs"]}

@app.get("/api/products/search")
async def search_products(
    query: Optional[str] = "",
    category: Optional[str] = "",
    availability: Optional[str] = "",
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None
):
    """
    Search products with filters (mock implementation for demo).
    
    This simulates the Elasticsearch search_products method.
    """
    filters = {}
    if category:
        filters['category'] = category
    if availability:
        filters['availability'] = availability.lower() == 'true'
    if min_price is not None or max_price is not None:
        filters['price_range'] = {}
        if min_price is not None:
            filters['price_range']['min'] = min_price
        if max_price is not None:
            filters['price_range']['max'] = max_price
    if min_rating is not None:
        filters['rating'] = min_rating
    
    # Filter products (simulating Elasticsearch logic)
    results = []
    for product in MOCK_PRODUCTS:
        # Text search
        if query:
            query_lower = query.lower()
            if query_lower not in product['name'].lower() and query_lower not in product['description'].lower():
                continue
        
        # Category filter
        if 'category' in filters:
            if product['category'] != filters['category']:
                continue
        
        # Availability filter
        if 'availability' in filters:
            availability_match = filters['availability']
            if availability_match and product['stock_quantity'] == 0:
                continue
            if not availability_match and product['stock_quantity'] > 0:
                continue
        
        # Price range filter
        if 'price_range' in filters:
            price_range = filters['price_range']
            if 'min' in price_range and product['price'] < price_range['min']:
                continue
            if 'max' in price_range and product['price'] > price_range['max']:
                continue
        
        # Rating filter
        if 'rating' in filters:
            if product['rating'] < filters['rating']:
                continue
        
        results.append(product)
    
    # Sort by rating (desc) then name (asc)
    results.sort(key=lambda x: (-x['rating'], x['name']))
    
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

