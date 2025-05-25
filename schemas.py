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
    consultation = 'consultation'
    achat = 'achat'
    GAG = 'GAG'
    AOON = 'AOON'

class DeviseEnum(str, Enum):
    DZD = 'DZD'
    DOLLAR = 'DOLLAR'
    EURO = 'EURO'

class ContractTypeEnum(str, Enum):
    ferme = 'ferme'
    commande = 'a commande'


    
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
    nb_projets: Optional[int]
    nb_cotrats: Optional[int]

class ChapitreCreate(ChapitreBase): pass
class ChapitreRead(ChapitreBase):
    id_chapitre: int
    class Config:
        orm_mode = True


class ProjetBase(BaseModel):
    nom_projet: str
    description: Optional[str]
    date_debut: date
    date_fin: Optional[date]
    id_bureau: int
    montant: float
    chapitre_id_chapitre: int
    type: ProjetTypeEnum
    etat:Optional[str]

class ProjetCreate(ProjetBase): 
    nom_projet: str
    description: Optional[str]
    date_debut: date
    id_bureau: int
    montant: float
    chapitre_id_chapitre: int
    type: ProjetTypeEnum
    etat:Optional[str]=None
    description_etat: Optional[str]=None
class ProjetRead(ProjetBase):
    nom_projet: str
    description: Optional[str]
    date_debut: date
    id_bureau: int
    montant: float
    chapitre_id_chapitre: int
    type: ProjetTypeEnum
    etat:Optional[str]=None
    description_etat: Optional[str]=None
    
    
    chapitre_id_chapitre: int
    type: ProjetTypeEnum
    
    
    
    class Config:
        orm_mode = True


class AchatSurFactureBase(BaseModel):
    montant: float
    description: Optional[str]
    date: date
    projet_id_projet: int
    id_fournisseur: int
    devise: DeviseEnum
    engagement: Optional[float] = 0
    etat:Optional[str]=None
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
    etat: Optional[str]
    id_projet: int
    id_fournisseur: int
    devise: DeviseEnum
    type: ContractTypeEnum
    engagement: Optional[float] = 0
    projet_id_projet: int
    projet_chapitre_id_chapitre: int

class ContractCreate(ContractBase):
    id_contrat: str
    description: Optional[str]
    date_debut: date
    date_de_notification: Optional[date]
    min: float
    max: Optional[float]
    duree: int
    etat:Optional[str]
    projet_id_projet: int
    id_fournisseur: int
    devise: DeviseEnum
    type: ContractTypeEnum
    engagement: float = 0
    projet_chapitre_id_chapitre: int

class ContractRead(BaseModel):
    id_contrat: str
    type: str  # "ferme" or "commande"
    description: str
    date_debut: date
    date_de_notification: date
    duree: int # Accepts both string and integer
    min: Optional[float] = None
    max: Optional[float] = None
    montant: Optional[float] = None  # Only for "ferme" type contracts
    etat: str  # "engagement" or "instance engagé"
    engagement: float
    projet_chapitre_id_chapitre: int  # Accepts both string and integer
    id_projet: int  # Accepts both string and integer
    id_fournisseur: int  # Accepts both string and integer
    devise: str  # "DZD", "EURO", or "DOLLAR"
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
    contract_id_contrat: Optional[str] = None
    contract_id_projet: Optional[int] = None
    contract_id_fournisseur: Optional[int] = None
    achat_sur_facture_id_facture: Optional[str] = None
    achat_sur_facture_projet_id_projet: Optional[int] = None 
    achat_sur_facture_id_fournisseur: Optional[int] = None   

class BonDeCommandeCreate(BonDeCommandeBase):
    id_bon: int

class BonDeCommandeRead(BonDeCommandeBase):
    id_bon: int
    class Config:
        orm_mode = True


class PVDeReceptionBase(BaseModel):
    date_pv: date
    description: Optional[str]
    id_bon: int
    date_facture: Optional[date]
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





class HistoriqueEtatBase(BaseModel):
    id_projet: Optional[int]=None
    etat: str
    date_debut: date
    date_fin: Optional[date]
    description: Optional[str]
    agent_id_agent: int
    id_facture: Optional[str] = None
    id_contrat: Optional[str] = None

class HistoriqueEtatCreate(BaseModel):
    etat: str
    date_debut: date
    description: Optional[str]
    agent_id_agent: int
    id_projet: Optional[int]=None
    id_facture: Optional[str] = None
    id_contrat: Optional[str] = None

class HistoriqueEtatRead(HistoriqueEtatCreate):
    class Config:
        orm_mode = True
