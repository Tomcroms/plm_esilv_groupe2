from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class BOM(Base):
    __tablename__ = 'boms'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    details = Column(String)
    product = relationship("Product", back_populates="bom")
