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

from ..models import sample, state_of_sample, molecules_in_sample




@view_config(route_name='sampleForm', renderer='../templates/sampleForm.jinja2')
def sampleForm(request):
    
    """ project form page """

    class Sample(colander.MappingSchema):
        setup_schema(None,sample)
        sampleschema =sample.__colanderalchemy__
        setup_schema(None,molecules_in_sample)
        molecules_in_sample_schema =molecules_in_sample.__colanderalchemy__
        setup_schema(None,state_of_sample)
        state_of_sample_schema =state_of_sample.__colanderalchemy__
        
        
        
    form = Sample()
    form = deform.Form(form,buttons=('submit',))
        
    
    if 'submit' in request.POST:
        #map columns
        controls = request.POST.items()
        
        #format for db input - descriptive_name = request.params['descriptive_name']
       
        try:
                appstruct = form.validate(controls) #call validate
                #request.dbsession.add(page)
                #project_id = request.dbsession.query(project).filter_by(descriptive_name=descriptive_name).first()
                #project_id = project_id.project_ID
                #next_url = request.route_url('projectPage', pagename=project_id)
                #return HTTPFound(location=next_url)
             
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
        search = request.matchdict['pagename']
    #search = request.params['body']
        searchdb = request.dbsession.query(sample).filter_by(sample_ID=search).all()
        dic = {}
    #return the dictionary of all values from the row
        for u in searchdb:
            new = u.__dict__
            dic.update( new )
    
    #need to work on display of this 
        return {'sampleForm': dic}
    
    
