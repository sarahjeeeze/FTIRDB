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
import shutil

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
from deform.widget import Widget, FileUploadWidget
from deform.interfaces import FileUploadTempStore 
from ..models import FTIRModel, dried_film, atr, not_atr, transflectance_diffuse, spectrometer, data_aquisition,post_processing_and_deposited_spectra, experimental_conditions, spectra, project_has_experiment, exp_has_publication, experiment, gas, molecule, protein, chemical, liquid, project, molecules_in_sample, sample, solid, state_of_sample

# regular expression used to find WikiWords



@view_config(route_name='spectrometerForm', renderer='../templates/spectrometerForm.jinja2')
def spectrometerForm(request):
    
    """ project form page """
  
    tmpstore = FileUploadTempStore()

    class Sample(colander.MappingSchema):
        setup_schema(None,spectrometer)
        spectrometerSchema =spectrometer.__colanderalchemy__
        setup_schema(None,atr)
        atrSchema =atr.__colanderalchemy__
        setup_schema(None,not_atr)
        not_atrSchema =not_atr.__colanderalchemy__
        setup_schema(None,transflectance_diffuse)
        trans_diff_Schema =transflectance_diffuse.__colanderalchemy__
           
        
        
    form = Sample()

    form = deform.Form(form,buttons=('submit',))
    
     

        
    if 'submit' in request.POST:#

        try:
            #upload file functionality - sample_power_spectrum as initial example
                
                controls = request.POST.items()
                pstruct = peppercorn.parse(controls)
                print(pstruct)
                optics = request.params['optics']
                
                #break through adding schema to db without having to manually enter each one
                ok = pstruct['spectrometerSchema']     
                page = spectrometer(**ok)
                request.dbsession.add(page)
                
                
                #try the same for upload and file name to add to db
                pok = pstruct['atrSchema']
                page = atr(**pok)
                request.dbsession.add(page)

                naok = pstruct['not_atrSchema']
                page = not_atr(**naok)
                request.dbsession.add(page)

                tran = pstruct['trans_diff_Schema']
                page = transflectance_diffuse(**tran)
                request.dbsession.add(page)
                appstruct = form.validate(controls) #call validate
                #need to fix this
                print(appstruct)
                experiment_id = request.dbsession.query(spectrometer).filter_by(optics=optics).first()
                spec_id = experiment_id.spectrometer_ID
                next_url = request.route_url('spectrometerPage', spectrometer_ID=spec_id)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'spectrometerForm':e.render()}
           

    else:
        
        spectrometerForm = form.render()
        return{'spectrometerForm':spectrometerForm}
    
        

@view_config(route_name='spectrometerPage', renderer='../templates/spectrometerPage.jinja2')

def spectrometerPage(request):

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
        search = request.matchdict['spectrometer_ID']
    #search = request.params['body']
        searchdb = request.dbsession.query(spectrometer).filter_by(spectrometer_ID=search).all()
        dic = {}
    #return the dictionary of all values from the row
        for u in searchdb:
            new = u.__dict__
            dic.update( new )
    
    #need to work on display of this 
        return {'spectrometerPage': dic }
    
    


