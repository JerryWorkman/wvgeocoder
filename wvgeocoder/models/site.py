from django.db import models
from django.contrib.gis.db import models as gismodels
from wvgeocoder.models.addy import Normalize

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

class Site(models.Model):
    fid = models.IntegerField(primary_key=True)
    objectid = models.IntegerField(null=True, blank=True)
    site_id = models.IntegerField(null=True, blank=True)
    site_type = models.CharField(max_length=10, blank=True)
    street_id = models.IntegerField(null=True, blank=True)
    addr_label = models.CharField(max_length=40, blank=True)
    address_nu = models.IntegerField(null=True, blank=True)
    post_id = models.IntegerField(null=True, blank=True)
    cnty_id = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip = models.CharField(max_length=15, blank=True)
    name_id = models.IntegerField(null=True, blank=True)
    street_i_1 = models.IntegerField(null=True, blank=True)
    historic = models.NullBooleanField(null=True, blank=True)
    post_id = models.IntegerField(null=True, blank=True)
    cnty_id = models.IntegerField(null=True, blank=True)
    name_id = models.IntegerField(null=True, blank=True)
    street_i_1 = models.IntegerField(null=True, blank=True)
    side = models.CharField(max_length=2, blank=True)
    name_order = models.CharField(max_length=2, blank=True)
    name_id_1 = models.IntegerField(null=True, blank=True)
    name_type = models.IntegerField(null=True, blank=True)
    prefix_dir = models.CharField(max_length=10, blank=True)
    name = models.CharField(max_length=40, blank=True)
    suffix_typ = models.CharField(max_length=10, blank=True)
    suffix_dir = models.CharField(max_length=5, blank=True)
    unparsed = models.CharField(max_length=50, blank=True)
    updated_1 = models.BigIntegerField(null=True, blank=True)
    name_1 = models.CharField(max_length=50, blank=True) #city
    cnty_id_1 = models.IntegerField(null=True, blank=True)
    updated_12 = models.BigIntegerField(null=True, blank=True)
#    point_x = models.FloatField(null=True, blank=True)
#    point_y = models.FloatField(null=True, blank=True)
    geometry = gismodels.PointField(srid=3857)  # Same as 900913 (google web mercator) 102100 (3857)
    the_geom = gismodels.PointField(srid=4326)  # geographic
    objects = gismodels.GeoManager()
    
#    addy_map = {
#        'address': 'addr_label',
#        'predirAbbrev' : 'prefix_dir',
#        'streetName' : 'name',
#        'streetTypeAbbrev' : 'suffix_typ',
#        'postdirAbbrev' : 'suffix_dir',
#        #'internal' :
#        'location' : 'name_1',
#        'stateAbbrev' : 'state',
#        'zip' : 'zip',
#    }
    
    def getLat(self):
        return self.the_geom.y 

    def getLon(self):
        return self.the_geom.x 

    class Meta:
        db_table = u'site'
        app_label = u'...' #needed to run from command line

    def __unicode__(self):
        a =  "{0} {1} {2} {3}, {4} {5}, {6} {7}".format(xstr(self.addr_label), xstr(self.prefix_dir),  
            xstr(self.name), xstr(self.suffix_typ), xstr(self.suffix_dir), xstr(self.name_1), 
            xstr(self.state), xstr(self.zip))
        return a.replace(' ,', '').replace('  ', '')
    
    def get_fields(self):
        # make a list of field/values.
        return [(field.verbose_name, field.value_to_string(self)) for field in Site._meta.fields]

    visible_fields = ['site_id', 'addr_label', 'prefix_dir', 'name', 'suffix_typ', 'suffix_dir', 'name_1', 'state', 'zip']

    def get_visible_fields(self):
        # make a list of visible field/values.
#        return self.get_fields()
        vfields = []
        for field in self.get_fields():
            if field.name in self.visible_fields:
                vfields.append(field)
        return vfields

    def get_all_fields(self):
        d = []
        for field in self._meta.fields:
            d.append( { "verbose": field.verbose_name, "value": field.value_to_string(self), "classname": field.__class__.__name__} )
        return d

    """
    {
      "error" :
      {
        "code" : 400,
        "message" : "Unable to find feature",
        "details" : []
      }
    }
    """

    def load_json(self, json_file, save=True):
        import json
        try:
            with open(json_file) as data_file:    
                json_data = json.load(data_file)
        except:
            print "Error opening file:", json_file
            return None
        if 'error' in json_data:
            error = json_data['error']
            print 'JSON error: ', error['message']
            return None            
        if 'feature' in json_data:
            feature = json_data['feature']
            if 'attributes' in feature:
                attributes = feature['attributes']
            else: return None
        else: return None
        field_names = Site._meta.get_all_field_names()
        for field_name in field_names:
            field_name = field_name.upper()
            if field_name in attributes:
                setattr(self, field_name.lower(), attributes[field_name])
        x = float(json_data['feature']['geometry']['x'])
        y = float(json_data['feature']['geometry']['y'])
        from django.contrib.gis.geos import Point
        self.geometry = Point(x, y)
        #import pprint
        #pprint.pprint(self)
        #print 'Fid:', self.fid
        if self.fid > -1: 
            if save: 
                self.save()
            return attributes
        else:
            return None

    def query(self, address):
        normaddy = Normalize(address).dict()
        sql = 'select * from ' + self.Meta.db_table + ' where 1=1'
        #model._meta.get_all_field_names()
        #model._meta.get_field()
        for addy_field in self.addy_map:
            field_value = normaddy[addy_field]
            if field_value:
                sql += ' and ' + addy_field + ' = ' + field_value
#        if addy.address:
#            sql += ' and address = ' + addy.address
#        #TODO: finish this
#        if addy.streetName:
#            sql += ' and address = ' + addy.address
