from fastapi import FastAPI, Depends,HTTPException
from routerAuth import auth as authenticate
import models
from routerapi import app as results
from database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def HOME():

    return "WELCOME TO LOCALE"


   

app.include_router(authenticate)
app.include_router(results)




