from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Address(Base):  # 1
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, index=True)  # 2
    location = Column(String(256), nullable=False)
    latitude = Column(Integer(), nullable=False)
    longitude = Column(Integer(), nullable=False)
