from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Agent
from routes import router
import security as security

# Create the database tables if they don't exist
from models import Base
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DEMT API with Auth")


templates = Jinja2Templates(directory="static")


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

@app.exception_handler(HTTPException)
async def custom_unauthorized_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401 and request.url.path == "/":
        return RedirectResponse(url="/login")
    return await http_exception_handler(request, exc)


@app.get("/", response_class=RedirectResponse)
async def root(current_agent: Agent = Depends(security.get_current_agent)):
    return RedirectResponse(url=f"/{current_agent.role}")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



@app.get("/directeur", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})




