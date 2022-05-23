from sqlalchemy import Column, Integer, String
from database import Base

# Define Address class inheriting from Base
class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    location_name = Column(String(256))
    longitude = Column(Integer())
    latitude = Column(Integer())