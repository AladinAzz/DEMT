from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Agent
from routes import router
import security as security

# Create the database tables if they don't exist
from models import Base
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DEMT API with Auth")


@app.post("/token", response_model=security.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    agent = security.authenticate_agent(db, form_data.username, form_data.password)
    if not agent:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = security.create_access_token(data={"sub": agent.username})
    return {"access_token": access_token, "token_type": "bearer"}
# Protect all routes by default:
app.include_router(router, dependencies=[Depends(security.get_current_agent)])


@app.get("/")
async def root(current_agent: Agent = Depends(security.get_current_agent)):
    return {"message": f"Hello {current_agent.prenom} {current_agent.nom}, welcome to DEMT1 API!"}







