"""

Project: FTIRDB
File: views/graph.py

Version: v1.0
Date: 10.09.2018
Function: provides functions required for addAccount view

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:

Contains functions required for viewing graphs based on jcamp files



============


"""
from pyramid.compat import escape
import re
from docutils.core import publish_parts
import matplotlib.pyplot as plt
from jcamp import JCAMP_reader, JCAMP_calc_xsec
import colander 
import deform
import peppercorn
import requests
from deform import Form, FileData
import os
#imppot sqlalchemy 
from sqlalchemy import event
from sqlalchemy import *
from sqlalchemy.databases import mysql
from sqlalchemy.orm import relation, backref, synonym
from sqlalchemy.orm.exc import NoResultFound
import colanderalchemy
from colanderalchemy import setup_schema


import numpy as np

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.response import Response
import deform
import colander
from deform import widget

from ..models import sample, state_of_sample, molecules_in_sample, liquid, gas, solid, dried_film, molecule, protein, chemical




@view_config(route_name='moleculeForm', renderer='../templates/moleculeForm.jinja2')
def moleForm(request):
    
    """ project form page """

   
        
    class All(colander.MappingSchema):
        setup_schema(None,molecule)
        moleculeschema=molecule.__colanderalchemy__
        #protein = proteins(widget=deform.widget.SequenceWidget(orderable=True))

        
        
    form = All()
    print(form)
    #reqts = form['form1']['form'].get_widget_resources()
    form = deform.Form(form,buttons=('submit',))

    



    if 'submit' in request.POST:
              
        
  
        #map columns
        controls = request.POST.items()
        print(request.params)
        print(request.POST)
        #molecule
        molecule_name= request.params['molecule_name']
        molecule_type= request.params['molecule_type']
        
        #protein
        protein_ID= request.params['protein_ID']
        protein_common_name= request.params['protein_common_name']
        alternative_names= request.params['alternative_names']
        source_organism= request.params['source_organism']
        uniprot_ID= request.params['uniprot_ID']
        sequence= request.params['sequence']
        #source_publications= request.params['source_publications']
        expression_system_or_natural_source= request.params['expression_system_or_natural_source']
        expressed_as= request.params['expressed_as']
        post_translational_modifications= request.params['post_translational_modifications']
        #mutation_details_expression_tages_isotopically_labelled= request.params['mutation_details_expression_tages_isotopically_labelled']
        description_of_labels= request.params['description_of_labels']
        ligands_present= request.params['ligands_present']
        concentration_or_ratio= request.params['concentration_or_ratio']
        #chem
        chemical_ID= request.params['chemical_ID']
        CAS= request.params['CAS']
        smiles_inchi_mol2= request.params['smiles_inchi_mol2']
        chemical_formula= request.params['chemical_formula']
                 
                #format for db input - descriptive_name = request.params['descriptive_name']
        
        
        try:
                appstruct = form.validate(controls)


                
                page = molecule(molecule_name=molecule_name, molecule_type=molecule_type)
                request.dbsession.add(page)
                page = chemical(chemical_ID=chemical_ID, CAS=CAS, smiles_inchi_mol2=smiles_inchi_mol2, chemical_formula=chemical_formula)
                request.dbsession.add(page)
                
                page =protein(protein_ID=protein_ID, protein_common_name=protein_common_name, alternative_names=alternative_names,
                source_organism=source_organism, uniprot_ID=uniprot_ID, sequence=sequence,
                expression_system_or_natural_source= expression_system_or_natural_source, expressed_as=expressed_as,
                post_translational_modifications=post_translational_modifications,
                description_of_labels=description_of_labels, ligands_present=ligands_present, concentration_or_ratio=concentration_or_ratio)
                request.dbsession.add(page)
                
                
                molecule_id = request.dbsession.query(molecule).filter_by(molecule_name=molecule_name).first()
                molecule_id = molecule_id.molecule_ID
                
                next_url = request.route_url('moleculePage', molecule=molecule_id)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'sampleForm':e.render()}
           

        
    
    else:
        
        sampleForm = form.render()
        return{'sampleForm':sampleForm}
    
@view_config(route_name='moleculePage', renderer='../templates/moleculePage.jinja2')

def moleculePage(request):

    """This page takes a project with project_ID in the URL and returns a page with a dictionary of
all the values, it also contains buttons for adding samples and experiments. When page is linked from here
the child/parent relationship is created"""

    if 'form.submitted' in request.params:
        if 'form.submitted' == 'sample':
            
            return {'projectForm': 'sample'}
        else:
            return {'projectForm': 'experiment'}
            
        #next_url = request.route_url('projectPage', pagename=4)
        #return HTTPFound(location=next_url)
        
        
        
    else:
        print(request)
        search = request.matchdict['molecule']
    #search = request.params['body']
        searchdb = request.dbsession.query(molecule).filter_by(molecule_ID=search).all()
        dic = {}
    #return the dictionary of all values from the row
        for u in searchdb:
            new = u.__dict__
            dic.update( new )
    
    #need to work on display of this 
        return {'samplePage': dic}
    
    
