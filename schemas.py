from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

# -------- Enums --------
class RoleEnum(str, Enum):
    directeur = 'directeur'
    chef_direction = 'chef direction'
    chef_bureau = 'chef bureau'
    agent = 'agent'

class ProjetTypeEnum(str, Enum):
    contrat = 'contrat'
    marche = 'marche'
    achat = 'achat'

class DeviseEnum(str, Enum):
    DZD = 'DZD'
    DOLLAR = 'DOLLAR'
    EURO = 'EURO'

class ContractTypeEnum(str, Enum):
    ferme = 'ferme'
    commande = 'a commande'

class EtatEnum(str, Enum):
    CahierDeCharge = 'Cahier de charge'
    Pub_CC = 'Pub CC'
    COPEO= 'COPEO'
    VisaCF= 'VisaCF'
    CCTP= 'CCTP'
    VisaCahierDeChargeCSM= 'Visa Cahier de charge CSM'
    Pub_AOON= 'Pub AOON'
    VisaCSM= 'Visa CSM'
    FP= 'F/P'
    engagement= 'Engagement'
    rejet= 'Rejet'
    
# -------- Schemas --------

class AgentBase(BaseModel):
    nom: str
    prenom: str
    role: RoleEnum
    direction_id_direction: int
    password: str
    bureau_id_bureau: int
    username: str

class AgentCreate(AgentBase): pass
class AgentRead(AgentBase):
    id_agent: int
    class Config:
        orm_mode = True


class BureauBase(BaseModel):
    nom_bureau: str
    id_direction: int

class BureauCreate(BureauBase): pass
class BureauRead(BureauBase):
    id_bureau: int
    class Config:
        orm_mode = True


class DirectionBase(BaseModel):
    nom_direction: str
    

class DirectionCreate(DirectionBase): pass
class DirectionRead(DirectionBase):
    id_direction: int
    class Config:
        orm_mode = True


class ChapitreBase(BaseModel):
    nom: str
    description: Optional[str]
    engagement: float
    montant_initiale: float
    mondatement: float

class ChapitreCreate(ChapitreBase): pass
class ChapitreRead(ChapitreBase):
    id_chapitre: int
    class Config:
        orm_mode = True


class ProjetBase(BaseModel):
    nom_projet: str
    description: Optional[str]
    date_debut: date
    date_fin: date
    id_bureau: int
    chapitre_id_chapitre: int
    type: ProjetTypeEnum

class ProjetCreate(ProjetBase): pass
class ProjetRead(ProjetBase):
    id_projet: int
    class Config:
        orm_mode = True


class AchatSurFactureBase(BaseModel):
    montant: float
    date: date
    projet_id_projet: int
    id_fournisseur: int
    devise: DeviseEnum
    class Config:
        extra = "allow"
class AchatSurFactureCreate(AchatSurFactureBase):
    id_facture: str

class AchatSurFactureRead(AchatSurFactureCreate):
    class Config:
        orm_mode = True


class ContractBase(BaseModel):
    description: Optional[str]
    date_debut: date
    date_de_notification: Optional[date]
    min: float
    max: Optional[float]
    duree: int
    etat:Optional[str]
    id_projet: int
    id_fournisseur: int
    devise: DeviseEnum
    type: ContractTypeEnum

class ContractCreate(ContractBase):
    id_contrat: str

class ContractRead(ContractCreate):
    class Config:
        orm_mode = True


class FournisseurBase(BaseModel):
    nom: str
    adresse: Optional[str]
    contact: Optional[str]

class FournisseurCreate(FournisseurBase): pass
class FournisseurRead(FournisseurBase):
    id_fournisseur: int
    class Config:
        orm_mode = True


class BonDeCommandeBase(BaseModel):
    date_bon: date
    description: Optional[str]
    montant: float
    etat: str
    date_de_notification: Optional[date]
    delais: int
    agent_id_agent: int
    contract_id_projet: int
    contract_id_fournisseur: int
    contract_id_contrat: str

class BonDeCommandeCreate(BonDeCommandeBase):
    id_bon: int

class BonDeCommandeRead(BonDeCommandeCreate):
    class Config:
        orm_mode = True


class PVDeReceptionBase(BaseModel):
    date: date
    description: Optional[str]
    id_bon: int
    date_f: Optional[date]
    montant: Optional[float]
    agent_id_agent: int

class PVDeReceptionCreate(PVDeReceptionBase):
    id_PV: str

class PVDeReceptionRead(PVDeReceptionCreate):
    class Config:
        orm_mode = True


class PVDeReceptionDifinitiveBase(BaseModel):
    date_etablissement: date
    contract_id_projet: int
    contract_id_fournisseur: int
    contract_id_contract: str

class PVDeReceptionDifinitiveCreate(PVDeReceptionDifinitiveBase):
    id_pv_de_rec_difinitive: str

class PVDeReceptionDifinitiveRead(PVDeReceptionDifinitiveCreate):
    class Config:
        orm_mode = True


class FactureBase(BaseModel):
    date: date
    montant: float
    id_PV: str
    agent_id_agent: int

class FactureCreate(FactureBase):
    id_facture: str

class FactureRead(FactureCreate):
    class Config:
        orm_mode = True


class HistoriqueEtatBase(BaseModel):
    id_projet: int
    etat: EtatEnum
    date_debut: date
    date_fin: Optional[date]
    description: Optional[str]
    agent_id_agent: int

class HistoriqueEtatCreate(HistoriqueEtatBase):
    id_historique: int

class HistoriqueEtatRead(HistoriqueEtatCreate):
    class Config:
        orm_mode = True
