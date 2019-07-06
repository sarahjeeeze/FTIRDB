#experiment - dont include in final project

from pyramid.compat import escape
import re
from docutils.core import publish_parts

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.response import Response

from ..models import FTIRModel, User, spectra, post_processing_and_deposited_spectra 

# regular expression used to find WikiWords
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")


@view_config(route_name='results', renderer='../templates/results.jinja2')
def view_results(request):
    
    search = request.matchdict['results']
    #search = request.params['body']
    searchdb = request.dbsession.query(post_processing_and_deposited_spectra).filter(post_processing_and_deposited_spectra.PPandD_ID==search).all()
    count = 0
    print(searchdb)
    dic = {}
    for item in searchdb:
        count += 1
        dic[item.PPandD_ID] = item

    return {"dic":dic}
    #dict =	{
      #"apple": "green",
      #"banana": "yellow",
      #"cherry": "red"
        #}
    #return {"dic":dict}
    #return dic
#../templates/results.jinja2
