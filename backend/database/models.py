from sqlalchemy import Column,Integer,String,Float,ForeignKey,DateTime
from sqlalchemy.orm import declarative_base,relationship
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__='customers'
    
    customer_id = Column(Integer,primary_key=True)
    customer_name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    phone_no = Column(String)
    address = Column(String)
    
    orders = relationship("Order",back_populates="customer")
    
class Category(Base):
    __tablename__ = 'categories'
    
    category_id = Column(Integer,primary_key=True)
    category_name = Column(String,nullable=False,unique=True)
    category_description = Column(String)
    
    products = relationship("Product",back_populates="category")
    
class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(Integer,primary_key=True)
    product_name = Column(String,nullable=False)
    category_id = Column(Integer,ForeignKey('categories.category_id'),nullable=False)
    price = Column(Float,nullable = False)
    
    order_items = relationship("OrderItem",back_populates="product")
    category = relationship("Category",back_populates='products')
    
class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)

    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    

class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    
