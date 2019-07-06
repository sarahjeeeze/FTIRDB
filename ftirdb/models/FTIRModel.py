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
    Float
    
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

    descriptive_name = Column(String(300),info={'colanderalchemy': {'description': 'explain what the project is'}})
    project_ID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    related_experiments_ID = Column(String(100),info={'colanderalchemy': {'description': 'provide ID of any existing related experiments'}})
   

    
class sample(Base):
    __tablename__ = 'sample'

    sample_ID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    descriptive_name = Column(String(45))
    composition = Column(String(45))
    project_ID = Column(INTEGER(6),info={'colanderalchemy': {'exclude': True}})

    #parent
    #state_of_sample = relationship('state_of_sample',uselist=False, back_populates='sample',  info={'colanderalchemy': {'exclude': True}})
    #molecules_in_sample = relationship('molecules_in_sample',uselist=False, back_populates='sample',  info={'colanderalchemy': {'exclude': True}})


class state_of_sample(Base):
    __tablename__ = 'state_of_sample'

    state_of_sample_ID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    state = Column(Enum('gas', 'solid', 'dried film', 'liquid'), nullable=False, info={'colanderalchemy': {'exclude': True}})
    #enter this somehow with a radiobutton or tick box?
    temperature_degrees = Column(INTEGER(11))
    pressure_PSI = Column(INTEGER(11))
    #child 
    sample_ID = Column(Integer, ForeignKey('sample.sample_ID'),  info={'colanderalchemy': {'exclude': True}})

    #sample = relationship('sample', back_populates='state_of_sample',  info={'colanderalchemy': {'exclude': True}})
    #relationship to various states, parent
    #liquid = relationship('liquid', uselist=False, back_populates='state_of_sample',  info={'colanderalchemy': {'exclude': True}})
    #dried_film = relationship('dried_film', uselist=False, back_populates='state_of_sample',  info={'colanderalchemy': {'exclude': True}})
    #solid = relationship('solid', uselist=False, back_populates='state_of_sample',  info={'colanderalchemy': {'exclude': True}})
    #gas = relationship('gas', uselist=False, back_populates='state_of_sample',  info={'colanderalchemy': {'exclude': True}})


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
    #sample = relationship('sample', back_populates='molecules_in_sample',  info={'colanderalchemy': {'exclude': True}})
    #parent to molcules
    #molecule = relationship('molecule',secondary=association_molecule)




class liquid(Base):
    __tablename__ = 'liquid'

  
    pH = Column(Integer)
    solvent = Column(String(45), info={'colanderalchemy': {'description':'name'}})
    atmosphere = Column(String(45),info={'colanderalchemy': {'description': 'psi'}})
    liquid_ID =  Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})


    state_of_sample_ID = Column(Integer, info={'colanderalchemy': {'exclude': True}})
    #state_of_sample = relationship('state_of_sample',back_populates='liquid', info={'colanderalchemy': {'exclude': True}})




class dried_film(Base):
    __tablename__ = 'dried_film'

    atmosphere = Column(String(45))
    volume = Column(String(45), info={'colanderalchemy': {'description': 'mm^3'}})
    area = Column(String(45),info={'colanderalchemy': {'description': 'mm^2'}})
    solvent = Column(String(45), info={'colanderalchemy': {'description': 'name'}})
    pH = Column(String(45), server_default=text("'RANGE(0,14)'"))
    
    dried_film_ID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})


    state_of_sample_ID = Column(Integer, ForeignKey('state_of_sample.state_of_sample_ID'), info={'colanderalchemy': {'exclude': True}})


class gas(Base):
    __tablename__ = 'gas'

    atmosphere = Column(String(45), info={'colanderalchemy': {'description': 'atmosphere in psi'}})
    water_vapour = Column(String(45))
    gasID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})

    state_of_sample_ID = Column(Integer, ForeignKey('state_of_sample.state_of_sample_ID'), info={'colanderalchemy': {'exclude': True}})


class solid(Base):
    __tablename__ = 'solid'

    crystal_form = Column(String(45))
    chemical_formula = Column(String(45))
    solid_ID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})

    state_of_sample_ID = Column(Integer, ForeignKey('state_of_sample.state_of_sample_ID'), info={'colanderalchemy': {'exclude': True}} )



class molecule(Base):
    __tablename__ = 'molecule'

    molecule_name = Column(String(45), nullable=False)
    molecule_type = Column(Enum('protein', 'chemical'))
    molecule_ID = Column(INTEGER(11), primary_key=True, autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    #info={'colanderalchemy': {'widget': 'deform.widget.SelectWidget(values=’chemical’,’protein’)'}}

    #child of molecular composition - doesnt need anything in here as
    #many to many relationship
    #parent of protein,chemical,ligand
    #protein = relationship('protein', uselist=False, back_populates='molecule')
    #chemical = relationship('chemical', uselist=False, back_populates='molecule')
    

#association table for relationship
# get it to fill out association table if molecule is created from the sample page, but dont fill out if molecule is created indendently
association_molecule = Table(
    'association_molecule', metadata,
    Column('mols_in_sample_ID', ForeignKey('molecules_in_sample.molecular_composition_ID'), primary_key=True),
    Column('molecule_ID', ForeignKey('molecule.molecule_ID'), nullable=False, index=True)
)    
    
class protein(Base):
    __tablename__ = 'protein'

    protein_ID = Column(INTEGER(6), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    protein_common_name = Column(String(45))
    alternative_names = Column(String(45))
    source_organism = Column(String(45))
    uniprot_ID = Column(String(45))
    sequence= Column('sequence', String(45), info={'colanderalchemy': {'description': 'Will get to autopoulate using biopython in future'}})
    #source_publications = Column(String(45), info={'colanderalchemy': {'exclude': True}})
    expression_system_or_natural_source = Column(String(45))
    expressed_as = Column(String(45))
    post_translational_modifications = Column(String(100))
    mutation_details = Column(String(100))
    expression_tags = Column(String(100))
    isotopically_labelled = Column(Enum('y', 'n'), default = 'n')
    description_of_labels = Column(String(100), info={'colanderalchemy': {'description': 'if yes'}})
    ligands_present = Column(Enum('y', 'n'), default = 'n')

    #one to one relationshiip with molecule
    # 1 to 1 relationship
    molecule_ID = Column(Integer, nullable=True, info={'colanderalchemy': {'exclude': True}}) 
    #molecule = relationship("molecule", back_populates="protein")


class chemical(Base):
    __tablename__ = 'chemical'

    chemical_ID = Column(INTEGER(11), primary_key=True, nullable=False)
    CAS = Column(String(45))
    smiles_inchi_mol2 = Column('smiles/inchi/mol2', String(45))
    chemical_formula = Column('chemical formula', String(45))
    #one to one relationshiip with molecule
    # 1 to 1 relationship
    molecule_ID = Column(Integer, nullable=True, info={'colanderalchemy': {'exclude': True}}) 
    #molecule = relationship("molecule", back_populates="chemical")

class experiment(Base):
    __tablename__ = 'experiment'

    experiment_ID =Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    experiment_description = Column(String(100))
    #experiemntal conditions parent
    #experimental_conditions_ID = relationship('experimental_conditions',uselist=False, back_populates='experiment', info={'colanderalchemy': {'exclude': True}})
    #need to add samples relationship here
    related_samples = Column(String(100), info={'colanderalchemy': {'description': 'Any related samples ID or these can be added'}})
    #data_aquisition_ID = Column(INTEGER(11), nullable=True, ForeignKey('data_aquisition.data_aq_ID'),info={'colanderalchemy': {'exclude': True}})
    
    
    #spectrometer_ID = Column(INTEGER(11),ForeignKey('spectrometer.spectrometer_ID'), nullable=True, info={'colanderalchemy': {'exclude': True}})
    #parent to despsitor,publication and spectrum
    # enter this automatically base on user logged in
    depositor_ID = Column(ForeignKey('depositor.depositor_ID'), info={'colanderalchemy': {'exclude': True}})
    #depositor = relationship('depositor', info={'colanderalchemy': {'exclude': True}})
    
    
    publication_ID = Column(INTEGER(11), ForeignKey('publication.publication_ID'), info={'colanderalchemy': {'exclude': True}})
    #publication = relationship('publication', secondary='exp_has_publication', info={'colanderalchemy': {'exclude': True}})
    #child of project, spectrum,
    #spectrometer = relationship('spectrometer', back_populates='experiment', info={'colanderalchemy': {'exclude': True}})
    #need to add project relationship here
        #association tables 4 publication and project
    #may also need a sample association table

# get forms to automatically fill out    
exp_has_publication = Table(
	'exp_has_publication', metadata,
	Column('publication_ID', ForeignKey('publication.publication_ID'), nullable=False, index=True),
    	Column('experiment_ID', ForeignKey('experiment.experiment_ID'), nullable=False, index=True)
)

project_has_experiment = Table(
    'project_has_experiment', metadata,
    Column('project_ID', ForeignKey('project.project_ID'), index=True),
    Column('experiment_ID', ForeignKey('experiment.experiment_ID'), primary_key=True)
)


class experimental_conditions(Base):
    __tablename__ = 'experimental_conditions'

    experimental_conditions_ID =Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    
    phase = Column(String(45), nullable=True)
    temperature = Column(String(45), nullable=True, info={'colanderalchemy': {'description': 'degrees centigrade'}})
    pressure = Column(String(45), nullable=True , info={'colanderalchemy': {'description': 'psi'}})
    #child of experiment one to one
    experiment_ID = Column(INTEGER(4), info={'colanderalchemy': {'exclude': True}})
    #experiment_ID = Column(ForeignKey('experiment.experiment_ID'), info={'colanderalchemy': {'exclude': True}})
    #experiment = relationship('experiment',back_populates='experimental_conditions')
    
    
    


class data_aquisition(Base):
    __tablename__ = 'data_aquisition'

    data_aq_ID =Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    
    number_of_sample_scans = Column(INTEGER(11), nullable=True)
    number_of_background_scans = Column(INTEGER(11), nullable=True)
    scanner_velocity_KHz = Column(INTEGER(11), nullable=True, default = 0)
    resolution = Column(INTEGER(11), nullable=True, default = 0)
    start_frequency = Column(INTEGER(11), nullable=True, default = 0)
    end_frequency = Column(INTEGER(11), nullable=True, default = 0)
    optical_filter = Column(Enum('yes', 'no'), default='no')
    higher_range = Column('higher_range_(cm-1)', INTEGER(11), info={'colanderalchemy': {'description': 'cm^-1'}}) # spelling mistake,exclude for now
    lower_range = Column('lower_range_(cm-1)', INTEGER(11), info={'colanderalchemy': {'description': 'cm^-1'}}) #spelling mistake, exclude for now
    #child of experiment
    #higher_range__cm_1_
    experiment_ID = Column(INTEGER(11),info={'colanderalchemy': {'description': 'struggling to model as a foreign key so for now just fill in corresponding experiment number but fix this later'}})    #experiment = relationship('experiment',back_populates='data_aquisition')
    
class spectrometer(Base):
    __tablename__ = 'spectrometer'

    spectrometer_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    instrument_manufacturer = Column(String(45))
    instrument_model = Column(String(45))
    light_source = Column(Enum('globar', 'laser', 'synchrotron', 'other'), default = 'globar',nullable=True )
    beamsplitter = Column(Enum('KBr', 'Mylar'), default='KBr',nullable=True)
    detector__type = Column('detector_ type', Enum('DTGS', 'MCT Broad band', 'MCT narrow band', 'other'), default='other', nullable=True)
    optics = Column(Enum('vacuum', 'purged', 'dry', 'atmospheric'), default='dry',nullable=True)
    type_of_recording = Column(Enum('fourier transform', 'dispersive', 'tunable laser'),  default = 'fourier transform',nullable=True)
    mode_of_recording = Column(Enum('transmission', 'ATR', 'transflectance', 'diffuse reflection'), default='transmission',nullable=True)
    #denormalising it
    experiment_ID = Column(INTEGER(11), ForeignKey(experiment.experiment_ID), nullable=True , info={'colanderalchemy': {'exclude': True}})
   
    
    #parent of experiment
    #experiment_ID = Column(ForeignKey('experiment.experiment_ID'))
    #parents of not_atr, atr and translfectance/diffuse - 1 to 1
    #not_atr= relationship("not_atr",uselist=False, back_populates="spectrometer")
    #atr= relationship("atr",uselist=False, back_populates="spectrometer")
    #transflectance_diffuse = relationship("transflectance_diffuse",uselist=False, back_populates="spectrometer")
    
    
class depositor(Base):
    __tablename__ = 'depositor'

    depositor_ID = Column(INTEGER(11), primary_key=True, unique=True)
    depositor_name = Column(String(45), nullable=False)
    institution = Column(String(45))
    country = Column(String(45))
    principle_investigator = Column(String(45))
    deposition_date = Column(Date)

    #currently child of experiment but perhaps should be the other way round

class publication(Base):
    __tablename__ = 'publication'

    publication_ID = Column(INTEGER(11), primary_key=True)
    publication_name = Column(String(45), nullable=False)
    authors = Column('author', String(100), nullable=False)
    link = Column(String(100))
    #currently child of experiment but perhaps should be the other way round


    

class not_atr(Base):
    __tablename__ = 'not_atr'

    
    not_atr_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    sample_window_material = Column(Enum('CaF2', 'BaF2', 'ZnSe', 'ZnS', 'CdTe', 'KBr', 'KRS-5', 'other'), default='CaF2')
    pathlength__if_known_ = Column('pathlength (if known)', INTEGER(11))
    multi_well_plate = Column('multi-well_plate', Enum('y', 'n'), default = 'y')
    product_code = Column('if yes - product code', String(45))
    #child of spectrometer
    spectrometer_ID = Column(INTEGER(11),info={'colanderalchemy': {'exclude': True}})
    #spectrometer = relationship("spectrometer",back_populates='not_atr')
                                                     
class atr(Base):
    __tablename__ = 'atr'

    atr_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})
    prism_size_mm = Column(INTEGER(11),nullable=True, default= 0 )
    number_of_reflections = Column(INTEGER(11),nullable=True, default = 0)
    prism_material = Column(Enum('Diamond', 'Ge', 'Si', 'KRS-5', 'ZnS', 'ZnSe'), default='Diamond', nullable=True)
    
    angle_of_incidence_degrees = Column(INTEGER(11),nullable=True, default = 0)
      #child of spectrometer
    spectrometer_ID = Column(INTEGER(11),info={'colanderalchemy': {'exclude': True}})
    #spectrometer = relationship("spectrometer",back_populates='atr')

class transflectance_diffuse(Base):
    __tablename__ = 'transf_diffuse'
    trans_diff_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})

    reflectance_device = Column(String(45), nullable=True)
    slide_material = Column(String(45),nullable=True)
    angle_of_incidence = Column(String(45),nullable=True,info={'colanderalchemy': {'description': 'In degrees'}})
    #child of spectrometer
    spectrometer_ID = Column(INTEGER(11),info={'colanderalchemy': {'exclude': True}})
    #spectrometer = relationship("spectrometer",back_populates='transflectance_diffuse')

#spectra


class spectra(Base):
    __tablename__ = 'spectra'

    spectra_ID= Column(INTEGER(11), primary_key=True, info={'colanderalchemy': {'exclude': True}})
    #add a spectra description here
    spectra_type = Column(Enum('sample power', 'background power spectrum', 'initial result spectrum'), nullable=True)
    format = Column(Enum('absorbance', 'transmittance', 'reflectance', 'log reflectance', 'kubelka munk', 'ATR spectrum', 'pas spectrum'), nullable=True)
    #child of experiment

    #can't get foreign key to work atm 
    experiment_ID = Column(Integer,nullable=True)
    
    
    



class ft_processing(Base):
    __tablename__ = 'ft_processing'
    ft_processing_ID = Column(INTEGER(11), primary_key=True, info={'colanderalchemy': {'exclude': True}})
    apodization__function = Column('apodization_ function', Enum('Blackman-Harris 3-Term', 'Blackman-Harris 5-Term', 'Norton-Beer,weak', 'Norton-Beer,medium', 'Norton-Beer,strong', 'Boxcar', 'Triangular', 'Four point', 'other'))
    zero_filling_factor = Column(INTEGER(11))
    non_linearity_correction = Column(Enum('yes', 'no'))
    phase_correction_mode = Column(Enum('Mertz', 'Mertz signed', 'Power spectrum', 'Mertz no peak search', 'Mertz signed no peak search', 'Power spectrum no peak search'))
    phase_resolution = Column(INTEGER(11))
    #child of experiment - but maybe should be parent?
    experiment_ID = Column(ForeignKey('experiment.experiment_ID'))


class post_processing_and_deposited_spectra(Base):
    __tablename__ = 'post_processing_and_deposited_spectra'

    sample_power_spectrum = Column(String(45), info={'colanderalchemy': {'exclude':True}})
    #deform.widget.FileUploadWidget(tmpstore)
    background_power_spectrum = Column(String(45), info={'colanderalchemy': {'exclude':True}})
    initial_result_spectrum = Column(String(45), info={'colanderalchemy': {'exclude':True}})
    initial_result_spectrum_format = Column('initial result spectrum format', Enum('Blackman-Harris 3-Term', 'Blackman-Harris 5-Term', 'Norton-Beer,weak', 'Norton-Beer,medium', 'Norton-Beer,strong', 'Boxcar', 'Triangular', 'Four point', 'other'), nullable=True)
    water_vapour = Column('water vapour', String(45))
    solvent = Column(String(45))
    solution_composition_item_1 = Column(String(45))
    solution_composition_item_2 = Column(String(45))
    other = Column(String(45))
    baseline_correction = Column(String(45))
    scaling = Column(String(45))
    second_derivative = Column('2nd_derivative', Enum('y', 'n'), default = 'n')
    method = Column(String(45))
    window_point_size_smoothing = Column('window_point_size/smoothing', String(45))
    final_published_spectrum = Column(String(45))
    final_published_spectrum_format = Column(Enum('absorbance', 'transmittance', 'reflectance', 'log reflectance', 'Kubelka Munk', 'ATR spectrum', 'PAS spectrum'), default='absorbance')
    smoothing_method = Column(String(45))
    smoothing_parameters = Column(String(45))
    spectra_ID = Column(Integer, index=True)
    PPandD_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, info={'colanderalchemy': {'exclude': True}})




class FTIRModel(Base):
    """ This class is to create the main FTIRModel table with SQL alchemy """
    __tablename__ = 'FTIRModel'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    data = Column(Text, nullable=False)
    magic = Column(Text, nullable=False)
    
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='created_pages')

