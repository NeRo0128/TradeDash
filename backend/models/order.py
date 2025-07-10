from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base

# Tabla de relación entre pedidos y productos
order_products = Table(
    'order_products',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('quantity', Integer),
    Column('price_at_time', Float)
)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float)
    status = Column(String)  # pending, completed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relaciones
    user = relationship("User")
    products = relationship("Product", secondary=order_products)