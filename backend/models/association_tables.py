from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

# Table d'association Many-to-Many entre Sequence et Objective
sequence_objective_association = Table(
    'sequence_objective_association',
    Base.metadata,
    Column('sequence_id', Integer, ForeignKey('sequences.id'), primary_key=True),
    Column('objective_id', Integer, ForeignKey('objectives.id'), primary_key=True) # 'objectives.id' sera défini plus tard
)

# Table d'association Many-to-Many entre Session et Objective
session_objective_association = Table(
    'session_objective_association',
    Base.metadata,
    Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True),
    Column('objective_id', Integer, ForeignKey('objectives.id'), primary_key=True) # 'objectives.id' sera défini plus tard
)
