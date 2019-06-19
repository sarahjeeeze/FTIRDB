"""

Project: FTIRDB
File: routes.py

Version: v1.0
Date: 10.09.2018
Function: provide the web address route structures

This program is released under the GNU Public Licence (GPL V3)

--------------------------------------------------------------------------
Description:
============
These routes are used to direct user to the correct views


"""
# import all required libraries
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
)
from pyramid.security import (
    Allow,
    Everyone,
)

#******************************************

# import the models 
from .models import FTIRModel, User, atr, chemicals, data_aquisition, depositor, dried_film, experiment, experimental_conditions, fourier_transform_processing, gas, liquid, molecular_composition, molecule, not_atr, post_processing_and_deposited_spectra, project, protein, publication, sample, solid, spectra, spectrometer, state_of_sample



def includeme(config):
    """Direct web address to correct page and python views """
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('view_wiki', '/')
    config.add_route('searchdb','/searchdb')
    config.add_route('form','/form')
    config.add_route('results','/results/{results}')
    config.add_route('graph','/graph')
    config.add_route('about', '/about')
    config.add_route('jcampupload', '/jcampupload')
    config.add_route('upload', '/upload')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('add_account','/add_account')
    config.add_route('add_page', '/add_page')
    config.add_route('userArea','/{user}/userArea', factory=user_factory)
    config.add_route('view_page', '/{pagename}', factory=page_factory)
    config.add_route('edit_page', '/{pagename}/edit_page',
                     factory=page_factory)

def new_page_factory(request):
    pagename = request.matchdict['pagename']
    if request.dbsession.query(FTIRModel).filter_by(name=pagename).count() > 0:
        next_url = request.route_url('edit_page', pagename=pagename)
        raise HTTPFound(location=next_url)
    return NewPage(pagename)

def user_factory(request):
    user = request.matchdict['user']
    page = request.dbsession.query(User).filter_by(name=user).first()
    if page is None:
        raise HTTPNotFound
    return PageResource(page)


class NewPage(object):
    def __init__(self, pagename):
        self.pagename = pagename

    def __acl__(self):
        return [
            (Allow, 'role:editor', 'create'),
            (Allow, 'role:basic', 'create'),
        ]

def page_factory(request):
    pagename = request.matchdict['pagename']
    page = request.dbsession.query(FTIRModel).filter_by(name=pagename).first()
    if page is None:
        raise HTTPNotFound
    return PageResource(page)

class PageResource(object):
    def __init__(self, page):
        self.page = page

    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, Everyone, 'edit'),
            (Allow, Everyone, 'edit'),
        ]
