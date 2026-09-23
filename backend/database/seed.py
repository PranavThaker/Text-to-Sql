from models import Customer,Category,Product,Order,OrderItem
from connection import get_session
from datetime import datetime

def seed_data():
    session = get_session()
    
    try:
        customers = [
            Customer(
                customer_name="Rahul Sharma",
                email="rahul@example.com",
                phone_no="9876543210",
                address="Ahmedabad, Gujarat"
            ),
            Customer(
                customer_name="Priya Patel",
                email="priya@example.com",
                phone_no="9876543211",
                address="Surat, Gujarat"
            ),
            Customer(
                customer_name="Amit Shah",
                email="amit@example.com",
                phone_no="9876543212",
                address="Vadodara, Gujarat"
            ),
            Customer(
                customer_name="Neha Mehta",
                email="neha@example.com",
                phone_no="9876543213",
                address="Mumbai, Maharashtra"
            ),
            Customer(   
                customer_name="Arjun Desai",
                email="arjun@example.com",
                phone_no="9876543214",
                address="Pune, Maharashtra"
            ),
        ]

        session.add_all(customers)
        session.flush()

        # -------------------------
        # 2. Categories
        # -------------------------
        categories = [
            Category(
                category_name="Electronics",
                category_description="Electronic devices and accessories"
            ),
            Category(
                category_name="Books",
                category_description="Books and educational material"
            ),
            Category(
                category_name="Home Appliances",
                category_description="Appliances for home use"
            ),
            Category(
                category_name="Stationery",
                category_description="Office and school stationery"
            ),
        ]

        session.add_all(categories)
        session.flush()

        # -------------------------
        # 3. Products
        # -------------------------
        products = [
            Product(
                product_name="Wireless Mouse",
                category=categories[0],
                price=799
            ),
            Product(
                product_name="Mechanical Keyboard",
                category=categories[0],
                price=2499
            ),
            Product(
                product_name="USB-C Hub",
                category=categories[0],
                price=1299
            ),
            Product(
                product_name="Python Programming Book",
                category=categories[1],
                price=899
            ),
            Product(
                product_name="Database Design Book",
                category=categories[1],
                price=1099
            ),
            Product(
                product_name="Electric Kettle",
                category=categories[2],
                price=1499
            ),
            Product(
                product_name="Desk Lamp",
                category=categories[2],
                price=999
            ),
            Product(
                product_name="Notebook",
                category=categories[3],
                price=199
            ),
            Product(
                product_name="Ball Pen Pack",
                category=categories[3],
                price=149
            ),
        ]

        session.add_all(products)
        session.flush()

        # -------------------------
        # 4. Orders
        # -------------------------
        orders = [
            Order(
                customer=customers[0],
                order_date=datetime(2026, 9, 1),
                total_amount=3298,
                status="Delivered"
            ),
            Order(
                customer=customers[0],
                order_date=datetime(2026, 9, 5),
                total_amount=899,
                status="Delivered"
            ),
            Order(
                customer=customers[1],
                order_date=datetime(2026, 9, 7),
                total_amount=2598,
                status="Shipped"
            ),
            Order(
                customer=customers[2],
                order_date=datetime(2026, 9, 10),
                total_amount=1499,
                status="Processing"
            ),
            Order(
                customer=customers[3],
                order_date=datetime(2026, 9, 12),
                total_amount=1197,
                status="Delivered"
            ),
            Order(
                customer=customers[4],
                order_date=datetime(2026, 9, 15),
                total_amount=2898,
                status="Shipped"
            ),
        ]

        session.add_all(orders)
        session.flush()

        # -------------------------
        # 5. Order Items
        # -------------------------
        order_items = [
            OrderItem(
                order=orders[0],
                product=products[0],
                quantity=1,
                price=799
            ),
            OrderItem(
                order=orders[0],
                product=products[1],
                quantity=1,
                price=2499
            ),

            OrderItem(
                order=orders[1],
                product=products[3],
                quantity=1,
                price=899
            ),

            OrderItem(
                order=orders[2],
                product=products[2],
                quantity=1,
                price=1299
            ),
            OrderItem(
                order=orders[2],
                product=products[7],
                quantity=5,
                price=199
            ),

            OrderItem(
                order=orders[3],
                product=products[5],
                quantity=1,
                price=1499
            ),

            OrderItem(
                order=orders[4],
                product=products[6],
                quantity=1,
                price=999
            ),
            OrderItem(
                order=orders[4],
                product=products[8],
                quantity=2,
                price=149
            ),

            OrderItem(
                order=orders[5],
                product=products[1],
                quantity=1,
                price=2499
            ),
            OrderItem(
                order=orders[5],
                product=products[7],
                quantity=2,
                price=199
            ),
        ]

        session.add_all(order_items)

        session.commit()

        print("Seed data inserted successfully.")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    seed_data()