"""
views.py
"""
#from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import json
from models.site import Site
from models.addy import Normalize, Geocoder

def home(request):
    return render_to_response('index.html',
            {}, 
            context_instance=RequestContext(request))
    
def get_site(request, fid=None):
    try:
        site = Site.objects.get(fid=fid)
        addr = site.__unicode__()
#        if ',' in addr:
#            addr = "\\n".join(addr.split(','))
        return render_to_response('site.html', 
                { 'address': addr, 'lat': site.getLat(), 'lon': site.getLon() }, 
                context_instance=RequestContext(request))
    except:
        return render_to_response('site.html',
                { 'error' : 'not found', 'fid': fid }, 
                context_instance=RequestContext(request))
        
def get_geocode_site(request):
    try:
        addr = request.REQUEST['a']   
        lat = request.REQUEST['lat']   
        lon = request.REQUEST['lon'] 
#        if ',' in addr:
#            addr = "\\n".join(addr.split(','))
        return render_to_response('site.html', 
                { 'address': addr, 'lat': lat, 'lon': lon }, 
                context_instance=RequestContext(request))
    except:
        return render_to_response('site.html',
                { 'error' : 'address, lat, and lon are required' }, 
                context_instance=RequestContext(request))
        
def site_search_form(request):
    return render_to_response('site_search_form.html', 
            {}, 
            context_instance=RequestContext(request))
    
def site_search(request):
    sites = []
    if 'address' in request.REQUEST:
        addr = request.REQUEST['address']   
        normalize = Normalize(addr)
        normaddy = normalize.toDict()
        addy = normalize.toAddy()
        addy_map = {
            'address': 'addr_label',
            'predirabbrev' : 'prefix_dir',
            'streetname' : 'name',
            'streettypeabbrev' : 'suffix_typ',
            'postdirabbrev' : 'suffix_dir',
            'internal' : '',
            'location' : 'name_1',
            'stateabbrev' : 'state',
            'zip' : 'zip',
            'parsed' : '',
        }
        query = "select * from site"
        where = ""
        valid = False
        for field, value in normaddy.items():
            if(field.lower() != 'id' and field.lower() != 'fid' and field in addy_map):            
                if value and value != None and value != 'None' and addy_map[field]:
                    if valid: 
                        where += ' and'
                    else:
                        valid = True
                    if type(value) == str or type(value) == unicode: 
                        value = value.upper()
                    where += " {0} = '{1}'".format(addy_map[field], value ) 
        query += ' where' + where # + ' order by name, address'
        if valid:
            [sites.append(site) for site in Site.objects.raw(query)]
        import operator
        ordered = sorted(sites, key=operator.attrgetter('addr_label'))
        geocoder = Geocoder(addr)
        georecords = geocoder.toAddy()
        return render_to_response('site_list.html', 
            { 'sites': ordered, 'query' : query, 'addy' : addy, 'georecords' : georecords }, 
            context_instance=RequestContext(request))

def normalize_address(request):
    if 'address' in request.REQUEST:
        address = request.REQUEST['address']   
        normaddy = Normalize(address)
        dat = normaddy.dict()
    else:
        dat = ['error', 'address is a required parameter']
    response = HttpResponse()
    response.content_type = 'text/json'
    response.write(json.dumps(dat))
    return response
