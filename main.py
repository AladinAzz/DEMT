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
    if exc.status_code == 401:
        return RedirectResponse(url="/login", status_code=302)
    return await http_exception_handler(request, exc)

@app.get("/", response_class=RedirectResponse)
async def root(current_agent: Agent = Depends(security.get_current_agent)):
    return RedirectResponse(url=f"/{current_agent.role.value}", status_code=302)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/directeur", response_class=HTMLResponse)
async def login_page(request: Request):
    
    return RedirectResponse(url="/acceuil")



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
    return templates.TemplateResponse("projets.html", {"request": request, "projects": projects,"etats": etats, "agent": current_agent})

@app.get("/project/{id}",response_class=HTMLResponse)
async def project_page(id:int,request: Request, db: Session = Depends(get_db), current_agent: Agent = Depends(security.get_current_agent)):
    projet= crud.ProjetCRUD.get(db,id)
    contrats= crud.ContractCRUD.get_by_id_projet(db,id)
    achats=crud.AchatSurFactureCRUD.get_by_id_projet(db,id)
    etats=crud.HistoriqueEtatCRUD.get_all(db)
    for achat in achats:
        etats_f = crud.HistoriqueEtatCRUD.get_by_id_achat(db, id)
        if not isinstance(etats, list):
            etats_f = [etats] if etats else []
        etats_f.sort(key=lambda x: x.date_debut, reverse=False)
        achat.etat = etats_f[-1].etat if etats_f else None
    if not isinstance(etats, list):
        etats = [etats] if etats else []
    etats.sort(key=lambda x: x.date_debut, reverse=False)
    
    setats = []
    setat=crud.EtatCRUD.get_all(db)
    if isinstance(setat,list):
        setats.extend(setat)
    else:
        setats.append(setat)
    
        
    return templates.TemplateResponse("projet.html", {
        "request": request,
        "projet": projet,
        "achats":achats,
        "contracts": contrats,
        "etats": etats ,
        "setats": setats,
        "agent": current_agent
        })




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
        "etats_dict": etats_dict,
        "agent": current_agent
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
        "etats_dict": etats_dict,
        "agent": current_agent
    })


@app.get("/bondecommande/{id_contrat}", response_class=HTMLResponse)
async def bondecommande_page(
    id_contrat: int,
    request: Request,
    db: Session = Depends(get_db),
    current_agent: Agent = Depends(security.get_current_agent)
):
    contrats = crud.ContractCRUD.get_by_id_contrat(db, id_contrat)
    bons=[]
    bons.extend( crud.BonDeCommandeCRUD.get_by_id_contrat(db, id_contrat))
    # Si tu veux aussi les états pour chaque contrat :
    etats = []
    etat=crud.HistoriqueEtatCRUD.get_by_id_contrat(db, id_contrat)
    if isinstance(etat, list) and len(etat) > 0:
        etats.extend(etat)
        contrats.etat=etats[-1].etat
    else:
        if etat:
            etats.append(etat)
        else:
            contrats.etat=""
            
    
    return templates.TemplateResponse("bondecomande.html", {
        "request": request,
        "bons": bons,
        "etat": etats,
        "contrats": contrats,
        "agent": current_agent
    })
    
@app.get("/pv/{id}", response_class=HTMLResponse)
async def pv_page(id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_agent: Agent = Depends(security.get_current_agent)
):
    bons=[]
    bons.append(crud.BonDeCommandeCRUD.get(db, id))
    
    pvs = crud.PVDeReceptionCRUD.get_by_id_commande(db, id)

        
    return templates.TemplateResponse("pv_de_reception.html", {
        "request": request,
        "pvs": pvs,
        "agent": current_agent,
        "bons": bons
    })
@app.get("/table/{id}", response_class=HTMLResponse)
def table_page(id:int,
    request: Request,
    db: Session = Depends(get_db),
    current_agent: Agent = Depends(security.get_current_agent)
):
    chapitre = crud.ChapitreCRUD.get(db,id)
    if chapitre:
        
            projets = crud.ProjetCRUD.get_by_id_chapitre(db, chapitre.id_chapitre)
            chapitre.nb_projets = 0
            chapitre.nb_contrats = 0
            if projets and len(projets) > 0:
                chapitre.nb_projets = len(projets)
                contrats=[]
                for projet in projets:
                    contrats.extend(crud.ContractCRUD.get_by_id_projet(db, projet.id_projet))
                    if contrats and isinstance(contrats, list):
                        chapitre.nb_contrats = chapitre.nb_contrats+ len(contrats)
                    
                    etats=crud.HistoriqueEtatCRUD.get_all(db)
                    if isinstance(etats,list):
                        etats = [etat for etat in etats if etat.id_projet is not None]
                        etats.sort(key=lambda x: x.id_projet, reverse=True)
                        for etat in etats:
                            if etat.id_projet==projet.id_projet:
                                projet.etat=etat.etat
                                break
                    else:
                        projet.etat=etats.etat

            else:
                chapitre.nb_projets = 0
                chapitre.etat = None
    else:
        raise HTTPException(status_code=404, detail="Chapitre not found")
    return templates.TemplateResponse("table.html", {
        "request": request,
        "chapitre": chapitre,
        "agent": current_agent,
        "projets": projets,
        
        
    })
       
    
@app.get("/users",response_class=HTMLResponse)
def users_page(
    request: Request,
    db: Session = Depends(get_db),
    current_agent: Agent = Depends(security.get_current_agent)
):
    agents = crud.AgentCRUD.get_all(db)
    return templates.TemplateResponse("agent.html", {
        "request": request,
        "agents": agents,
        "agent": current_agent
    })
    
    


@app.get("/acceuil", response_class=HTMLResponse)
def acceuil_page(
    request: Request,
    db: Session = Depends(get_db),
    current_agent: Agent = Depends(security.get_current_agent)
):
    # Get all chapters
    chapters = crud.ChapitreCRUD.get_all(db)
    
    return templates.TemplateResponse("acceuil.html", {
        "request": request,
        "chapitres": chapters,
        "agent": current_agent
    })
    
@app.get("/bondecommandef/{id}", response_class=HTMLResponse)
async def bondecommande_achat_page(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_agent: Agent = Depends(security.get_current_agent)
):
    achat= crud.AchatSurFactureCRUD.get_by_id_facture(db, id)
    bons = crud.BonDeCommandeCRUD.get_by_id_achat(db, id)
    # Si tu veux aussi les états pour chaque contrat :
    etats = []
    etats.extend( crud.HistoriqueEtatCRUD.get_by_id_achat(db, id))
    if  len(etats) > 0:
        etat = max(etats, key=lambda e: e.date_debut)
    else:
        etat = None
        etats=None
    achat.etat = etat.etat if etat else None
    
    return templates.TemplateResponse("bondecommandef.html", {
        "request": request,
        "bons": bons,
        "achat": achat,
        "etats": etats,
        "agent": current_agent
    })
    
@app.get("/settings",response_class=HTMLResponse)
def settings_page (
    request: Request,
    db: Session = Depends(get_db),
    current_agent: Agent = Depends(security.get_current_agent)
):
    chapitres = []
    ch = crud.ChapitreCRUD.get_all(db)
    if isinstance(ch, list):
        chapitres.extend(ch)
    elif ch:
        chapitres.append(ch)

    directions = []
    dir_ = crud.DirectionCRUD.get_all(db)
    if isinstance(dir_, list):
        directions.extend(dir_)
    elif dir_:
        directions.append(dir_)

    bureaux = []
    bur = crud.BureauCRUD.get_all(db)
    if isinstance(bur, list):
        bureaux.extend(bur)
    elif bur:
        bureaux.append(bur)

    etats = []
    et = crud.EtatCRUD.get_all(db)
    if isinstance(et, list):
        etats.extend(et)
    elif et:
        etats.append(et)
    return templates.TemplateResponse("parametre.html", {
        "request": request,
        "agent": current_agent,
        "chapitres": chapitres,
        "directions": directions,
        "bureaux": bureaux,
        "etats": etats 
    })
    
    
@app.get("/fournisseur", response_class=HTMLResponse)
async def fournisseur_page(
    request: Request,
    db: Session = Depends(get_db),
    current_agent: Agent = Depends(security.get_current_agent)
):
    fournisseurs = []
    f = crud.FournisseurCRUD.get_all(db)
    
    if isinstance(f, list):
        fournisseurs.extend(f)
    elif f:
        fournisseurs.append(f)
    
    
    
    return templates.TemplateResponse("fournisseur.html", {
        "request": request,
        "fournisseurs": fournisseurs,
        "agent": current_agent
    })
    
    
    
    
    
    
    
    
    