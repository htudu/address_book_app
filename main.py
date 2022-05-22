from fastapi import Request, FastAPI

from typing import Union
from pydantic import BaseModel

from models.address import Address

from database import SessionLocal

session = SessionLocal()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items")
async def create_address(request: Request):
    
    location_rec = session.query(Address).order_by(Address.id).desc().first()
    if location_rec:
        location_id = location_rec.id
    else:
        location_id = 1
    payload = request.json()
    payload["id"] = location_id

    #--- insert record ---
    # try:
    rec = Address(**payload)
    session.add(rec)
    session.commit()

    return await {"message": "address added successful", "code": 200}

@app.put("/items")
async def update_address(request: Request):
    return await request.json()
