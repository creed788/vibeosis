from sqlalchemy import Column, Integer, String, Enum, Text, TIMESTAMP, func
from database import Base, engine

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category = Column(Enum("finished", "semi-finished", "raw"), nullable=False)
    description = Column(String(250))
    product_image = Column(Text)
    sku = Column(String(100), unique=True, nullable=False)
    unit_of_measure = Column(Enum("mtr", "mm", "ltr", "ml", "cm", "mg", "gm", "unit", "pack"), nullable=False)
    lead_time = Column(Integer)
    created_date = Column(TIMESTAMP, server_default=func.now())
    updated_date = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


