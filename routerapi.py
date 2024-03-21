from fastapi import APIRouter,Depends,HTTPException,FastAPI,status
from pydantic import Field
from typing_extensions import Annotated
from sqlalchemy.orm import Session,session
from routerAuth import get_db, get_current_user
from models import User, Region,State,LGA
from pathlib import Path
from functools import lru_cache
import redis.asyncio as redis
from fastapi.requests import Request
from fastapi_simple_rate_limiter import rate_limiter


app = APIRouter(prefix="/locale")



db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]





@lru_cache(maxsize=50)
@app.get("/region",status_code=status.HTTP_200_OK)
@rate_limiter(limit=50, seconds=300)
async def read_all_regions(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    all_regions = db.query(Region.name).all()
    return all_regions

@lru_cache(maxsize=50)
@app.get("/state",status_code=status.HTTP_200_OK)
@rate_limiter(limit=50, seconds=300)
async def read_all_State(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    all_states= db.query(State,Region).join(Region).all()
    data =[]
    for state, region in all_states:
        state_info = {
            "name": state.name,
            "state_capital": state.state_capital,
            "region_name": region.name
        }
        data.append(state_info)

    return data


@lru_cache(maxsize=50)
@app.get("/state{region_no}", status_code=status.HTTP_200_OK)
@rate_limiter(limit=50, seconds=300)
async def read_states_by_region(user:user_dependency,db:db_dependency,region: str):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    all_states_by_region = db.query(State,Region).filter(region == Region.name).all()
    data =[]
    for state, region in all_states_by_region:
        state_info = {
            "name": state.name,
            "state_capital": state.state_capital,
            "region_name": region.name
        }
        data.append(state_info)

    return data


@lru_cache(maxsize=50)
@app.get("/LGA{state_no}",status_code=status.HTTP_200_OK)
@rate_limiter(limit=50, seconds=300)
async def read_lgas_by_state(user:user_dependency,db:db_dependency,statename:str):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    all_lgas_by_state = db.query(LGA,State).join(State).filter(State.name == statename).all()
    data = []
    for lga in all_lgas_by_state:
        one_lga = lga.LGA.name
        data.append(one_lga)
    return data