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

from ..models import project

# regular expression used to find WikiWords



@view_config(route_name='projectform', renderer='../templates/projectform.jinja2')
def projectform(request):
    
    """ project form page """

    setup_schema(None,project)
    projectSchema=project.__colanderalchemy__
    form = deform.Form(projectSchema,buttons=('submit',))
        
    
    if 'submit' in request.POST:
        #map columns explicitly - see another form for automatic mapping example
        controls = request.POST.items()
        descriptive_name = request.params['descriptive_name']
        related_experiments_ID = request.params['related_experiments_ID']
        page = project(descriptive_name=descriptive_name,related_experiments_ID=related_experiments_ID)
        

        try:
                appstruct = form.validate(controls) #call validate
                request.dbsession.add(page)
                project_id = request.dbsession.query(project).filter_by(descriptive_name=descriptive_name).first()
                project_id = project_id.project_ID
                next_url = request.route_url('projectPage', pagename=project_id)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'projectForm':e.render()}
           

        
    
    else:
        projectForm = form.render()
        return{'projectForm':projectForm}
    
@view_config(route_name='projectPage', renderer='../templates/projectPage.jinja2')

def projectPage(request):

    """This page takes a project with project_ID in the URL and returns a page with a dictionary of
all the values, it also contains buttons for adding samples and experiments. When page is linked from here
the child/parent relationship is created"""

    if 'form.submitted' in request.params:
        if request.params['form.submitted'] == 'sample':
            #retrieve project ID and send to sample page
            search = request.matchdict['pagename']
            next_url = request.route_url('sampleForm', project_ID=search)
            return HTTPFound(location=next_url)
            
        else:
            search = request.matchdict['pagename']
            next_url = request.route_url('experimentForm')
            return HTTPFound(location=next_url)
            
        #return HTTPFound(location=next_url)
        
        
        
    else:
        search = request.matchdict['pagename']
    #search = request.params['body']
        searchdb = request.dbsession.query(project).filter_by(project_ID=search).all()
        dic = {}
    #return the dictionary of all values from the row
        for u in searchdb:
            new = u.__dict__
            dic.update( new )
    
    #need to work on display of this 
        return {'projectForm': dic }
    
    
    
