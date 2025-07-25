from sqlalchemy.orm import Session
from typing import List, Optional, Any
import models
from security import *
# -----------------------------
# Generic CRUD Helpers (used by all below)
# -----------------------------
def get_all(db: Session, model):
    return db.query(model).all()

def get_by_id(db: Session, model, id: Any):
    return db.query(model).get(id)

def create(db: Session, model, data: dict):
    obj = model(**data)
    db.add(obj)
    db.commit()
    
    return obj

def update(db: Session, model, id: Any, data: dict):
    obj = db.query(model).get(id)
    if not obj:
        return None
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, model, id: Any):
    obj = db.query(model).get(id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

# -----------------------------
# Per-table CRUD
# -----------------------------

# Define CRUD classes for all models below

class AgentCRUD:
    model = models.Agent
    @staticmethod
    def get_all(db: Session): return get_all(db, AgentCRUD.model)
    @staticmethod
    def get(db: Session, id: int): return get_by_id(db, AgentCRUD.model, id)
    @staticmethod
    def create(db: Session, data: dict): 
        data['password'] = get_password_hash(data['password'])
        return create(db, AgentCRUD.model, data)
    @staticmethod
    def update(db: Session, id: int, data: dict): 
        data['password'] = get_password_hash(data['password'])
        return update(db, AgentCRUD.model, id, data)
    @staticmethod
    def delete(db: Session, id: int): return delete(db, AgentCRUD.model, id)

class ProjetCRUD:
    model = models.Projet
    @staticmethod
    def get_by_id_chapitre(db: Session, id: int, model=None):
        if model is None:
            model = ProjetCRUD.model
        return db.query(model).filter(model.chapitre_id_chapitre == id).all()
    @staticmethod
    def get_all(db: Session): return get_all(db, ProjetCRUD.model)
    @staticmethod
    def get(db: Session, id: int): return get_by_id(db, ProjetCRUD.model, id)
    @staticmethod
    def create(db: Session, data: dict): return create(db, ProjetCRUD.model, data)
    @staticmethod
    def update(db: Session, id: int, data: dict): return update(db, ProjetCRUD.model, id, data)
    @staticmethod
    def delete(db: Session, id: int): return delete(db, ProjetCRUD.model, id)

class BureauCRUD:
    model = models.Bureau
    @staticmethod
    def get_all(db: Session): return get_all(db, BureauCRUD.model)
    @staticmethod
    def get(db: Session, id: int): return get_by_id(db, BureauCRUD.model, id)
    @staticmethod
    def create(db: Session, data: dict): return create(db, BureauCRUD.model, data)
    @staticmethod
    def update(db: Session, id: int, data: dict): return update(db, BureauCRUD.model, id, data)
    @staticmethod
    def delete(db: Session, id: int): return delete(db, BureauCRUD.model, id)

class DirectionCRUD:
    model = models.Direction
    @staticmethod
    def get_all(db: Session): return get_all(db, DirectionCRUD.model)
    @staticmethod
    def get(db: Session, id: int): return get_by_id(db, DirectionCRUD.model, id)
    @staticmethod
    def create(db: Session, data: dict): return create(db, DirectionCRUD.model, data)
    @staticmethod
    def update(db: Session, id: int, data: dict): return update(db, DirectionCRUD.model, id, data)
    @staticmethod
    def delete(db: Session, id: int): return delete(db, DirectionCRUD.model, id)

class ChapitreCRUD:
    model = models.Chapitre
    @staticmethod
    def get_by_id_chapitre(db: Session, id: int, model=None):
        if model is None:
            model = ChapitreCRUD.model
        return db.query(model).filter(model.id_chapitre == id).all()
    @staticmethod
    def get_all(db: Session): return get_all(db, ChapitreCRUD.model)
    @staticmethod
    def get(db: Session, id: int): return get_by_id(db, ChapitreCRUD.model, id)
    @staticmethod
    def create(db: Session, data: dict): return create(db, ChapitreCRUD.model, data)
    @staticmethod
    def update(db: Session, id: int, data: dict): return update(db, ChapitreCRUD.model, id, data)
    @staticmethod
    def delete(db: Session, id: int): return delete(db, ChapitreCRUD.model, id)

class AchatSurFactureCRUD:
    model = models.AchatSurFacture
    @staticmethod
    def get_all(db: Session): return get_all(db, AchatSurFactureCRUD.model)
    @staticmethod
    def get_by_id_projet(db: Session, id: Any, model=None):
        if model is None:
            model = AchatSurFactureCRUD.model
        # Retourne tous les achats sur facture du projet
        return db.query(model).filter(model.projet_id_projet == id).all()
    @staticmethod
    def get_by_id_facture(db: Session, id: Any, model=None):
        if model is None:
            model = AchatSurFactureCRUD.model
        # Retourne tous les achats sur facture du projet
        return db.query(model).filter(model.id_facture == id).first()
                          
    @staticmethod
    def get(db: Session, id: Any): return get_by_id(db, AchatSurFactureCRUD.model, id)
    @staticmethod
    def create(db: Session, data: dict): return create(db, AchatSurFactureCRUD.model, data)
    @staticmethod
    def update(db: Session, id: any, data: dict): return update(db, AchatSurFactureCRUD.model, id, data)
    @staticmethod
    def delete(db: Session, id: any): return delete(db, AchatSurFactureCRUD.model, id)

class ContractCRUD:
    model = models.Contract
    @staticmethod
    def get_all(db: Session): return get_all(db, ContractCRUD.model)
    @staticmethod
    def get(db: Session, id: str): return get_by_id(db, ContractCRUD.model, id)
    @staticmethod
    def get_by_id_projet(db: Session, id: Any, model=None):
        if model is None:
            model = ContractCRUD.model
        # Retourne tous les contrats du projet
        return db.query(model).filter(model.id_projet == id).all()
    @staticmethod
    def get_by_id_contrat(db: Session, id: Any, model=None):
        if model is None:
            model = ContractCRUD.model
        # Retourne le contrat par son id
        return db.query(model).filter(model.id_contrat == id).first()
    @staticmethod
    def create(db: Session, data: dict): return create(db, ContractCRUD.model, data)
    @staticmethod
    def update(db: Session, id: str, data: dict): return update(db, ContractCRUD.model, id, data)
    @staticmethod
    def delete(db: Session, id: str): return delete(db, ContractCRUD.model, id)

class FournisseurCRUD:
    model = models.Fournisseur
    @staticmethod
    def get_all(db: Session): return get_all(db, FournisseurCRUD.model)
    @staticmethod
    def get(db: Session, id: int): return get_by_id(db, FournisseurCRUD.model, id)
    @staticmethod
    def create(db: Session, data: dict): return create(db, FournisseurCRUD.model, data)
    @staticmethod
    def update(db: Session, id: int, data: dict): return update(db, FournisseurCRUD.model, id, data)
    @staticmethod
    def delete(db: Session, id: int): return delete(db, FournisseurCRUD.model, id)

class BonDeCommandeCRUD:
    model = models.BonDeCommande
    @staticmethod
    def get_all(db: Session): return get_all(db, BonDeCommandeCRUD.model)
    @staticmethod
    def get(db: Session, id: int): return get_by_id(db, BonDeCommandeCRUD.model, id)
    @staticmethod
    def get_by_id_contrat(db: Session, id: Any, model=None):
        if model is None:
            model = BonDeCommandeCRUD.model
        return db.query(model).filter(model.contract_id_contrat == id).all()
    @staticmethod
    def get_by_id_project(db: Session, id: Any, model=None):
        if model is None:
            model = BonDeCommandeCRUD.model
        return db.query(model).filter(model.contract_id_projet == id and model.achat_sur_facture_projet_id_projet==None or model.achat_sur_facture_projet_id_projet == id).all()
    @staticmethod
    def get_by_id_achat(db: Session, id: Any, model=None):
        if model is None:
            model = BonDeCommandeCRUD.model
        return db.query(model).filter(model.achat_sur_facture_id_facture == id).all()
    @staticmethod
    def create(db: Session, data: dict): return create(db, BonDeCommandeCRUD.model, data)
    @staticmethod
    def update(db: Session, id: int, data: dict): return update(db, BonDeCommandeCRUD.model, id, data)
    @staticmethod
    def delete(db: Session, id: int): return delete(db, BonDeCommandeCRUD.model, id)

class PVDeReceptionCRUD:
    model = models.PVDeReception
    @staticmethod
    def get_all(db: Session): return get_all(db, PVDeReceptionCRUD.model)
    @staticmethod
    def get(db: Session, id: str): return get_by_id(db, PVDeReceptionCRUD.model, id)
    @staticmethod
    def get_by_id_commande(db: Session, id: Any, model=None):
        if model is None:
            model = PVDeReceptionCRUD.model
        return db.query(model).filter(model.id_bon == id).all()
    @staticmethod
    def create(db: Session, data: dict): return create(db, PVDeReceptionCRUD.model, data)
    @staticmethod
    def update(db: Session, id: str, data: dict): return update(db, PVDeReceptionCRUD.model, id, data)
    @staticmethod
    def delete(db: Session, id: str): return delete(db, PVDeReceptionCRUD.model, id)

class PVDeReceptionDifinitiveCRUD:
    model = models.PVDeReceptionDifinitive
    @staticmethod
    def get_all(db: Session): return get_all(db, PVDeReceptionDifinitiveCRUD.model)
    @staticmethod
    def get(db: Session, id: str): return get_by_id(db, PVDeReceptionDifinitiveCRUD.model, id)
    @staticmethod
    def create(db: Session, data: dict): return create(db, PVDeReceptionDifinitiveCRUD.model, data)
    @staticmethod
    def update(db: Session, id: str, data: dict): return update(db, PVDeReceptionDifinitiveCRUD.model, id, data)
    @staticmethod
    def delete(db: Session, id: str): return delete(db, PVDeReceptionDifinitiveCRUD.model, id)


class HistoriqueEtatCRUD:
    model = models.HistoriqueEtat
    @staticmethod
    def get_all(db: Session): return get_all(db, HistoriqueEtatCRUD.model)
    @staticmethod
    def get(db: Session, id: int): return get_by_id(db, HistoriqueEtatCRUD.model, id)
    @staticmethod
    def get_by_id_projet(db: Session, id: Any, model=None):
        if model is None:
            model = HistoriqueEtatCRUD.model
        return db.query(model).filter(model.id_projet == id).all()
    @staticmethod
    def get_by_id_contrat(db: Session, id: Any, model=None):
        if model is None:
            model = HistoriqueEtatCRUD.model
        return db.query(model).filter(model.id_contrat == id).all()
    @staticmethod
    def get_by_id_achat(db: Session, id: Any, model=None):
        if model is None:
            model = HistoriqueEtatCRUD.model
        return db.query(model).filter(model.id_facture == id).all()
    @staticmethod
    def create(db: Session, data: dict): return create(db, HistoriqueEtatCRUD.model, data)
    @staticmethod
    def update(db: Session, id: int, data: dict): return update(db, HistoriqueEtatCRUD.model, id, data)
    @staticmethod
    def delete(db: Session, id: int): return delete(db, HistoriqueEtatCRUD.model, id)

class EtatCRUD:
    model = models.etat

    @staticmethod
    def get_all(db: Session):
        return get_all(db, EtatCRUD.model)

    @staticmethod
    def get(db: Session, id: int):
        return get_by_id(db, EtatCRUD.model, id)

    @staticmethod
    def create(db: Session, data: dict):
        return create(db, EtatCRUD.model, data)

    @staticmethod
    def update(db: Session, id: int, data: dict):
        return update(db, EtatCRUD.model, id, data)

    @staticmethod
    def delete(db: Session, id: int):
        return delete(db, EtatCRUD.model, id)

