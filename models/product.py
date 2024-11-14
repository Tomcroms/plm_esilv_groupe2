from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    reference = Column(String, nullable=False, unique=True)
    description = Column(String)
    bom = relationship("BOM", back_populates="product")

class BOM(Base):
    __tablename__ = 'boms'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    details = Column(String)
    product = relationship("Product", back_populates="bom")
