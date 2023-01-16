from sqlalchemy import Integer, String
from sqlalchemy.sql.schema import Column
from .database import Base

class Item(Base):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)