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
import numpy
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
import pathlib
from pathlib import Path

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

from ..models import project, experiment, spectrometer, post_processing_and_deposited_spectra, spectra, sample

# regular expression used to find WikiWords



@view_config(route_name='projectform', renderer='../templates/projectform.jinja2')
def projectform(request):
    
    """ project form page """
    #if you dont want schema name to show then make it in to a class
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
                appstruct = form.validate(controls)
               
                #call validate
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

    if 'submitted' in request.params:
        
        
        if request.params['submitted'] == 'Add sample':
            #retrieve project ID and send to sample page
            search = request.matchdict['pagename']
            next_url = request.route_url('sampleForm2',project_ID=search)
            return HTTPFound(location=next_url)
            
        else:
            search = request.matchdict['pagename']
            next_url = request.route_url('experimentForm2',project_ID=search)
            return HTTPFound(location=next_url)
            
        #return HTTPFound(location=next_url)
        
        
        
    else:
        search = request.matchdict['pagename']
    #return project related to ID 
        
        searchdb = request.dbsession.query(project).filter_by(project_ID=search).all()
        dic = {}
        for u in searchdb:
            new = u.__dict__
            dic.update( new )
        
        
        searchexp = request.dbsession.query(experiment).filter_by(project_ID=search).all()
        
        expdic = {}
        
        for u in searchexp:
            new = u.__dict__
            expdic.update( new )
      
    #return samples related to ID in a dictionary

       
        samples = {}
            
        search2 = request.dbsession.query(sample.sample_ID).filter_by(project_ID=search).all()
        
        for u in search2:
            num = u[0]
            samples[ 'sample' + str(num)] = num
           
        
        
    #return spectra related to ID in a dictionary
        #need to return spectra ID and use for getting data from ppd
    # return experiment data
        exp_ID = request.dbsession.query(experiment.experiment_ID).filter_by(project_ID=search).first()
        

        searchexp2 = request.dbsession.query(experiment.experiment_ID).filter_by(project_ID=search).all()
        exp_ID = exp_ID[0]
        print('here')
   
        print(searchexp2)
        exper = {}
    
        # just return related experiment ID's
        for u in searchexp2:
            num = u[0]
            exper[ 'experiment' + str(num)] = num
           
       
    #return spectra detail
        spectradic = {}
        search = request.dbsession.query(spectra).filter_by(experiment_ID=exp_ID).all()
        for u in search:
            new = u.__dict__
            spectradic.update( new )
        
        also = request.dbsession.query(spectra.spectra_ID).filter_by(experiment_ID=exp_ID).first()
        print('help')
        what = also[0]
        # need to fix this 
        if what > 7:
            
            ppd_ID = what
            
        else:
            ppd_ID = 1 
            
        print(ppd_ID) 
        #for some reason the spectra_ID in ppd are all 1
        
        search2 = request.dbsession.query(post_processing_and_deposited_spectra).filter_by(spectra_ID=ppd_ID).all()
        depodic = {}
        for u in search2: 
            new = u.__dict__
            depodic.update( new )
        print(depodic)
        
    # spectrometer information
      
        spectrodic = {}
        search = request.dbsession.query(spectrometer).filter_by(experiment_ID=exp_ID).all()
        for u in search:
            new = u.__dict__
            spectrodic.update( new )
        
        
            
       
     

        
        """spec_ID = spec
        ppd = request.dbsession.query(post_processing_and_deposited_spectra).filter_by(spectra_ID=spec_ID).all()
        depodic = {}
        for u in ppd:
            new = u.__dict__
            depodic.update( new )"""
        #code for outputing all 3 graphs - here you need to add downloadable, and use pathlib      
        plt.figure(1)
        filename = pathlib.PureWindowsPath('C:/ftirdb/ftirdb/data/infrared_spectra/' + depodic['sample_power_spectrum'])
        
        jcamp_dict = JCAMP_reader(filename)
        plt.plot(jcamp_dict['x'], jcamp_dict['y'], label='filename', alpha = 0.7, color='blue')
        plt.xlabel(jcamp_dict['xunits'])
        plt.ylabel(jcamp_dict['yunits'])
        plt.savefig('C:/ftirdb/ftirdb/static/fig.png', transparent=True)
        plt.figure(2)
        filename2 = pathlib.PureWindowsPath('C:/ftirdb/ftirdb/data/infrared_spectra/' + depodic['background_power_spectrum'])
        jcamp_dict2 = JCAMP_reader(filename2)
       
        logged = numpy.log10(jcamp_dict2['x'])
       
        print(jcamp_dict2['x'])
        print(logged)
        print(jcamp_dict2['xunits'])
        JCAMP_calc_xsec(jcamp_dict, skip_nonquant=False, debug=False)
        plt.plot(jcamp_dict['wavelengths'], jcamp_dict['xsec'], label='filename', alpha = 0.7, color='green')
        plt.xlabel(jcamp_dict['xunits'])
        plt.ylabel(jcamp_dict['yunits'])
        plt.savefig('C:/ftirdb/ftirdb/static/fig2.png', transparent=True)
        plt.figure(3)
        filename3 = pathlib.PureWindowsPath('C:/ftirdb/ftirdb/data/infrared_spectra/' + depodic['initial_result_spectrum'])
        jcamp_dict3 = JCAMP_reader(filename3)
        plt.plot(jcamp_dict3['x'], jcamp_dict3['y'], label='filename', alpha = 0.7, color='red')
        plt.xlabel(jcamp_dict['xunits'])
        plt.ylabel(jcamp_dict['yunits'])
        plt.savefig('C:/ftirdb/ftirdb/static/fig3.png', transparent=True)
        jcampname1 ="request.static_url('ftirdb:static/data/"+ depodic['sample_power_spectrum'] 
        jcampname2 ='ftirdb:static/infrared_spectra/'+ depodic['background_power_spectrum']
        jcampname3 ='ftirdb:static/infrared_spectra/'+ depodic['initial_result_spectrum']
        
     
    #need to work on display of this 
        return {'dic': dic , 'expdic':expdic,'exper':exper,'samples':samples,'spectrodic':spectrodic, 'depodic':depodic, 'spectradic':spectradic,'spectrodic':spectrodic, 'sample_power_spectrum': 'ftirdb:static/fig.png',
                'background_power_spectrum': 'ftirdb:static/fig2.png',
                'initial_result_spectrum': 'ftirdb:static/fig3.png', 'filename':jcampname1,'filename2':jcampname2,'filename3':jcampname3}
    
    
    
