schema_descriptions = {
    'customers':{
        'description':'Stores information about customers who place orders',
        'columns':{
            'customer_id':'Unique identifier for each customer.',
            'customer_name':'Full name of the customer.',
            'email':'Unique email of the customer.',
            'phone_no':'Phone number of the customer',
            'address':'Address where the customer is located'
        }
    },
    
    'categories':{
        'description':'Stores product categories used to organize products.',
        'columns':{
            'category_id':'Unique identifier for each product category.',
            'category_name':'Name of the product category.',
            'category_description':'Description explaining what types of products belong to the category.'
        }
    },
    
    'products':{
        'description':'Stores products that can be purchsed by the customers.',
        'columns':{
            'product_id':'Unique identifier for each product.',
            'product_name':'Name of the product.',
            'category_id':'Foreign key referencing the category that the product belongs to.',
            'price':'Price of the product.',
        }
    },
    
    "orders": {
        "description": "Stores orders placed by customers.",
        "columns": {
            "order_id": "Unique identifier for each order.",
            "customer_id": "Foreign key referencing the customer who placed the order.",
            "order_date": "Date and time when the order was placed.",
            "total_amount": "Total monetary value of the order.",
            "status": "Current status of the order, such as Processing, Shipped, or Delivered."
        }
    },

    "order_items": {
        "description": "Stores individual products included in each order.",
        "columns": {
            "order_item_id": "Unique identifier for each order item.",
            "order_id": "Foreign key referencing the order containing this item.",
            "product_id": "Foreign key referencing the product included in the order.",
            "quantity": "Number of units of the product ordered.",
            "price": "Price of the product at the time it was included in the order."
        }
    }
}