from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session

from app import models,schemas,crud
from app.database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

app=FastAPI()
def get_db():
    db=SessionLocal()
#What is SessionLocal?
# When you see SessionLocal = sessionmaker(...), you have created a Class Factory.

# The Analogy: If engine is the physical phone line connected to the database server, SessionLocal is the Phone. Every time you call SessionLocal(), you are picking up the phone to start a new call.

# Why the "Local" name? It’s a convention. It signifies that each request to your API gets its own "local" session that doesn't interfere with other users' requests.
    try:
        yield db
    finally:
        db.close()
        
@app.get("/")
def home():
    return {"message":"FastAPI Crud App running"}


@app.post("/users",response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,

    db:Session=Depends(get_db)
    #Depends(get_db) calls a helper function (usually a generator) that yields a database session for this specific request and automatically closes it once the request is finished.
):
    return crud.create_user(db, user)


@app.get("/users",response_model=list[schemas.UserResponse])
def get_users(
    db:Session=Depends(get_db)
):
    return crud.get_users(db)
@app.get("/users/{user_id}",response_model=schemas.UserResponse)
def get_user(user_id:int,db:Session=Depends(get_db)):
    user = crud.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404,
                            detail="user not found")
    return user
@app.put("/users/{user_id}",response_model=schemas.UserResponse)
def update_user(
    user_id:int,
    updated_user:schemas.UserCreate,
    db:Session=Depends(get_db)):
    user=crud.update_user(db,user_id,updated_user)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="user not found"
            
        )
    return user
@app.delete("/users/{user_id}")
def delete_user(
    user_id:int,
    db:Session=Depends(get_db)
):
    user=crud.delete_user(db,user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="user not found"
            
        )
    return {"message":"user deleted successfully"}
    
    
    
