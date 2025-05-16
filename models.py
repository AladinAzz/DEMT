from sqlalchemy import (
    Column, Integer, String, Text, Float, Date, Enum as SqlEnum, ForeignKey,
    UniqueConstraint, PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from enum import Enum

Base = declarative_base()

# ---------------------- ENUMS ----------------------

class RoleEnum(str, Enum):
    directeur = 'directeur'
    chef_direction = 'chef direction'
    chef_bureau = 'chef bureau'
    agent = 'agent'

class ProjetTypeEnum(str, Enum):
    contrat = 'contrat'
    marche = 'marché'
    achat = 'achat sur facture'

class DeviseEnum(str, Enum):
    DZD = 'DZD'
    DOLLAR = 'DOLLAR'
    EURO = 'EURO'

class ContractTypeEnum(str, Enum):
    ferme = 'ferme'
    commande = 'a commande'

# ---------------------- TABLES ----------------------

class Direction(Base):
    __tablename__ = 'direction'
    id_direction = Column(Integer, primary_key=True)
    nom_direction = Column(String(100), nullable=False)

    agents = relationship("Agent", back_populates="direction")
    bureaux = relationship("Bureau", back_populates="direction")

class Bureau(Base):
    __tablename__ = 'bureau'
    id_bureau = Column(Integer, primary_key=True)
    nom_bureau = Column(String(100), nullable=False)
    id_direction = Column(Integer, ForeignKey('direction.id_direction'), nullable=False)

    direction = relationship("Direction", back_populates="bureaux")
    agents = relationship("Agent", back_populates="bureau")
    projets = relationship("Projet", back_populates="bureau")

class Agent(Base):
    __tablename__ = 'agent'
    id_agent = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    role = Column(SqlEnum(RoleEnum), nullable=False)
    direction_id_direction = Column(Integer, ForeignKey('direction.id_direction'), nullable=False)
    password = Column(String(100), nullable=False)
    bureau_id_bureau = Column(Integer, ForeignKey('bureau.id_bureau'), nullable=False)
    username = Column(String(45), unique=True, nullable=False)

    direction = relationship("Direction", back_populates="agents")
    bureau = relationship("Bureau", back_populates="agents")

class Chapitre(Base):
    __tablename__ = 'chapitre'
    id_chapitre = Column(Integer, primary_key=True)
    nom = Column(String(45), nullable=False)
    description = Column(Text, nullable=True)
    engagement = Column(Float, nullable=False, default=0)
    montant_initiale = Column(Float, nullable=False)
    mondatement = Column(Float, nullable=False)

    projets = relationship("Projet", back_populates="chapitre")

class Projet(Base):
    __tablename__ = 'projet'
    id_projet = Column(Integer, primary_key=True)
    nom_projet = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    id_bureau = Column(Integer, ForeignKey('bureau.id_bureau'), nullable=False)
    chapitre_id_chapitre = Column(Integer, ForeignKey('chapitre.id_chapitre'), nullable=False)
    type = Column(SqlEnum(ProjetTypeEnum), nullable=False)

    bureau = relationship("Bureau", back_populates="projets")
    chapitre = relationship("Chapitre", back_populates="projets")
    achats = relationship("AchatSurFacture", back_populates="projet")
    contrats = relationship("Contract", back_populates="projet")
    historiques = relationship("HistoriqueEtat", back_populates="projet")

class AchatSurFacture(Base):
    __tablename__ = 'achat_sur_facture'
    id_facture = Column(String(45), primary_key=True)
    montant = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    projet_id_projet = Column(Integer, ForeignKey('projet.id_projet'), nullable=False)

    projet = relationship("Projet", back_populates="achats")

class Fournisseur(Base):
    __tablename__ = 'fournisseur'
    id_fournisseur = Column(Integer, primary_key=True)
    nom = Column(String(100), nullable=False)
    adresse = Column(Text, nullable=True)
    contact = Column(Text, nullable=True)

    contrats = relationship("Contract", back_populates="fournisseur")

class Contract(Base):
    __tablename__ = 'contract'
    id_contrat = Column(String(45), primary_key=True)
    description = Column(Text, nullable=True)
    date_debut = Column(Date, nullable=False)
    date_de_notification = Column(Date, nullable=True)
    min = Column(Float, nullable=False)
    max = Column(Float, nullable=True)
    duree = Column(Integer, nullable=False)
    id_projet = Column(Integer, ForeignKey('projet.id_projet'), nullable=False)
    id_fournisseur = Column(Integer, ForeignKey('fournisseur.id_fournisseur'), nullable=False)
    devise = Column(SqlEnum(DeviseEnum), nullable=False)
    type = Column(SqlEnum(ContractTypeEnum), nullable=False)

    projet = relationship("Projet", back_populates="contrats")
    fournisseur = relationship("Fournisseur", back_populates="contrats")
    bons = relationship("BonDeCommande", back_populates="contract")
    pv_definitifs = relationship("PVDeReceptionDifinitive", back_populates="contract")

class BonDeCommande(Base):
    __tablename__ = 'bon_de_commande'
    id_bon = Column(Integer, primary_key=True)
    date_bon = Column(Date, nullable=False)
    description = Column(Text, nullable=True)
    montant = Column(Float, nullable=False)
    etat = Column(String(50), nullable=False)
    date_de_notification = Column(Date, nullable=True)
    delais = Column(Integer, nullable=False)
    agent_id_agent = Column(Integer, ForeignKey('agent.id_agent'), nullable=False)
    contract_id_projet = Column(Integer, nullable=False)
    contract_id_fournisseur = Column(Integer, nullable=False)
    contract_id_contrat = Column(String(45), ForeignKey('contract.id_contrat'), nullable=False)

    agent = relationship("Agent")
    contract = relationship("Contract", back_populates="bons")
    pvs = relationship("PVDeReception", back_populates="bon")

class PVDeReception(Base):
    __tablename__ = 'pv_de_reception'
    id_PV = Column(String(45), primary_key=True)
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)
    id_bon = Column(Integer, ForeignKey('bon_de_commande.id_bon'), nullable=False)
    agent_id_agent = Column(Integer, ForeignKey('agent.id_agent'), nullable=False)

    bon = relationship("BonDeCommande", back_populates="pvs")
    agent = relationship("Agent")
    factures = relationship("Facture", back_populates="pv")

class Facture(Base):
    __tablename__ = 'facture'
    id_facture = Column(String(45), primary_key=True)
    date = Column(Date, nullable=False)
    montant = Column(Float, nullable=False)
    id_PV = Column(String(45), ForeignKey('pv_de_reception.id_PV'), nullable=False)
    agent_id_agent = Column(Integer, ForeignKey('agent.id_agent'), nullable=False)

    pv = relationship("PVDeReception", back_populates="factures")
    agent = relationship("Agent")

class HistoriqueEtat(Base):
    __tablename__ = 'historique_etat'
    id_historique = Column(Integer, primary_key=True)
    id_projet = Column(Integer, ForeignKey('projet.id_projet'), nullable=False)
    etat = Column(String(45), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    agent_id_agent = Column(Integer, ForeignKey('agent.id_agent'), nullable=False)

    projet = relationship("Projet", back_populates="historiques")
    agent = relationship("Agent")

class PVDeReceptionDifinitive(Base):
    __tablename__ = 'pv_de_reception_difinitive'
    id_pv_de_rec_difinitive = Column(String(45), primary_key=True)
    date_etablissement = Column(Date, nullable=False)
    contract_id_projet = Column(Integer, nullable=False)
    contract_id_fournisseur = Column(Integer, nullable=False)
    contract_id_contract = Column(String(45), ForeignKey('contract.id_contrat'), nullable=False)

    contract = relationship("Contract", back_populates="pv_definitifs")
