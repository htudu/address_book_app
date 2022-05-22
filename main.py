from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
from utilities import distance_check

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
def root():
    return "Address Book App is working"

@app.post("/address", response_model=schemas.Address, status_code=status.HTTP_201_CREATED)
def create_address(address: schemas.AddressCreate, session: Session = Depends(get_session)):

    # create an instance of the Address database model
    rec = models.Address(location_name = address.location_name,
                            longitude = address.longitude,
                            latitude = address.latitude)

    # add it to the session and commit it
    session.add(rec)
    session.commit()
    session.refresh(rec)

    # return the Address object
    return rec

@app.get("/address/{id}", response_model=schemas.Address)
def read_address(id: int, session: Session = Depends(get_session)):

    # get the todo item with the given id
    todo = session.query(models.Address).get(id)

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo

@app.put("/address/{id}", response_model=schemas.Address)
def update_todo(id: int, location_name: str, session: Session = Depends(get_session)):

    # get the todo item with the given id
    rec = session.query(models.Address).get(id)

    # update todo item with the given task (if an item with the given id was found)
    if rec:
        rec.location_name = location_name
        session.commit()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not rec:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return rec

@app.delete("/address/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, session: Session = Depends(get_session)):

    # get the todo item with the given id
    rec = session.query(models.Address).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if rec:
        session.delete(rec)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return None




@app.get("/addresses", response_model = List[schemas.Address])
def read_todo_list(distance: int, latitude: float, longitude: float, session: Session = Depends(get_session)):

    # get all todo items
    address_list = session.query(models.Address).all()

    filtered_address_list = []
    for addr in address_list:
        status = distance_check(latitude, longitude, addr.latitude, addr.longitude, distance)
        print(status)
        if status:
            filtered_address_list.append(addr)
 
    return filtered_address_list








# from fastapi import Request, FastAPI

# from models.address import Address

# from database import SessionLocal

# session = SessionLocal()

# app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# # @app.post("/items")
# # async def create_address(request: Request):

# #     location_rec = session.query(Address).order_by(Address.id).desc().first()
# #     if location_rec:
# #         location_id = location_rec.id
# #     else:
# #         location_id = 1
# #     payload = request.json()
# #     payload["id"] = location_id

# #     #--- insert record ---
# #     # try:
# #     rec = Address(**payload)
# #     session.add(rec)
# #     session.commit()

# #     return await {"message": "address added successful", "code": 200}

# @app.put("/items")
# async def update_address(request: Request):
    
#     return await request.json()


# @app.post("/items")
# async def create_address(address: Address):
#     address_dict = address.dict()
#     print(address_dict)
#     db_query = """INSERT INTO Article (title, slug, content, author) 
#                 VALUES (:title, :slug, :content, :author)"""

#     # .. which you can then expand automagically
#     cursor.execute(db_query, **article_obj.dict())