from fastapi import FastAPI,Depends,HTTPException
from models import Region, State, LGA
from routerAuth import get_db
from sqlalchemy.orm import session
from database import engine

app = FastAPI()

# input all lgas,states and regions
@app.post("/region")
async def input_info(regionname:str, db: session = Depends(get_db)):
    region_model = Region(name = regionname)

    db.add(region_model)
    db.commit()
    

@app.post("/states")
async def input_info(state_name:str,statecapital:str,regionid:int,id_state:int, db: session = Depends(get_db)):
    state_model = State(
        id = id_state,
        name = state_name,
        state_capital = statecapital,
        region_id = regionid)
    
    db.add(state_model)
    db.commit()


@app.delete("/states{state_name}")
async def edit_info(state_name:str,db: session = Depends(get_db)):
    state_model = db.query(State).filter(state_name == State.name).first()
    if state_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(state_model)
    db.commit()

@app.post("/lgas")
async def input_info(lga_name:str,stateid:int, db: session = Depends(get_db)):
    lga_model = LGA(
        name = lga_name,
        state_id = stateid)
    
    db.add(lga_model)
    db.commit()   
    return lga_model.name


@app.put("/lgas{lga_name}")
async def input_info(lga_name:str,stateid:int, db: session = Depends(get_db)):
    lga_model = LGA(
        name = lga_name,
        state_id = stateid)
    
    db.add(lga_model)
    db.commit()   
    return lga_model.name

@app.delete("/lga{lga_name}")
async def del_info(lga_name:str,db: session = Depends(get_db)):
    lga_model = db.query(LGA).filter(lga_name == LGA.name).first()
    if lga_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(lga_model)
    db.commit()