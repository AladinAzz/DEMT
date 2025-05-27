from fastapi import APIRouter, Depends, HTTPException, status
from datetime import date
from sqlalchemy.orm import Session
from typing import List
import security
import crud, models, schemas
from database import get_db

router = APIRouter()

# Helper to raise 404 if not found
def get_or_404(obj, model_name: str):
    if obj is None:
        raise HTTPException(status_code=404, detail=f"{model_name} not found")
    return obj

# ----- Agent -----
@router.get("/agents", response_model=List[schemas.AgentRead])
def list_agents(db: Session = Depends(get_db)):
    return crud.AgentCRUD.get_all(db)

@router.get("/agents/{agent_id}", response_model=schemas.AgentRead)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = crud.AgentCRUD.get(db, agent_id)
    return get_or_404(agent, "Agent")

@router.post("/agents", response_model=schemas.AgentRead, status_code=status.HTTP_201_CREATED)
def create_agent(agent: schemas.AgentCreate, db: Session = Depends(get_db)):
    
    
    return crud.AgentCRUD.create(db, agent.__dict__)

@router.put("/agents/{agent_id}", response_model=schemas.AgentRead)
def update_agent(agent_id: int, agent: schemas.AgentRead, db: Session = Depends(get_db)):
    
    
    if agent.password == None:
        agent_to_update = crud.AgentCRUD.get(db, agent_id)
        agent.password = agent_to_update.password  # Keep the existing password if not provided
    
    updated = crud.AgentCRUD.update(db, agent_id, agent.__dict__)
    return get_or_404(updated, "Agent")

@router.delete("/agents/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    success = crud.AgentCRUD.delete(db, agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return

# ----- Bureau -----
@router.get("/bureaux", response_model=List[schemas.BureauRead])
def list_bureaux(db: Session = Depends(get_db)):
    return crud.BureauCRUD.get_all(db)

@router.get("/bureaux/{bureau_id}", response_model=schemas.BureauRead)
def get_bureau(bureau_id: int, db: Session = Depends(get_db)):
    bureau = crud.BureauCRUD.get(db, bureau_id)
    return get_or_404(bureau, "Bureau")

@router.post("/bureaux", response_model=schemas.BureauRead, status_code=status.HTTP_201_CREATED)
def create_bureau(bureau: schemas.BureauCreate, db: Session = Depends(get_db)):
    return crud.BureauCRUD.create(db, bureau.__dict__)

@router.put("/bureaux/{bureau_id}", response_model=schemas.BureauRead)
def update_bureau(bureau_id: int, bureau: schemas.BureauCreate, db: Session = Depends(get_db)):
    updated = crud.BureauCRUD.update(db, bureau_id, bureau.__dict__)
    return get_or_404(updated, "Bureau")

@router.delete("/bureaux/{bureau_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bureau(bureau_id: int, db: Session = Depends(get_db)):
    success = crud.BureauCRUD.delete(db, bureau_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bureau not found")
    return

# ----- Direction -----
@router.get("/directions", response_model=List[schemas.DirectionRead])
def list_directions(db: Session = Depends(get_db)):
    return crud.DirectionCRUD.get_all(db)

@router.get("/directions/{direction_id}", response_model=schemas.DirectionRead)
def get_direction(direction_id: int, db: Session = Depends(get_db)):
    direction = crud.DirectionCRUD.get(db, direction_id)
    return get_or_404(direction, "Direction")

@router.post("/directions", response_model=schemas.DirectionRead, status_code=status.HTTP_201_CREATED)
def create_direction(direction: schemas.DirectionCreate, db: Session = Depends(get_db)):
    return crud.DirectionCRUD.create(db, direction.__dict__)

@router.put("/directions/{direction_id}", response_model=schemas.DirectionRead)
def update_direction(direction_id: int, direction: schemas.DirectionCreate, db: Session = Depends(get_db)):
    updated = crud.DirectionCRUD.update(db, direction_id, direction.__dict__)
    return get_or_404(updated, "Direction")

@router.delete("/directions/{direction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_direction(direction_id: int, db: Session = Depends(get_db)):
    success = crud.DirectionCRUD.delete(db, direction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Direction not found")
    return

# ----- Chapitre -----
@router.get("/chapitres", response_model=List[schemas.ChapitreRead])
def list_chapitres(db: Session = Depends(get_db)):
    return crud.ChapitreCRUD.get_all(db)

@router.get("/chapitres/{chapitre_id}", response_model=schemas.ChapitreRead)
def get_chapitre(chapitre_id: int, db: Session = Depends(get_db)):
    chapitre = crud.ChapitreCRUD.get(db, chapitre_id)
    return get_or_404(chapitre, "Chapitre")

@router.post("/chapitres", response_model=schemas.ChapitreCreate, status_code=status.HTTP_201_CREATED)
def create_chapitre(chapitre: schemas.ChapitreCreate, db: Session = Depends(get_db)):
    return crud.ChapitreCRUD.create(db, chapitre.__dict__)

@router.put("/chapitres/{chapitre_id}", response_model=schemas.ChapitreRead)
def update_chapitre(chapitre_id: int, chapitre: schemas.ChapitreCreate, db: Session = Depends(get_db)):
    updated = crud.ChapitreCRUD.update(db, chapitre_id, chapitre.__dict__)
    return get_or_404(updated, "Chapitre")

@router.delete("/chapitres/{chapitre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chapitre(chapitre_id: int, db: Session = Depends(get_db)):
    success = crud.ChapitreCRUD.delete(db, chapitre_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chapitre not found")
    return

# ----- Projet -----
@router.get("/projets", response_model=List[schemas.ProjetRead])
def list_projets(db: Session = Depends(get_db)):
    projects= crud.ProjetCRUD.get_all(db)
    return projects

@router.get("/projets/{projet_id}", response_model=schemas.ProjetRead)
def get_projet(projet_id: int, db: Session = Depends(get_db)):
    projet = crud.ProjetCRUD.get(db, projet_id)
    return get_or_404(projet, "Projet")

@router.post("/projets", response_model=schemas.ProjetRead, status_code=status.HTTP_201_CREATED)
def create_projet(
    projet: dict,
    db: Session = Depends(get_db),
    current_user: models.Agent = Depends(security.get_current_agent)
):
    # Prepare project data
    projet_data = {
        "nom_projet": projet["nom_projet"],
        "description": projet.get("description"),
        "date_debut": projet["date_debut"],
        "id_bureau": projet["id_bureau"],
        "montant": projet["montant"],
        "chapitre_id_chapitre": projet["chapitre_id_chapitre"],
        "type": projet["type"],
        
    }
    # Create project
    created_projet = crud.ProjetCRUD.create(db, projet_data)

    # Create state history if etat is provided
    if projet.get("etat") is not None:
        description_etat = projet.get("description_etat", "")
        date_etat = projet.get("date_etat", projet.get("date_debut", date.today()))
        try:
            crud.HistoriqueEtatCRUD.create(
                db,
                {
                    "etat": projet["etat"],
                    "description": description_etat,
                    "id_projet": created_projet.id_projet,
                    "date_debut": date_etat,
                    "agent_id_agent": current_user.id_agent,
                },
            )
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error creating history: {str(e)}")
            raise HTTPException(500, f"History creation failed: {str(e)}")

    return get_or_404(created_projet, "Projet")

@router.put("/projets/{projet_id}", response_model=schemas.ProjetRead)
def update_projet(
    projet_id: int, 
    projet: dict,
    db: Session = Depends(get_db),
    current_user: models.Agent = Depends(security.get_current_agent)
):
    # Get the projet to update
    projet_to_update = crud.ProjetCRUD.get(db, projet_id)
    
    # Update fields
    projet_to_update.chapitre_id_chapitre = projet["chapitre_id_chapitre"]
    projet_to_update.nom_projet = projet["nom_projet"]
    projet_to_update.date_debut = projet["date_debut"]
    projet_to_update.montant = projet["montant"]
    projet_to_update.description = projet["description"]
    projet_to_update.type = projet["type"]
    
    # Check state history
    hist = crud.HistoriqueEtatCRUD.get(db, projet_id)
    if isinstance(hist, list):
        if len(hist) > 0:
            hist.sort(key=lambda x: x.date_debut, reverse=True)
            last_etat = hist[-1].etat
            if last_etat != projet["etat"]:
                description_etat = projet.get("description_etat", "")
                date_etat = projet.get("date_etat", date.today())
                try:
                    create_historique = crud.HistoriqueEtatCRUD.create(
                        db,
                        {
                            "etat": projet["etat"],
                            "description": description_etat,
                            "id_projet": projet_id,
                            "date_debut": date_etat,
                            "agent_id_agent": current_user.id_agent
                        }
                    )
                    db.commit()
                except Exception as e:
                    db.rollback()
                    print(f"Error creating history: {str(e)}")
                    raise HTTPException(500, f"History creation failed: {str(e)}")
        else:
            # Case: hist is an empty list (no history at all)
            description_etat = projet.get("description_etat", "")
            date_etat = projet.get("date_etat", date.today())
            try:
                create_historique = crud.HistoriqueEtatCRUD.create(
                    db,
                    {
                        "etat": projet["etat"],
                        "description": description_etat,
                        "id_projet": projet_id,
                        "date_debut": date_etat,
                        "agent_id_agent": current_user.id_agent
                    }
                )
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Error creating history: {str(e)}")
                raise HTTPException(500, f"History creation failed: {str(e)}")
    else:
        # Case: hist is None or a single object
        if hist is None or getattr(hist, "etat", None) != projet["etat"]:
            description_etat = projet.get("description_etat", "")
            date_etat = projet.get("date_etat", date.today())
            try:
                create_historique = crud.HistoriqueEtatCRUD.create(
                    db,
                    {
                        "etat": projet["etat"],
                        "description": description_etat,
                        "id_projet": projet_id,
                        "date_debut": date_etat,
                        "agent_id_agent": current_user.id_agent
                    }
                )
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Error creating history: {str(e)}")
                raise HTTPException(500, f"History creation failed: {str(e)}")
    
    updated = crud.ProjetCRUD.update(db, projet_id, projet_to_update.__dict__)
    
    return get_or_404(updated, "Projet")

@router.delete("/projets/{projet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_projet(projet_id: int, db: Session = Depends(get_db)):
    # Delete all contracts referencing this project
    contracts = db.query(models.Contract).filter(
        (models.Contract.projet_id_projet == projet_id) | 
        (models.Contract.id_projet == projet_id)
    ).all()
    for contract in contracts:
        db.delete(contract)
    db.commit()
    # Now delete the project
    success = crud.ProjetCRUD.delete(db, projet_id)
    if not success:
        raise HTTPException(status_code=404, detail="Projet not found")
    return

# ----- AchatSurFacture -----
@router.get("/achats_sur_facture", response_model=List[schemas.AchatSurFactureRead])
def list_achats(db: Session = Depends(get_db)):
    return crud.AchatSurFactureCRUD.get_all(db)

@router.get("/achats_sur_facture/{id_facture}", response_model=schemas.AchatSurFactureRead)
def get_achat(id_facture: str, db: Session = Depends(get_db)):
    achat = crud.AchatSurFactureCRUD.get_by_id_facture(db, id_facture)
    return get_or_404(achat, "AchatSurFacture")

@router.post("/achats_sur_facture", response_model=schemas.AchatSurFactureRead, status_code=status.HTTP_201_CREATED)
def create_achat(
    achat: dict,
    db: Session = Depends(get_db),
    current_user: models.Agent = Depends(security.get_current_agent)
):
    # Prepare achat data
    achat_data = {
        "id_facture": achat["id_facture"],
        "montant": achat["montant"],
        "description": achat["description"],
        "date": achat["date"],
        "projet_id_projet": achat["projet_id_projet"],
        "id_fournisseur": achat["id_fournisseur"],
        "devise": achat["devise"],
        "engagement": achat["engagement"],
    }
    # Create achat
    created_achat = crud.AchatSurFactureCRUD.create(db, achat_data)

    # Create state history if etat is provided
    if achat.get("etat") is not None:
        description_etat = achat.get("description_etat", "")
        date_etat = achat.get("dateetat", achat.get("date"))
        try:
            crud.HistoriqueEtatCRUD.create(
                db,
                {
                    "etat": achat["etat"],
                    "description": description_etat,
                    "id_facture": achat["id_facture"],
                    "date_debut": date_etat,
                    "agent_id_agent": current_user.id_agent,
                },
            )
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error creating history: {str(e)}")
            raise HTTPException(500, f"History creation failed: {str(e)}")

    return get_or_404(created_achat, "AchatSurFacture")


@router.put("/achats_sur_facture/{id_facture}", response_model=schemas.AchatSurFactureRead)
def update_achat(
    id_facture: str,
    achat: dict,
    db: Session = Depends(get_db),
    current_user: models.Agent = Depends(security.get_current_agent)
):
    # Get the achat to update
    achat_to_update = crud.AchatSurFactureCRUD.get_by_id_facture(db, id_facture)
    
    # Update fields
    achat_to_update.montant = achat["montant"]
    achat_to_update.description = achat["description"]
    achat_to_update.date = achat["date"]
    achat_to_update.projet_id_projet = achat["projet_id_projet"]
    achat_to_update.id_fournisseur = achat["id_fournisseur"]
    achat_to_update.devise = achat["devise"]
    achat_to_update.engagement = achat["engagement"]
    
    # Check state history
    hist = crud.HistoriqueEtatCRUD.get_by_id_achat(db, id_facture)
    if isinstance(hist, list):
        if len(hist) > 0:
            hist.sort(key=lambda x: x.date_debut, reverse=True)
            last_etat = hist[-1].etat
            if last_etat != achat["etat"]:
                description_etat = achat.get("description_etat", "")
                date_etat = achat.get("dateetat", achat["date"])
                try:
                    create_historique = crud.HistoriqueEtatCRUD.create(
                        db,
                        {
                            "etat": achat["etat"],
                            "description": description_etat,
                            "id_facture": id_facture,
                            "date_debut": date_etat,
                            "agent_id_agent": current_user.id_agent
                        }
                    )
                    db.commit()
                except Exception as e:
                    db.rollback()
                    print(f"Error creating history: {str(e)}")
                    raise HTTPException(500, f"History creation failed: {str(e)}")
        else:
            # Case: hist is an empty list (no history at all)
            description_etat = achat.get("description_etat", "")
            date_etat = achat.get("dateetat", achat["date"])
            try:
                create_historique = crud.HistoriqueEtatCRUD.create(
                    db,
                    {
                        "etat": achat["etat"],
                        "description": description_etat,
                        "id_facture": id_facture,
                        "date_debut": date_etat,
                        "agent_id_agent": current_user.id_agent
                    }
                )
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Error creating history: {str(e)}")
                raise HTTPException(500, f"History creation failed: {str(e)}")
    else:
        # Case: hist is None or a single object
        if hist is None or getattr(hist, "etat", None) != achat["etat"]:
            description_etat = achat.get("description_etat", "")
            date_etat = achat.get("dateetat", achat["date"])
            try:
                create_historique = crud.HistoriqueEtatCRUD.create(
                    db,
                    {
                        "etat": achat["etat"],
                        "description": description_etat,
                        "id_facture": id_facture,
                        "date_debut": date_etat,
                        "agent_id_agent": current_user.id_agent
                    }
                )
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Error creating history: {str(e)}")
                raise HTTPException(500, f"History creation failed: {str(e)}")
    
    updated = crud.AchatSurFactureCRUD.update(
        db, 
        (id_facture, achat["projet_id_projet"], achat["id_fournisseur"]), 
        achat_to_update.__dict__
    )
    return get_or_404(updated, "AchatSurFacture")



@router.delete("/achats_sur_facture/{id_facture}", status_code=status.HTTP_204_NO_CONTENT)
def delete_achat(id_facture: str, db: Session = Depends(get_db)):
    success = crud.AchatSurFactureCRUD.delete(db, id_facture)
    if not success:
        raise HTTPException(status_code=404, detail="AchatSurFacture not found")
    return

# ----- Contract -----
@router.get("/contracts", response_model=List[schemas.ContractRead])
def list_contracts(db: Session = Depends(get_db)):
    return crud.ContractCRUD.get_all(db)

@router.get("/contracts/{id_contrat}", response_model=schemas.ContractRead)
def get_contract(id_contrat: str, db: Session = Depends(get_db)):
    contract = crud.ContractCRUD.get(db, id_contrat)
    return get_or_404(contract, "Contract")

@router.post("/contracts", response_model=schemas.ContractRead, status_code=status.HTTP_201_CREATED)
def create_contract(
    contract: dict,
    db: Session = Depends(get_db),
    current_agent: models.Agent = Depends(security.get_current_agent)
):
    # Prepare contract data
    contract_data = {
        "id_contrat":contract["id_contrat"],
        "id_projet": contract["id_projet"],
        "projet_id_projet": contract.get("id_projet"),  # <-- add this line
        "id_fournisseur": contract["id_fournisseur"],
        "description": contract["description"],
        "date_debut": contract["date_debut"],
        "date_de_notification": contract.get("date_de_notification"),
        "min": contract["min"],
        "max": contract.get("max"),
        "duree": contract["duree"],
        "etat": contract.get("etat"),
        "devise": contract["devise"],
        "type": contract["type"],
        "engagement": contract.get("engagement", 0),
        "projet_chapitre_id_chapitre": contract.get("projet_chapitre_id_chapitre"),
    }

    # Create contract
    created_contract = crud.ContractCRUD.create(db, contract_data)

    # Create state history if etat is provided
    if contract.get("etat") is not None:
        description_etat = contract.get("description_etat", "")
        date_etat = contract.get("date_etat", contract.get("date_debut", date.today()))
        try:
            crud.HistoriqueEtatCRUD.create(
                db,
                {
                    "etat": contract["etat"],
                    "description": description_etat,
                    "id_contrat": created_contract.id_contrat,
                    "date_debut": date_etat,
                    "agent_id_agent": current_agent.id_agent,
                },
            )
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error creating history: {str(e)}")
            raise HTTPException(500, f"History creation failed: {str(e)}")

    return get_or_404(created_contract, "Contract")

@router.put("/contracts/{id_contrat}", response_model=schemas.ContractRead)
def update_contract(id_contrat: str, contract: dict, db: Session = Depends(get_db),current_agent: models.Agent = Depends(security.get_current_agent)):
    contract_to_update = crud.ContractCRUD.get_by_id_contrat(db, id_contrat)
    
    contract_to_update.projet_id_projet = contract.get("id_projet")
    contract_to_update.id_projet= contract["id_projet"]
    contract_to_update.id_fournisseur = contract["id_fournisseur"]
    contract_to_update.description = contract["description"]
    contract_to_update.date_debut = contract["date_debut"]
    contract_to_update.date_de_notification = contract.get("date_de_notification")
    contract_to_update.min = contract["min"]
    contract_to_update.max = contract.get("max")
    contract_to_update.duree = contract["duree"]
    contract_to_update.etat = contract.get("etat")
    contract_to_update.devise = contract["devise"]
    contract_to_update.type = contract["type"]
    contract_to_update.engagement = contract.get("engagement", 0)
    contract_to_update.projet_chapitre_id_chapitre = contract.get("id_chapitre")
    # Check state history
    hist = crud.HistoriqueEtatCRUD.get_by_id_contrat(db, id_contrat)
    
    if isinstance(hist, list):
        if len(hist) > 0:
            hist.sort(key=lambda x: x.date_debut, reverse=True)
            last_etat = hist[-1].etat
            if last_etat != contract["etat"]:
                description_etat = contract.get("description_etat", "")
                date_etat = contract.get("date_etat", date.today())
                try:
                    create_historique = crud.HistoriqueEtatCRUD.create(
                        db,
                        {
                            "etat": contract["etat"],
                            "description": description_etat,
                            "id_contrat": id_contrat,
                            "date_debut": date_etat,
                            "agent_id_agent": current_agent.id_agent
                        }
                    )
                    db.commit()
                except Exception as e:
                    db.rollback()
                    print(f"Error creating history: {str(e)}")
                    raise HTTPException(500, f"History creation failed: {str(e)}")
        else:
            # Case: hist is an empty list (no history at all)
            description_etat = contract.get("description_etat", "")
            date_etat = contract.get("date_etat", date.today())
            try:
                create_historique = crud.HistoriqueEtatCRUD.create(
                    db,
                    {
                        "etat": contract["etat"],
                        "description": description_etat,
                        "id_contrat": id_contrat,
                        "date_debut": date_etat,
                        "agent_id_agent": contract.get("agent_id_agent")
                    }
                )
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Error creating history: {str(e)}")
                raise HTTPException(500, f"History creation failed: {str(e)}")
    else:
        # Case: hist is None or a single object
        if hist is None or getattr(hist, "etat", None) != contract["etat"]:
            description_etat = contract.get("description_etat", "")
            date_etat = contract.get("date_etat", date.today())
            try:
                create_historique = crud.HistoriqueEtatCRUD.create(
                    db,
                    {
                        "etat": contract["etat"],
                        "description": description_etat,
                        "id_contrat": id_contrat,
                        "date_debut": date_etat,
                        "agent_id_agent": contract.get("agent_id_agent")
                    }
                )
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Error creating history: {str(e)}")
                raise HTTPException(500, f"History creation failed: {str(e)}")
            
    updated = crud.ContractCRUD.update(db, (contract_to_update.id_projet,contract_to_update.id_fournisseur,contract_to_update.id_contrat), contract_to_update.__dict__)
    return get_or_404(updated, "Contract")

@router.delete("/contracts/{id_contrat}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contract(id_contrat: str, db: Session = Depends(get_db)):
    c=crud.ContractCRUD.get_by_id_contrat(db, id_contrat)
    
    success = crud.ContractCRUD.delete(db, (id_contrat, c.projet_id_projet, c.id_fournisseur))
    if not success:
        raise HTTPException(status_code=404, detail="Contract not found")
    return

# ----- Fournisseur -----
@router.get("/fournisseurs", response_model=List[schemas.FournisseurRead])
def list_fournisseurs(db: Session = Depends(get_db)):
    return crud.FournisseurCRUD.get_all(db)

@router.get("/fournisseurs/{id_fournisseur}", response_model=schemas.FournisseurRead)
def get_fournisseur(id_fournisseur: int, db: Session = Depends(get_db)):
    fournisseur = crud.FournisseurCRUD.get(db, id_fournisseur)
    return get_or_404(fournisseur, "Fournisseur")

@router.post("/fournisseurs", response_model=schemas.FournisseurRead, status_code=status.HTTP_201_CREATED)
def create_fournisseur(fournisseur: schemas.FournisseurCreate, db: Session = Depends(get_db)):
    return crud.FournisseurCRUD.create(db, fournisseur.__dict__)

@router.put("/fournisseurs/{id_fournisseur}", response_model=schemas.FournisseurRead)
def update_fournisseur(id_fournisseur: int, fournisseur: schemas.FournisseurCreate, db: Session = Depends(get_db)):
    updated = crud.FournisseurCRUD.update(db, id_fournisseur, fournisseur.__dict__)
    return get_or_404(updated, "Fournisseur")

@router.delete("/fournisseurs/{id_fournisseur}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fournisseur(id_fournisseur: int, db: Session = Depends(get_db)):
    success = crud.FournisseurCRUD.delete(db, id_fournisseur)
    if not success:
        raise HTTPException(status_code=404, detail="Fournisseur not found")
    return

# ----- BonDeCommande -----
@router.get("/bons_de_commande", response_model=List[schemas.BonDeCommandeRead])
def list_bons(db: Session = Depends(get_db)):
    return crud.BonDeCommandeCRUD.get_all(db)

@router.get("/bons_de_commande/{id_bon}", response_model=schemas.BonDeCommandeRead)
def get_bon(id_bon: int, db: Session = Depends(get_db)):
    bon = crud.BonDeCommandeCRUD.get(db, id_bon)
    return get_or_404(bon, "BonDeCommande")

@router.post("/bons_de_commande", response_model=schemas.BonDeCommandeRead, status_code=status.HTTP_201_CREATED)
def create_bon(bon: schemas.BonDeCommandeCreate, db: Session = Depends(get_db)):
    return crud.BonDeCommandeCRUD.create(db, bon.__dict__)

@router.put("/bons_de_commande/{id_bon}", response_model=schemas.BonDeCommandeRead)
def update_bon(id_bon: int, bon: schemas.BonDeCommandeCreate, db: Session = Depends(get_db)):
    updated = crud.BonDeCommandeCRUD.update(db, id_bon, bon.__dict__)
    return get_or_404(updated, "BonDeCommande")

@router.delete("/bons_de_commande/{id_bon}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bon(id_bon: int, db: Session = Depends(get_db)):
    success = crud.BonDeCommandeCRUD.delete(db, id_bon)
    if not success:
        raise HTTPException(status_code=404, detail="BonDeCommande not found")
    return

# ----- PVDeReception -----
@router.get("/pvs", response_model=List[schemas.PVDeReceptionRead])
def list_pvs(db: Session = Depends(get_db)):
    return crud.PVDeReceptionCRUD.get_all(db)

@router.get("/pvs/{id_pv}", response_model=schemas.PVDeReceptionRead)
def get_pv(id_pv: str, db: Session = Depends(get_db)):
    pv = crud.PVDeReceptionCRUD.get(db, id_pv)
    return get_or_404(pv, "PVDeReception")

@router.post("/pvs", response_model=schemas.PVDeReceptionRead, status_code=status.HTTP_201_CREATED)
def create_pv(pv: schemas.PVDeReceptionCreate, db: Session = Depends(get_db)):
    return crud.PVDeReceptionCRUD.create(db, pv.__dict__)

@router.put("/pvs/{id_pv}", response_model=schemas.PVDeReceptionRead)
def update_pv(id_pv: str, pv: schemas.PVDeReceptionCreate, db: Session = Depends(get_db)):
    updated = crud.PVDeReceptionCRUD.update(db, id_pv, pv.__dict__)
    return get_or_404(updated, "PVDeReception")

@router.delete("/pvs/{id_pv}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pv(id_pv: str, db: Session = Depends(get_db)):
    success = crud.PVDeReceptionCRUD.delete(db, id_pv)
    if not success:
        raise HTTPException(status_code=404, detail="PVDeReception not found")
    return

# ----- PVDeReceptionDifinitive -----
@router.get("/pvs_difinitive", response_model=List[schemas.PVDeReceptionDifinitiveRead])
def list_pvs_dif(db: Session = Depends(get_db)):
    return crud.PVDeReceptionDifinitiveCRUD.get_all(db)

@router.get("/pvs_difinitive/{id_pv}", response_model=schemas.PVDeReceptionDifinitiveRead)
def get_pv_dif(id_pv: str, db: Session = Depends(get_db)):
    pv = crud.PVDeReceptionDifinitiveCRUD.get(db, id_pv)
    return get_or_404(pv, "PVDeReceptionDifinitive")

@router.post("/pvs_difinitive", response_model=schemas.PVDeReceptionDifinitiveRead, status_code=status.HTTP_201_CREATED)
def create_pv_dif(pv: schemas.PVDeReceptionDifinitiveCreate, db: Session = Depends(get_db)):
    return crud.PVDeReceptionDifinitiveCRUD.create(db, pv.__dict__)

@router.put("/pvs_difinitive/{id_pv}", response_model=schemas.PVDeReceptionDifinitiveRead)
def update_pv_dif(id_pv: str, pv: schemas.PVDeReceptionDifinitiveCreate, db: Session = Depends(get_db)):
    updated = crud.PVDeReceptionDifinitiveCRUD.update(db, id_pv, pv.__dict__)
    return get_or_404(updated, "PVDeReceptionDifinitive")

@router.delete("/pvs_difinitive/{id_pv}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pv_dif(id_pv: str, db: Session = Depends(get_db)):
    success = crud.PVDeReceptionDifinitiveCRUD.delete(db, id_pv)
    if not success:
        raise HTTPException(status_code=404, detail="PVDeReceptionDifinitive not found")
    return

# ----- HistoriqueEtat -----
@router.get("/historiques_etat", response_model=List[schemas.HistoriqueEtatRead])
def list_historiques(db: Session = Depends(get_db)):
    return crud.HistoriqueEtatCRUD.get_all(db)

@router.get("/historiques_etat/{id_historique}", response_model=schemas.HistoriqueEtatRead)
def get_historique(id_historique: int, db: Session = Depends(get_db)):
    historique = crud.HistoriqueEtatCRUD.get(db, id_historique)
    return get_or_404(historique, "HistoriqueEtat")

@router.post("/historiques_etat", response_model=schemas.HistoriqueEtatRead, status_code=status.HTTP_201_CREATED)
def create_historique(historique: schemas.HistoriqueEtatCreate, db: Session = Depends(get_db)):
    return crud.HistoriqueEtatCRUD.create(db, historique.__dict__)

@router.put("/historiques_etat/{id_historique}", response_model=schemas.HistoriqueEtatRead)
def update_historique(id_historique: int, historique: schemas.HistoriqueEtatCreate, db: Session = Depends(get_db)):
    updated = crud.HistoriqueEtatCRUD.update(db, id_historique, historique.__dict__)
    return get_or_404(updated, "HistoriqueEtat")

@router.delete("/historiques_etat/{id_historique}", status_code=status.HTTP_204_NO_CONTENT)
def delete_historique(id_historique: int, db: Session = Depends(get_db)):
    success = crud.HistoriqueEtatCRUD.delete(db, id_historique)
    if not success:
        raise HTTPException(status_code=404, detail="HistoriqueEtat not found")
    return

#---------- Etat -----------
@router.get("/etats", response_model=List[schemas.EtatRead])
def list_etats(db: Session = Depends(get_db)):
    return crud.EtatCRUD.get_all(db)

@router.get("/etats/{id_etat}", response_model=schemas.EtatRead)
def get_etat(id_etat: int, db: Session = Depends(get_db)):
    etat = crud.EtatCRUD.get(db, id_etat)
    return get_or_404(etat, "Etat")

@router.post("/etats", response_model=schemas.EtatCreate, status_code=status.HTTP_201_CREATED)
def create_etat(etat: schemas.EtatCreate, db: Session = Depends(get_db)):
    return crud.EtatCRUD.create(db, etat.__dict__)

@router.put("/etats/{id_etat}", response_model=schemas.EtatRead)
def update_etat(id_etat: int, etat: schemas.EtatCreate, db: Session = Depends(get_db)):
    updated = crud.EtatCRUD.update(db, id_etat, etat.__dict__)
    return get_or_404(updated, "Etat")

@router.delete("/etats/{id_etat}", status_code=status.HTTP_204_NO_CONTENT)
def delete_etat(id_etat: int, db: Session = Depends(get_db)):
    success = crud.EtatCRUD.delete(db, id_etat)
    if not success:
        raise HTTPException(status_code=404, detail="Etat not found")
    return

