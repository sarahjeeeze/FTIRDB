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
from ..models import FTIRModel, dried_film, data_aquisition,post_processing_and_deposited_spectra, experimental_conditions, spectra, project_has_experiment, exp_has_publication, experiment, gas, molecule, protein, chemical, liquid, project, molecules_in_sample, sample, solid, state_of_sample

# regular expression used to find WikiWords



@view_config(route_name='spectraForm', renderer='../templates/spectraForm.jinja2')
def spectraForm(request):
    
    """ project form page """
  
    tmpstore = FileUploadTempStore()

    class Sample(colander.MappingSchema):
        setup_schema(None,spectra)
        spectraSchema =spectra.__colanderalchemy__
        sample_power_spectrum = colander.SchemaNode(
                deform.FileData(),
                widget=deform.widget.FileUploadWidget(tmpstore)
                )
        background_power_spectrum = colander.SchemaNode(
                deform.FileData(),
                widget=deform.widget.FileUploadWidget(tmpstore)
                )
        initial_result_spectrum = colander.SchemaNode(
                deform.FileData(),
                widget=deform.widget.FileUploadWidget(tmpstore)
                )
        setup_schema(None,post_processing_and_deposited_spectra)
        ppSchema =post_processing_and_deposited_spectra.__colanderalchemy__
        upload = colander.SchemaNode(
                deform.FileData(),
                widget=deform.widget.FileUploadWidget(tmpstore)
                )
        
       
        
    form = Sample()

    form = deform.Form(form,buttons=('submit',))
        
    if 'submit' in request.POST:
        
        #add more of these and then work on jcamp graph overlays with javascript
        
    

        try:
                #appstruct = form.validate(controls) #call validate
                #upload file functionality - sample_power_spectrum as initial example
                print(request.POST)
                controls = request.POST.items()
                pstruct = peppercorn.parse(controls)
                print(pstruct)
                """ this doesnt work for now dirName = request.params['experiment_ID']
                dirName = 'C:/ftirdb/ftirdb/data/' + dirName
                os.mkdir(dirName)"""
                myfile = pstruct['sample_power_spectrum']['upload']
                background = pstruct['background_power_spectrum']['upload']
                init = pstruct['initial_result_spectrum']['upload']
                permanent_store = 'C:/ftirdb/ftirdb/data/'
                permanent_file = open(os.path.join(permanent_store,
                                        myfile.filename.lstrip(os.sep)),
                                        'wb')
                shutil.copyfileobj(myfile.file, permanent_file)
                myfile.file.close()
                permanent_file.close()
                permanent_file = open(os.path.join(permanent_store,
                                        background.filename.lstrip(os.sep)),
                                        'wb')
                shutil.copyfileobj(background.file, permanent_file)
                background.file.close()
                permanent_file.close()
                permanent_file = open(os.path.join(permanent_store,
                                        init.filename.lstrip(os.sep)),
                                        'wb')
                shutil.copyfileobj(init.file, permanent_file)
                init.file.close()
                permanent_file.close()
                print(myfile.filename)
                #break through adding schema to db without having to manually enter each one
                ok = pstruct['spectraSchema']     
                page = spectra(**ok)
                request.dbsession.add(page)
           
                #try the same for upload and file name to add to db
                pok = pstruct['ppSchema']
                sample_power_spectrum= myfile.filename
                background_power_spectrum= background.filename
                initial = init.filename
                page = post_processing_and_deposited_spectra(sample_power_spectrum=sample_power_spectrum, background_power_spectrum=background_power_spectrum,initial_result_spectrum=initial,**pok)
                request.dbsession.add(page)
                #in future change this so it just querys spectra and takes the first option
                searchdb = request.dbsession.query(spectra).first()
                spectra_ID = searchdb.spectra_ID


                
                
                next_url = request.route_url('spectraPage', spectra_ID=spectra_ID)
                return HTTPFound(location=next_url)
             
        except deform.ValidationFailure as e: # catch the exception
                return {'spectraForm':e.render()}
    else:
        
        spectraForm = form.render()
        return{'spectraForm':spectraForm}          
           

    
@view_config(route_name='spectraPage', renderer='../templates/spectraPage.jinja2')

def spectraPage(request):

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
        search = request.matchdict['spectra_ID']
    #search = request.params['body']
        searchdb = request.dbsession.query(spectra).filter_by(spectra_ID=search).all()
        spectradic = {}
    #return the dictionary of all values from the row
        for u in searchdb:
            new = u.__dict__
            spectradic.update( new )
        searchdb = request.dbsession.query(post_processing_and_deposited_spectra).filter_by(spectra_ID=search).all()
        depodic = {}
        for u in searchdb:
            new = u.__dict__
            depodic.update( new )

            
        plt.figure(1)
        filename = 'C:/ftirdb/ftirdb/data/infrared_spectra/' + depodic['sample_power_spectrum']
        jcamp_dict = JCAMP_reader(filename)
        plt.plot(jcamp_dict['x'], jcamp_dict['y'], label='filename', alpha = 0.7, color='blue')
        plt.xlabel(jcamp_dict['xunits'])
        plt.ylabel(jcamp_dict['yunits'])
        plt.savefig('C:/ftirdb/ftirdb/static/fig.png', transparent=True)
        plt.figure(2)
        filename2 = 'C:/ftirdb/ftirdb/data/infrared_spectra/' + depodic['background_power_spectrum']
        jcamp_dict2 = JCAMP_reader(filename2)
        plt.plot(jcamp_dict2['x'], jcamp_dict2['y'], label='filename', alpha = 0.7, color='green')
        plt.xlabel(jcamp_dict['xunits'])
        plt.ylabel(jcamp_dict['yunits'])
        plt.savefig('C:/ftirdb/ftirdb/static/fig2.png', transparent=True)
        plt.figure(3)
        filename3 = 'C:/ftirdb/ftirdb/data/infrared_spectra/' + depodic['initial_result_spectrum']
        jcamp_dict3 = JCAMP_reader(filename3)
        plt.plot(jcamp_dict3['x'], jcamp_dict3['y'], label='filename', alpha = 0.7, color='green')
        plt.xlabel(jcamp_dict['xunits'])
        plt.ylabel(jcamp_dict['yunits'])
        plt.savefig('C:/ftirdb/ftirdb/static/fig3.png', transparent=True)

    
    #need to work on display of this 
        return {'spectraPage': spectradic, 'deop':depodic, 'sample_power_spectrum': 'ftirdb:static/fig.png', 'background_power_spectrum': 'ftirdb:static/fig2.png',
                'initial_result_spectrum': 'ftirdb:static/fig3.png'}
    
    
    
