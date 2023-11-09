from fastapi import FastAPI ,Body,Depends
import schemas
import models
from database import Base,engine,SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

def get_session():
    session=SessionLocal()
    try:
        yield session
    finally:
        session.close()



app=FastAPI()

fakeDatabase={
    1:{'task':'Clean car'},
    2:{'task':'Write Blog'},
    3:{'task':'Start stream'}
}

@app.get("/")
def getItems(session:Session=Depends(get_session)):
    items=session.query(models.Item).all()
    return items

@app.get("/{id}")
def getItem(id:int,session:Session=Depends(get_session)):
    item=session.query(models.Item).get(id)
    return item


# Option 1 
# @app.post("/")
# def addItem(task:str):
#     newID=len(fakeDatabase.keys()) + 1
#     fakeDatabase[newID]={'task':task}
#     return fakeDatabase

#option 2 
@app.post("/")
def addItem(item:schemas.Item,session:Session=Depends(get_session)):
   item=models.Item(task=item.task)
   session.add(item)
   session.commit()
   session.refresh(item)
   
   return item

# # option 3
# @app.post("/")
# def addItem(body=Body()):
#     newID=len(fakeDatabase.keys()) + 1
#     fakeDatabase[newID]={'task':body['task']}
#     return fakeDatabase

@app.put("/{id}")
def updateItem(id:int,item:schemas.Item,session:Session=Depends(get_session)):
    itemObject=session.query(models.Item).get(id)
    itemObject.task=item.task
    session.commit()
    return itemObject


@app.delete("/{id}")
def deleteItem(id:int,session:Session=Depends(get_session)):
    itemObject=session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'item was deleted '




