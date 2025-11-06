"""
Product API endpoints.
"""
from typing import List, Dict, Optional
from datetime import datetime

class ProductService:
    """Service for managing product operations."""
    
    def __init__(self, db_connection, cache):
        self.db = db_connection
        self.cache = cache
    
    async def get_product(self, product_id: int) -> Optional[Dict]:
        """Retrieve a product by ID with caching."""
        cache_key = f"product:{product_id}"
        
        if cached := await self.cache.get(cache_key):
            return cached
        
        product = await self.db.fetch_one(
            "SELECT * FROM products WHERE id = ?", 
            product_id
        )
        
        if product:
            await self.cache.set(cache_key, product, ttl=3600)
        
        return product
    
    async def search_products(self, query: str, filters: Dict) -> List[Dict]:
        """
        Search products with filters using Elasticsearch.
        
        Requires: elasticsearch library (elasticsearch[async])
        Assumes: self.db is an Elasticsearch client instance
        
        Filters supported:
        - price_range: Dict with 'min' and/or 'max' keys
        - category: str or List[str] of category names
        - availability: bool (True for in stock, False for out of stock)
        - rating: float (minimum rating threshold)
        
        Example:
            filters = {
                'price_range': {'min': 10.0, 'max': 100.0},
                'category': ['Electronics', 'Books'],
                'availability': True,
                'rating': 4.0
            }
        """
        from elasticsearch import AsyncElasticsearch
        
        # Build Elasticsearch query
        must_clauses = []
        filter_clauses = []
        
        # Text search query (full-text search)
        if query:
            must_clauses.append({
                "multi_match": {
                    "query": query,
                    "fields": ["name^2", "description"],  # Boost name field
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            })
        else:
            # If no query, match all
            must_clauses.append({"match_all": {}})
        
        # Price range filter
        if 'price_range' in filters:
            price_range = filters['price_range']
            price_filter = {}
            if 'min' in price_range:
                price_filter['gte'] = price_range['min']
            if 'max' in price_range:
                price_filter['lte'] = price_range['max']
            if price_filter:
                filter_clauses.append({"range": {"price": price_filter}})
        
        # Category filter
        if 'category' in filters:
            category = filters['category']
            if isinstance(category, list):
                filter_clauses.append({"terms": {"category": category}})
            else:
                filter_clauses.append({"term": {"category": category}})
        
        # Availability filter
        if 'availability' in filters:
            availability = filters['availability']
            if availability:
                filter_clauses.append({"range": {"stock_quantity": {"gt": 0}}})
            else:
                filter_clauses.append({"term": {"stock_quantity": 0}})
        
        # Rating filter
        if 'rating' in filters:
            filter_clauses.append({
                "range": {
                    "rating": {
                        "gte": filters['rating']
                    }
                }
            })
        
        # Build Elasticsearch query body
        es_query = {
            "query": {
                "bool": {
                    "must": must_clauses,
                    "filter": filter_clauses
                }
            },
            "sort": [
                {"rating": {"order": "desc"}},
                {"name.keyword": {"order": "asc"}}
            ],
            "size": 100
        }
        
        # Execute search
        response = await self.db.search(
            index="products",
            body=es_query
        )
        
        # Extract results
        results = []
        for hit in response['hits']['hits']:
            product = hit['_source']
            product['id'] = hit['_id']  # Add document ID
            results.append(product)
        
        return results
    
    def apply_discount(self, price: float, discount_percent: float) -> float:
        """Apply discount to price."""
        return price * (1 - discount_percent / 100)

