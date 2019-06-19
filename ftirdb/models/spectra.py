"""

Project: FTIRDB
File: models/spectra.py

Version: v1.0
Date: 10.09.2018
Function: Create the main FTIRDB table in the data base this may be edited easily

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

This file contains a different SQLalchemy model used for experimenting with different data models.



"""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    String,
)


from .meta import Base

class Spectra(Base):
    __tablename__ = 'Spectra'
    spectra_id = Column(Integer, primary_key=True)
    label = Column(String(32), nullable=False, unique=True)
    time = Column(Integer, nullable=False)


   

    

class Spectra_detail(Base):
    __tablename__ = 'Spectra_detail'
    spectra_id = Column(Integer, primary_key=True)
    index= Column(Integer, nullable=False, unique=True)
    value = Column(Integer, nullable=False)
    

 

class Graph_experiment(Base):
    __tablename__ = 'Graph_experiment'
    spectra_id = Column(Integer, primary_key = True)
    a = Column(Integer, nullable=False)
    b = Column(Integer, nullable=False)
    c = Column(Integer, nullable=False)
    d = Column(Integer, nullable=False)


