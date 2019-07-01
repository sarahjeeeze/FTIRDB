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

from ..models import FTIRModel, dried_film, data_aquisition, experimental_conditions, project_has_experiment, exp_has_publication, experiment, gas, molecule, protein, chemical, liquid, project, molecules_in_sample, sample, solid, state_of_sample


# regular expression used to find WikiWords



@view_config(route_name='experimentForm', renderer='../templates/experimentForm.jinja2')
def experimentForm(request):
    
    """ project form page """
    class All(colander.MappingSchema):
        setup_schema(None,experiment)
        experimentSchema=experiment.__colanderalchemy__
        setup_schema(None,experimental_conditions)
        conditionsSchema=experimental_conditions.__colanderalchemy__
        setup_schema(None,data_aquisition)
        data_aquisition_Schema=data_aquisition.__colanderalchemy__
        
        
        


    tables = All()
    form = deform.Form(tables,buttons=('submit',))
        
    
    if 'submit' in request.POST:
        #map columns
        controls = request.POST.items()


        controls = request.POST.items()     #call validate
        pstruct = peppercorn.parse(controls)
        print(pstruct)
        

        try:



                appstruct = form.validate(controls)
                
                exp = pstruct['experimentSchema'] # try to add to database
                print(exp)
                page = experiment(**exp)
                request.dbsession.add(page)
                experiment_description= request.params['experiment_description'] #link experiment column to related foreign keys
                experiment_id = request.dbsession.query(experiment).filter_by(experiment_description=experiment_description).first()
                experiment_id = experiment_id.experiment_ID
                experimemtal_cond = pstruct['conditionsSchema']
                page = experimental_conditions(experiment_ID=experiment_id, **experimental_cond)
                request.dbsession.add(page)
                
                page = data_aquisition(number_of_sample_scans=number_of_sample_scans, scanner_velocity_KHz=scanner_velocity_KHz,
                                       resolution=resolution, start_frequency=start_frequency,
                                       end_frequency=end_frequency, optical_filter=optical_filter)
                request.dbsession.add(page)
                experiment_id = request.dbsession.query(experiment).filter_by(experiment_description=experiment_description).first()
                experiment_id = experiment_id.experiment_ID
                next_url = request.route_url('experimentPage', experiment=experiment_id)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'experimentForm':e.render()}
           

        
    
    else:
        experimentForm = form.render()
        return{'experimentForm':experimentForm}
    
@view_config(route_name='experimentPage', renderer='../templates/experimentPage.jinja2')

def experimentPage(request):

    """This page takes a project with project_ID in the URL and returns a page with a dictionary of
all the values, it also contains buttons for adding samples and experiments. When page is linked from here
the child/parent relationship is created"""

    if 'form.submitted' in request.params:
        if request.params['form.submitted'] == 'sample':
            #retrieve project ID and send to sample page
         return {'projectForm': 'sample'}
        else:
            return {'projectForm': 'experiment'}
            
        #next_url = request.route_url('projectPage', pagename=4)
        #return HTTPFound(location=next_url)
        
        
        
    else:
        search = request.matchdict['experiment']
    #search = request.params['body']
        searchdb = request.dbsession.query(experiment).filter_by(experiment_ID=search).all()
        dic = {}
    #return the dictionary of all values from the row
        for u in searchdb:
            new = u.__dict__
            dic.update( new )
    
    #need to work on display of this 
        return {'experimentPage': dic }
    
    
"""experiment_description= request.params['experiment_description']
        related_samples= request.params['related_samples']
        #spectrometer_ID= request.params['spectrometer_ID']
        #depositor_ID= request.params['depositor_ID'] #taken out as rely on relationships not yet created
        #depositor= request.params['depositor']
        #publication_ID= request.params['publication_ID']
        #publication= request.params['publication']
        #spectrometer_ID= request.params['spectrometer_ID']
        data_aquisition_ID= request.params['data_aquisition_ID']
        phase= request.params['phase']
        temperatue= request.params['temperatue']
        pressure= request.params['pressure']
        number_of_sample_scans= request.params['number_of_sample_scans']
        scanner_velocity_KHz= request.params['scanner_velocity_KHz']
        resolution= request.params['resolution']
        start_frequency= request.params['start_frequency']
        end_frequency= request.params['end_frequency']
        optical_filter= request.params['optical_filter']
        #higher_range= request.params['higher_range__cm_1_']
        #lower_range= request.params['lower_range__cm_1_']
        
"""
            
