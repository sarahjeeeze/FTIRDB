"""

Project: FTIRDB
File: models/FTIRModel.py

Version: v1.0
Date: 10.09.2018
Function: Create the main FTIRDB table in the data base this may be edited easily

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

This file contains the SQLalchemy model for the FTIRDB.

The model includes any contstraints that entered data should adhere to as well as any
links to other models.


"""

#import necessary modules from sqlalchemy - may need to add others

from sqlalchemy import (
    Column,
    Index,
    Integer,
    text,
    Text,
    ForeignKey,
    String,
    
)

from .meta import Base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Date, String
from sqlalchemy.dialects.mysql import INTEGER, TINYINT




from sqlalchemy import Column, Date, Enum, ForeignKey, LargeBinary, String, Table
from sqlalchemy.dialects.mysql import INTEGER, LONGBLOB, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


metadata = Base.metadata


class project(Base):
    __tablename__ = 'project'

    descriptive_name = Column(String(300))
    project_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    related_experiments_ID = Column(String(100))
    related_samples_ID = Column(String(100))

    
class sample(Base):
    __tablename__ = 'sample'

    sample_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    descriptive_name = Column(String(45))
    composition = Column(String(45))

    #parent
    state_of_sample = relationship('state_of_sample',uselist=False, back_populates='sample',  info={'colanderalchemy': {'exclude': True}})
    molecules_in_sample = relationship('molecules_in_sample',uselist=False, back_populates='sample',  info={'colanderalchemy': {'exclude': True}})


class state_of_sample(Base):
    __tablename__ = 'state_of_sample'

    state_of_sample_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    state = Column(Enum('gas', 'solid', 'dried film', 'liquid'), nullable=False, info={'colanderalchemy': {'exclude': True}})
    #enter this somehow with a radiobutton or tick box?
    temperature_degrees = Column(INTEGER(11))
    pressure_PSI = Column(INTEGER(11))
    #child 
    sample_ID = Column(Integer, ForeignKey('sample.sample_ID'),  info={'colanderalchemy': {'exclude': True}})

    sample = relationship('sample', back_populates='state_of_sample',  info={'colanderalchemy': {'exclude': True}})
    #relationship to various states, parent
    liquid = relationship('liquid', uselist=False, back_populates='state_of_sample',  info={'colanderalchemy': {'exclude': True}})
    dried_film = relationship('dried_film', uselist=False, back_populates='state_of_sample',  info={'colanderalchemy': {'exclude': True}})
    solid = relationship('solid', uselist=False, back_populates='state_of_sample',  info={'colanderalchemy': {'exclude': True}})
    gas = relationship('gas', uselist=False, back_populates='state_of_sample',  info={'colanderalchemy': {'exclude': True}})


class molecules_in_sample(Base):
    __tablename__ = 'molecules_in_sample'

    molecular_composition_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    descriptive_name = Column(String(45))
    molecule_1_name = Column(String(45))
    concentration_1 = Column(INTEGER(11))
    molecule_2_name = Column(String(45))
    concentration_2 = Column(INTEGER(11))
    molecule_3_name = Column(String(45))
    concentration_3 = Column(INTEGER(11))
    molecule_4_name = Column(String(45))
    concentration_4 = Column(INTEGER(11))

    #child
    sample_ID = Column(Integer, ForeignKey('sample.sample_ID'),  info={'colanderalchemy': {'exclude': True}})
    sample = relationship('sample', back_populates='molecules_in_sample',  info={'colanderalchemy': {'exclude': True}})


class liquid(Base):
    __tablename__ = 'liquid'

    solution_composition = Column(String(100), nullable=False)
    pH = Column(String(45))
    concentration = Column(String(45))
    solvent = Column(String(45))
    atmosphere = Column(String(45))
    sample_ID = Column(INTEGER(11), primary_key=True)

    state_of_sample_ID = Column(Integer, ForeignKey('state_of_sample.state_of_sample_ID'))
    state_of_sample = relationship('state_of_sample',back_populates='liquid')




class dried_film(Base):
    __tablename__ = 'dried_film'

    atmosphere = Column(String(45))
    solution__composition = Column('solution_composition', String(45))
    concentration = Column(String(45))
    volume = Column(String(45))
    area = Column(String(45))
    solvent = Column(String(45))
    pH = Column(String(45), server_default=text("'RANGE(0,14)'"))
    sample_ID = Column(INTEGER(11), primary_key=True)

    state_of_sample_ID = Column(Integer, ForeignKey('state_of_sample.state_of_sample_ID'))
    state_of_sample = relationship('state_of_sample',back_populates='dried_film')


class gas(Base):
    __tablename__ = 'gas'

    atmosphere = Column(String(45))
    water_vapour = Column(String(45))
    sample_ID = Column(INTEGER(11), primary_key=True)

    state_of_sample_ID = Column(Integer, ForeignKey('state_of_sample.state_of_sample_ID'))
    state_of_sample = relationship('state_of_sample',back_populates='gas')


class solid(Base):
    __tablename__ = 'solid'

    crystal_form = Column(String(45))
    chemical_formula = Column(String(45))
    sample_ID = Column(INTEGER(11), primary_key=True)

    state_of_sample_ID = Column(Integer, ForeignKey('state_of_sample.state_of_sample_ID'))
    state_of_sample = relationship('state_of_sample',back_populates='solid')

class FTIRModel(Base):
    """ This class is to create the main FTIRModel table with SQL alchemy """
    __tablename__ = 'FTIRModel'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    data = Column(Text, nullable=False)
    magic = Column(Text, nullable=False)
    
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='created_pages')

