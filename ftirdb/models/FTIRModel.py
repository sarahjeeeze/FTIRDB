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

class sample(Base):
    __tablename__ = 'sample'

    sample_ID = Column(INTEGER(11), primary_key=True, info={'colanderalchemy': {'exclude': True}})
    descriptive_name = Column(String(45))
    composition = Column(String(45))
    molecular_composition_ID = Column(ForeignKey('molecular_composition.molecular_composition_ID'), nullable=False, index=True)

    molecular_composition = relationship('molecular_composition')


class atr(Base):
    __tablename__ = 'atr'

    spectrometer_ID = Column(INTEGER(11), primary_key=True, info={'colanderalchemy': {'exclude': True}})
    prism_size_mm = Column(INTEGER(11))
    number_of_reflections = Column(INTEGER(11))
    prism_material = Column(Enum('Diamond', 'Ge', 'Si', 'KRS-5', 'ZnS', 'ZnSe'), server_default=text("'Diamond'"))
    angle_of_incidence_degrees = Column(INTEGER(11))


class depositor(Base):
    __tablename__ = 'depositor'

    depositor_ID = Column(INTEGER(11), primary_key=True, unique=True)
    depositor_name = Column(String(45), nullable=False)
    institution = Column(String(45))
    country = Column(String(45))
    principle_investigator = Column(String(45))
    deposition_date = Column(Date)


class fourier_transform_processing(Base):
    __tablename__ = 'fourier_transform_processing'

    experiment_ID = Column(INTEGER(11), primary_key=True)
    apodization__function = Column('apodization_ function', Enum('Blackman-Harris 3-Term', 'Blackman-Harris 5-Term', 'Norton-Beer,weak', 'Norton-Beer,medium', 'Norton-Beer,strong', 'Boxcar', 'Triangular', 'Four point', 'other'))
    zero_filling_factor = Column(INTEGER(11))
    non_linearity_correction = Column(Enum('yes', 'no'))
    phase_correction_mode = Column(Enum('Mertz', 'Mertz signed', 'Power spectrum', 'Mertz no peak search', 'Mertz signed no peak search', 'Power spectrum no peak search'))
    phase_resolution = Column(INTEGER(11))


class liquid(Base):
    __tablename__ = 'liquid'

    solution_composition = Column(String(100), nullable=False)
    pH = Column(String(45))
    concentration = Column(String(45))
    solvent = Column(String(45))
    atmosphere = Column(String(45))
    sample_ID = Column(INTEGER(11), primary_key=True)


class state_of_sample(liquid):
    __tablename__ = 'state_of_sample'

    state = Column(Enum('gas', 'solid', 'dried film', 'liquid'), nullable=False)
    sample_ID = Column(ForeignKey('liquid.sample_ID'), ForeignKey('sample.sample_ID'), primary_key=True, index=True)
    temperature_degrees = Column(INTEGER(11))
    pressure_PSI = Column(INTEGER(11))

    sample = relationship('sample', uselist=False)


class dried_film(state_of_sample):
    __tablename__ = 'dried_film'

    atmosphere = Column(String(45))
    solution__composition = Column('solution_ composition', String(45))
    concentration = Column(String(45))
    volume = Column(String(45))
    area = Column(String(45))
    solvent = Column(String(45))
    pH = Column(String(45), server_default=text("'RANGE(0,14)'"))
    sample_ID = Column(ForeignKey('state_of_sample.sample_ID'), primary_key=True, index=True)


class gas(state_of_sample):
    __tablename__ = 'gas'

    atmosphere = Column(String(45))
    water_vapour = Column(String(45))
    state_of_sample_sample_ID = Column(ForeignKey('state_of_sample.sample_ID'), primary_key=True, index=True)


class solid(state_of_sample):
    __tablename__ = 'solid'

    crystal_form = Column(String(45))
    chemical_formula = Column(String(45))
    sample_ID = Column(ForeignKey('state_of_sample.sample_ID'), primary_key=True, index=True)


class molecular_composition(Base):
    __tablename__ = 'molecular_composition'

    molecular_composition_ID = Column(INTEGER(11), primary_key=True)
    molecular_composition_description = Column(String(45))

    molecule = relationship('molecule', secondary='molecule_has_molecular_composition')


class molecule(Base):
    __tablename__ = 'molecule'

    molecule_name = Column(String(45), nullable=False)
    molecule_type = Column(Enum('protein', 'chemical'))
    molecule_ID = Column(INTEGER(11), primary_key=True)


class not_atr(Base):
    __tablename__ = 'not_atr'

    spectrometer_ID = Column(INTEGER(11), primary_key=True)
    sample_window_material = Column(Enum('CaF2', 'BaF2', 'ZnSe', 'ZnS', 'CdTe', 'KBr', 'KRS-5', 'other'), server_default=text("'CaF2'"))
    pathlength__if_known_ = Column('pathlength (if known)', INTEGER(11))
    multi_well_plate = Column('multi-well_plate', Enum('y', 'n'))
    if_yes___product_code = Column('if yes - product code', String(45))


class spectrometer(not_atr):
    __tablename__ = 'spectrometer'

    spectrometer_ID = Column(ForeignKey('not_atr.spectrometer_ID'), ForeignKey('atr.spectrometer_ID'), primary_key=True)
    instrument_manufacturer = Column(String(45))
    instrument_model = Column(String(45))
    light_source = Column(Enum('globar', 'laser', 'synchrotron', 'other'), server_default=text("'globar'"))
    beamsplitter = Column(Enum('KBr', 'Mylar'), server_default=text("'KBr'"))
    detector__type = Column('detector_ type', Enum('DTGS', 'MCT Broad band', 'MCT narrow band', 'other'), server_default=text("'DTGS'"))
    optics = Column(Enum('vacuum', 'purged', 'dry', 'atmospheric'), server_default=text("'vacuum'"))
    type_of_recording = Column(Enum('fourier transform', 'dispersive', 'tunable laser'), server_default=text("'fourier transform'"))
    mode_of_recording = Column(Enum('transmission', 'ATR', 'transflectance', 'diffuse reflection'), server_default=text("'transmission'"))

    
    atr = relationship('atr', uselist=False)


class project(Base):
    __tablename__ = 'project'

    descriptive_name = Column(String(300))
    project_ID = Column(INTEGER(4), primary_key=True, unique=True,  autoincrement=True, default=0, info={'colanderalchemy': {'exclude': True}})
    related_experiments_ID = Column(String(100))


class publication(Base):
    __tablename__ = 'publication'

    publication_ID = Column(INTEGER(11), primary_key=True)
    publication_name = Column(String(45), nullable=False)
    author_s_ = Column('author(s)', String(100), nullable=False)
    link = Column(String(100))



class chemicals(Base):
    __tablename__ = 'chemicals'

    chemical_ID = Column(INTEGER(11), primary_key=True, nullable=False)
    CAS = Column(String(45))
    smiles_inchi_mol2 = Column('smiles/inchi/mol2', String(45))
    chemical_formula = Column('chemical formula', String(45))
    molecule_ID = Column(ForeignKey('molecule.molecule_ID'), primary_key=True, nullable=False, index=True)

    molecule = relationship('molecule')


class data_aquisition(Base):
    __tablename__ = 'data_aquisition'

    experiment_ID = Column(INTEGER(11), primary_key=True)
    number_of_sample_scans = Column(INTEGER(11))
    number_of_background_scans = Column(INTEGER(11))
    scanner_velocity_KHz = Column(INTEGER(11))
    resolution = Column(INTEGER(11))
    start_frequency = Column(INTEGER(11))
    end_frequency = Column(INTEGER(11))
    optical_filter = Column(Enum('yes', 'no'))
    higher_range__cm_1_ = Column('higher_range_(cm-1)', INTEGER(11))
    lower_range__cm_1_ = Column('lower_range_(cm-1)', INTEGER(11))
    Fourier_transform_processing_FTIRDBID = Column('Fourier transform processing_FTIRDBID', ForeignKey('fourier_transform_processing.experiment_ID'), nullable=False, index=True)

    fourier_transform_processing = relationship('fourier_transform_processing')


class experiment(data_aquisition):
    __tablename__ = 'experiment'

    experiment_ID = Column(ForeignKey('data_aquisition.experiment_ID'), primary_key=True)
    experiment_description = Column(String(100))
    related_samples = Column(String(100))
    spectrometer_type_ID = Column(INTEGER(11))
    depositor_ID = Column(ForeignKey('depositor.depositor_ID'), index=True)
    spectrometer_ID = Column(ForeignKey('spectrometer.spectrometer_ID'), index=True)

    depositor = relationship('depositor')
    spectrometer = relationship('spectrometer')
    project = relationship('project', secondary='project_has_experiment')
    publication = relationship('publication', secondary='publication_has_experiment')


class experimental_conditions(experiment):
    __tablename__ = 'experimental_conditions'

    experiment_ID = Column(ForeignKey('experiment.experiment_ID'), primary_key=True)
    phase = Column(String(45))
    temperatue = Column(String(45))
    pressure = Column(String(45))


t_molecule_has_molecular_composition = Table(
    'molecule_has_molecular_composition', metadata,
    Column('molecular_composition_ID', ForeignKey('molecular_composition.molecular_composition_ID'), primary_key=True),
    Column('molecule_ID', ForeignKey('molecule.molecule_ID'), nullable=False, index=True)
)


class protein(Base):
    __tablename__ = 'protein'

    protein_ID = Column(INTEGER(11), primary_key=True, nullable=False)
    protein_common_name = Column(String(45))
    alternative_names = Column(String(45))
    source_organism = Column(String(45))
    uniprot_ID = Column(String(45))
    sequence__use_biopython_ = Column('sequence (use biopython)', String(45))
    source__publications_ = Column('source (publications)', String(45))
    expression_system_or_natural_source = Column(String(45))
    expressed_as = Column(String(45))
    post_translational_modifications = Column(String(100))
    mutation_details = Column(String(100))
    expression_tags = Column(String(100))
    isotopically_labelled = Column(Enum('y', 'n'))
    description_of_labels = Column(String(100))
    ligands_present = Column(Enum('y', 'n'))
    concentration_or_ratio = Column(String(100))
    molecule_ID = Column(ForeignKey('molecule.molecule_ID'), primary_key=True, nullable=False, index=True)

    molecule = relationship('molecule')





t_project_has_experiment = Table(
    'project_has_experiment', metadata,
    Column('project_ID', ForeignKey('project.project_ID'), index=True),
    Column('experiment_ID', ForeignKey('experiment.experiment_ID'), primary_key=True)
)


t_publication_has_experiment = Table(
    'publication_has_experiment', metadata,
    Column('publication_ID', ForeignKey('publication.publication_ID'), nullable=False, index=True),
    Column('experiment_ID', ForeignKey('experiment.experiment_ID'), nullable=False, index=True)
)


class spectra(Base):
    __tablename__ = 'spectra'

    spectra_ID = Column(INTEGER(11), primary_key=True, nullable=False)
    spectra_type = Column(Enum('sample power', 'background power spectrum', 'initial result spectrum'))
    format = Column(Enum('absorbance', 'transmittance', 'reflectance', 'log reflectance', 'kubelka munk', 'ATR spectrum', 'pas spectrum'))
    experiment_ID = Column(ForeignKey('experiment.experiment_ID'), primary_key=True, nullable=False, index=True)

    experiment = relationship('experiment')


class post_processing_and_deposited_spectra(spectra):
    __tablename__ = 'post_processing_and_deposited_spectra'

    sample_power_spectrum = Column(String(45))
    background_power_spectrum = Column(String(45))
    initial_result_spectrum = Column(String(45))
    initial_result_spectrum_format = Column('initial result spectrum format', Enum('Blackman-Harris 3-Term', 'Blackman-Harris 5-Term', 'Norton-Beer,weak', 'Norton-Beer,medium', 'Norton-Beer,strong', 'Boxcar', 'Triangular', 'Four point', 'other'))
    water_vapour = Column('water vapour', String(45))
    solvent = Column(String(45))
    solution_composition_item_1 = Column(String(45))
    solution_composition_item_2 = Column(String(45))
    other = Column(String(45))
    baseline_correction = Column(String(45))
    scaling = Column(String(45))
    _2nd_derivative = Column('2nd_derivative', Enum('y', 'n'))
    method = Column(String(45))
    window_point_size_smoothing = Column('window_point_size/smoothing', String(45))
    final_published_spectrum = Column(String(45))
    final_published_spectrum_format = Column(Enum('absorbance', 'transmittance', 'reflectance', 'log reflectance', 'Kubelka Munk', 'ATR spectrum', 'PAS spectrum'))
    smoothing_method = Column(String(45))
    smooth_parameters = Column(String(45))
    spectra_ID = Column(ForeignKey('spectra.spectra_ID'), primary_key=True, index=True)
    post_processing_and_deposited_spectracol = Column(String(45))
class FTIRModel(Base):
    """ This class is to create the main FTIRModel table with SQL alchemy """
    __tablename__ = 'FTIRModel'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    data = Column(Text, nullable=False)
    magic = Column(Text, nullable=False)
    
    #creator_id = Column(, ForeignKey('users.id'), nullable=False)
    #creator = relationship('User', backref='created_pages')

