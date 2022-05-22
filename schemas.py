
  
from pydantic import BaseModel

# Create Address Schema (Pydantic Model)
class AddressCreate(BaseModel):
    location_name: str
    longitude: float
    latitude: float

# Complete Address Schema (Pydantic Model)
class Address(BaseModel):
    id: int
    location_name: str
    longitude: float
    latitude: float

    class Config:
        orm_mode = True
