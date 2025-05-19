from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud
from database import engine, get_db
from models import Agent
from routes import router
import security as security

# Create the database tables if they don't exist




app = FastAPI(title="DEMT API with Auth")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")

def format_date_fr(value):
    # Example: format YYYY-MM-DD to DD/MM/YYYY
    if not value:
        return ""
    return value.strftime("%d/%m/%Y")


templates.env.filters["format_date_fr"] = format_date_fr

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
    if exc.status_code == 401 :
        return RedirectResponse(url="/login")
    return await http_exception_handler(request, exc)




@app.get("/", response_class=RedirectResponse)
async def root(current_agent: Agent = Depends(security.get_current_agent)):
    return RedirectResponse(url=f"/{current_agent.role.lower()}")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



@app.get("/directeur", response_class=HTMLResponse)
async def login_page(request: Request):
    
    return RedirectResponse(url="/project")



@app.get("/project",response_class=HTMLResponse)
async def project_page(request: Request, db: Session = Depends(get_db), current_agent: Agent = Depends(security.get_current_agent)):
    projects= crud.ProjetCRUD.get_all(db)
    etats=[]
    for project in projects:
        etat = crud.HistoriqueEtatCRUD.get(db, project.id_projet)
        if etat:
            # Select the etat with the latest date_debut if etat is a list
            if isinstance(etat, list):
                etat = max(etat, key=lambda e: e.date_debut)
            etats.append(etat)
        else:
            etats.append(None)
    return templates.TemplateResponse("projet.html", {"request": request, "projects": projects,"etats": etats})


@app.get("/contrat", response_class=HTMLResponse)
async def contract_page(request: Request, db: Session = Depends(get_db), current_agent: Agent = Depends(security.get_current_agent)):
    contracts = crud.ContractCRUD.get_all(db)
    etats_dict = {}

    for contrat in contracts:
        etat = crud.HistoriqueEtatCRUD.get(db, contrat.id_projet)
        if etat:
            if isinstance(etat, list):
                latest_etat = max(etat, key=lambda e: e.date_debut)
                etats_dict[contrat.id_projet] = latest_etat
            else:
                etats_dict[contrat.id_projet] = etat

    return templates.TemplateResponse("contrat.html", {
        "request": request,
        "contracts": contracts,
        "etats_dict": etats_dict
    })



@app.get("/achat", response_class=HTMLResponse)
async def achat_page(
    request: Request,
    db: Session = Depends(get_db),
    current_agent: Agent = Depends(security.get_current_agent)
):
    achats = crud.AchatSurFactureCRUD.get_all(db)
    # Créer un dictionnaire pour stocker les états par projet
    etats_dict = {}
    
    for achat in achats:
        etat = crud.HistoriqueEtatCRUD.get(db, achat.projet_id_projet)
        if etat:
            if isinstance(etat, list):
                latest_etat = max(etat, key=lambda e: e.date_debut)
                etats_dict[achat.projet_id_projet] = latest_etat
            else:
                etats_dict[achat.projet_id_projet] = etat
    
    return templates.TemplateResponse("achat.html", {
        "request": request,
        "achats": achats,
        "etats_dict": etats_dict
    })


@app.get("/bondecommande/{id_projet}", response_class=HTMLResponse)
async def bondecommande_page(id_projet: int,
    request: Request,
    db: Session = Depends(get_db),
    current_agent: Agent = Depends(security.get_current_agent)
):
    contrat=crud.ContractCRUD.get_by_id_projet(db,id_projet)
    etat = crud.HistoriqueEtatCRUD.get(db, id_projet)
    contrat.etat=etat.etat.value
    bons = crud.BonDeCommandeCRUD.get_by_id_project(db, id_projet)
    return templates.TemplateResponse("bondecomande.html", {
        "request": request,
        "bons": bons,
        "contrat": contrat
    })
    
@app.get("/pv/{id}", response_class=HTMLResponse)
async def pv_page(id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_agent: Agent = Depends(security.get_current_agent)
):
    pvs = crud.PVDeReceptionCRUD.get_by_id_commande(db, id)

    for pv in pvs:
        factures = crud.FactureCRUD.get_by_id_pv(db, pv.id_bon)
        if factures and len(factures) > 0:
            facture = factures[0]
            pv.date_f = facture.date
            pv.montant = facture.montant
        else:
            pv.date_f = None
            pv.montant = None
    return templates.TemplateResponse("pv_de_reception.html", {
        "request": request,
        "pvs": pvs
    })