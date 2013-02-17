from django.db import connection

def xstr(s):
    try:
        if s is None:
            return '' 
        elif type(s) == int or type(s) == float:
            return s
        elif s[0].isnumeric():
            return s.lower()
        elif len(s) <= 2:
            return s.upper()
        else:
            return s.title()  
    except:
        return ''

class Addy:

    def __init__(self, rec):
        self.d = rec
    
    def query_string(self):
        return "a={0}&lat={1}&lon={2}".format(self.__unicode__(), self.d['lat'], self.d['lon'])
    
    def __unicode__(self):
        """format a single record"""
        addr = '{0} {1} {2} {3}, {4} {5} {6}, {7} {8}'.format(
            self.d['address'], self.d['predirabbrev'], xstr(self.d['streetname']), 
            xstr(self.d['streettypeabbrev']), self.d['postdirabbrev'], self.d['internal'],
            self.d['location'], self.d['stateabbrev'], self.d['zip'])        
        return addr.replace('None', '').replace(' ,', ' ').replace('  ', ' ')
    
    def getLat(self):
        return self.d['lat'] 
    
    def getLon(self):
        return self.d['lon'] 
       
class Normalize:
    #The street number
    #address                      
    #Directional prefix of road such as N, S, E, W etc. These are controlled using the direction_lookup table.
    #predirabbrev    
    #streetname
    #abbreviated version of street type: e.g. St, Ave, Cir. These are controlled using the street_type_lookup table.
    #streettypeabbrev 
    #abbreviated directional suffice of road N, S, E, W etc. These are controlled using the direction_lookup table.
    #postdirabbrev 
    #internal address such as an apartment or suite number.
    #internal  
    #usually a city or governing province.
    #location 
    #two character US State. e.g MA, NY, MI. These are controlled by the state_lookup table.
    #stateabbrev  
    #5-digit zipcode. e.g. 02109.
    #zip 
    #parsed 

    template = "SELECT * FROM normalize_address('{0}') as g;"
 
    def __init__(self, address):
        query = self.template.format(address)
        cursor = connection.cursor()    
        cursor.execute(query)
        desc = cursor.description
        self.d = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ][0] # there is just and only one
        self.addy = Addy(self.d)
 
    def toDict(self):
        return self.d
    
    def toAddy(self):
        return self.addy
 
    def __unicode__(self):
        return self.addy.__unicode__()
 
class Geocoder:
    d = []
    template = "SELECT g.rating, ST_X(g.geomout) As lon, "
    template += "ST_Y(g.geomout) As lat, (addy).* FROM geocode('{0}') as g;"
    
    def __init__(self, address):
        cursor = connection.cursor()    
        query = self.template.format(address)
        cursor.execute(query)
        desc = cursor.description
        self.d = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
    
    def toDict(self):
        return self.d

    def toAddy(self):
        d = []        
        [d.append(Addy(r)) for r in self.d]
        return d
