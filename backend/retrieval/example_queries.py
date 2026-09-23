example_queries = [
    {
        'question':'Show all customers.',
        'sql':"""
        Select * FROM customers;
        """
    },
    {
      'question':'Show the names and prices of all products.',
      'sql':"""
      SELECT product_name,price FROM products;
      """  
    },
    {
      'question':'Show all products that cost more than 1000.',
      'sql':"""
      SELECT product_name,price FROM products WHERE price>1000;
      """  
    },
    {
      'question':'Show all products in the Electronics category.',
      'sql':"""
      SELECT p.product_name,p.price FROM products p JOIN categories c ON p.category_id = c.category_id WHERE c.category_name = 'Electronics';
      """  
    },
    {
        "question": "How many products are in each category?",
        "sql": """
SELECT c.category_name, COUNT(p.product_id) AS product_count
FROM categories c
LEFT JOIN products p
    ON c.category_id = p.category_id
GROUP BY c.category_name;
"""
    },
    {
        "question": "Show all orders placed by each customer.",
        "sql": """
SELECT c.customer_name, o.order_id, o.order_date, o.total_amount, o.status
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
ORDER BY c.customer_name, o.order_date;
"""
    },
    {
        "question": "Show all orders that have been delivered.",
        "sql": """
SELECT *
FROM orders
WHERE status = 'Delivered';
"""
    },
    {
        "question": "What is the total number of orders for each customer?",
        "sql": """
SELECT c.customer_name, COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;
"""
    },
    {
        "question": "What is the total amount spent by each customer?",
        "sql": """
SELECT c.customer_name, SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spent DESC;
"""
    },
    {
        "question": "Which products have been ordered and how many units were sold?",
        "sql": """
SELECT p.product_name, SUM(oi.quantity) AS units_sold
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
ORDER BY units_sold DESC;
"""
    },
    {
        "question": "Show the products included in each order.",
        "sql": """
SELECT o.order_id, p.product_name, oi.quantity, oi.price
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
ORDER BY o.order_id;
"""
    },
    {
        "question": "Which customer placed the most expensive order?",
        "sql": """
SELECT c.customer_name, o.order_id, o.total_amount
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
ORDER BY o.total_amount DESC
LIMIT 1;
"""
    },
    {
        "question": "What is the average product price in each category?",
        "sql": """
SELECT c.category_name, AVG(p.price) AS average_price
FROM categories c
JOIN products p
    ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name;
"""
    },
    {
        "question": "How many orders are there for each order status?",
        "sql": """
SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status;
"""
    },
    {
        "question": "Show customers who have placed at least two orders.",
        "sql": """
SELECT c.customer_name, COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING COUNT(o.order_id) >= 2;
"""
    }
]