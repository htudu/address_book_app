from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine
from sqlalchemy.orm import Session
import models
import schemas
from utilities import distance_check, get_session

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()



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

    # get the address with the given id
    address = session.query(models.Address).get(id)

    # check if address with given id exists. If not, raise exception and return 404 not found response
    if not address:
        raise HTTPException(status_code=404, detail=f"address with id {id} not found")

    return address

@app.put("/address/{id}", response_model=schemas.Address)
def update_address(id: int, location_name: str, session: Session = Depends(get_session)):

    # get the address with the given id
    rec = session.query(models.Address).get(id)

    # update address with the given address id 
    if rec:
        rec.location_name = location_name
        session.commit()

    # check if address with given id exists. If not, raise exception and return 404 not found response
    if not rec:
        raise HTTPException(status_code=404, detail=f"address with id {id} not found")

    return rec

@app.delete("/address/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(id: int, session: Session = Depends(get_session)):

    # get the address with the given id
    rec = session.query(models.Address).get(id)

    # if address with given id exists, delete it from the database. Otherwise raise 404 error
    if rec:
        session.delete(rec)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"address with id {id} not found")

    return None




@app.get("/get_address_within", response_model = List[schemas.Address])
def read_address_list(distance: int, latitude: float, longitude: float, session: Session = Depends(get_session)):

    # get all address within a given distance
    address_list = session.query(models.Address).all()

    filtered_address_list = []
    for addr in address_list:
        status = distance_check(latitude, longitude, addr.latitude, addr.longitude, distance)
        print(status)
        if status:
            filtered_address_list.append(addr)
 
    return filtered_address_list

