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

from ..models import sample, state_of_sample, molecules_in_sample, liquid, gas, solid, dried_film




@view_config(route_name='sampleForm', renderer='../templates/sampleForm.jinja2')
def sampleForm(request):
    
    """ project form page """

            
    class Liquid(colander.Schema):
        setup_schema(None,liquid)
        liquidschema = liquid.__colanderalchemy__

    class Sample(colander.MappingSchema):
        setup_schema(None,sample)
        sampleschema =sample.__colanderalchemy__
        setup_schema(None,molecules_in_sample)
        molecules_in_sample_schema =molecules_in_sample.__colanderalchemy__
        setup_schema(None,state_of_sample)
        state_of_sample_schema =state_of_sample.__colanderalchemy__
        setup_schema(None,liquid)
        #for now include all of the states as not sure how to add them. Sequence doesnt seem to work
        liquid_schema =liquid.__colanderalchemy__
        setup_schema(None,solid)
        solid_schema =solid.__colanderalchemy__
        setup_schema(None,gas)
        gas_schema =gas.__colanderalchemy__
        setup_schema(None,liquid)
        liquid_schema =liquid.__colanderalchemy__
        
          
        
    form = Sample()
    form = deform.Form(form,buttons=('submit',))

    
    if 'submit' in request.POST:
        descriptive_name= request.params['descriptive_name']
        composition= request.params['composition']
        descriptive_name = request.params['descriptive_name']
        molecule_1_name = request.params['molecule_1_name']
        concentration_1 = request.params['concentration_1']
        molecule_2_name = request.params['molecule_2_name']
        concentration_2 = request.params['concentration_2']
        molecule_3_name = request.params['molecule_3_name']
        concentration_3 = request.params['concentration_3']
        molecule_4_name = request.params['molecule_4_name']
        concentration_4 = request.params['concentration_4']
        
        
        
  
        #map columns
        controls = request.POST.items()
        print(request.params)
        print(request.POST)
        #format for db input - descriptive_name = request.params['descriptive_name']
        
        
        try:
                appstruct = form.validate(controls)
                page = sample(descriptive_name=descriptive_name,composition=composition)#call validate
                request.dbsession.add(page)
                page = molecules_in_sample(descriptive_name=descriptive_name,molecule_4_name=molecule_4_name,
                                           molecule_3_name=molecule_3_name,molecule_2_name=molecule_2_name,
                                           molecule_1_name=molecule_1_name,concentration_1=concentration_1,
                                           concentration_2=concentration_2,concentration_3=concentration_3,
                                           concentration_4=concentration_4,sample_ID=4)
                
                sample_id = request.dbsession.query(sample).filter_by(composition=composition).first()
                sample_id = sample_id.sample_ID
                
                next_url = request.route_url('samplePage', samplename=sample_id)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'sampleForm':e.render()}
           

        
    
    else:
    
        sampleForm = form.render()
        return{'sampleForm':sampleForm}
@view_config(route_name='sampleForm2', renderer='../templates/sampleForm2.jinja2')
def sampleForm2(request):
    
    """ project form page """

  
            
    class Liquid(colander.Schema):
        setup_schema(None,liquid)
        liquidschema = liquid.__colanderalchemy__

    class Sample(colander.MappingSchema):
        setup_schema(None,sample)
        sampleschema =sample.__colanderalchemy__
        setup_schema(None,molecules_in_sample)
        molecules_in_sample_schema =molecules_in_sample.__colanderalchemy__
        setup_schema(None,state_of_sample)
        state_of_sample_schema =state_of_sample.__colanderalchemy__
        setup_schema(None,liquid)
        #for now include all of the states as not sure how to add them. Sequence doesnt seem to work
        liquid_schema =liquid.__colanderalchemy__
        setup_schema(None,solid)
        solid_schema =solid.__colanderalchemy__
        setup_schema(None,gas)
        gas_schema =gas.__colanderalchemy__
        setup_schema(None,liquid)
        liquid_schema =liquid.__colanderalchemy__
        
    

        
        
    form = Sample()
    form = deform.Form(form,buttons=('submit',))

    



    if 'submit' in request.POST:
        descriptive_name= request.params['descriptive_name']
        composition= request.params['composition']
        descriptive_name = request.params['descriptive_name']
        molecule_1_name = request.params['molecule_1_name']
        concentration_1 = request.params['concentration_1']
        molecule_2_name = request.params['molecule_2_name']
        concentration_2 = request.params['concentration_2']
        molecule_3_name = request.params['molecule_3_name']
        concentration_3 = request.params['concentration_3']
        molecule_4_name = request.params['molecule_4_name']
        concentration_4 = request.params['concentration_4']
        
        
        
  
        #map columns
        controls = request.POST.items()
        print(request.params)
        print(request.POST)
        #format for db input - descriptive_name = request.params['descriptive_name']
        
        
        try:
                appstruct = form.validate(controls)
                page = sample(descriptive_name=descriptive_name,composition=composition)#call validate
                request.dbsession.add(page)
                page = molecules_in_sample(descriptive_name=descriptive_name,molecule_4_name=molecule_4_name,
                                           molecule_3_name=molecule_3_name,molecule_2_name=molecule_2_name,
                                           molecule_1_name=molecule_1_name,concentration_1=concentration_1,
                                           concentration_2=concentration_2,concentration_3=concentration_3,
                                           concentration_4=concentration_4,sample_ID=4)
                
                sample_id = request.dbsession.query(sample).filter_by(composition=composition).first()
                sample_id = sample_id.sample_ID
                
                next_url = request.route_url('samplePage', samplename=sample_id)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'sampleForm':e.render()}
           

        
    
    else:
    
        sampleForm = form.render()
        return{'sampleForm':sampleForm}
    
@view_config(route_name='samplePage', renderer='../templates/samplePage.jinja2')

def samplePage(request):

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
        search = request.matchdict['samplename']
    #search = request.params['body']
        searchdb = request.dbsession.query(sample).filter_by(sample_ID=search).all()
        dic = {}
    #return the dictionary of all values from the row
        for u in searchdb:
            new = u.__dict__
            dic.update( new )
    
    #need to work on display of this 
        return {'samplePage': dic}
    
    
