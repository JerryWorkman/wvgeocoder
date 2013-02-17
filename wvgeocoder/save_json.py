if __name__ == "__main__":
    import os
    import sys
    #parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    #sys.path.insert(0,parentdir) 
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wvgeocoder.settings")
    path = '/ms4w/apps/wvgeocoder'
    if path not in sys.path:
        sys.path.append(path)


#Other Django stuff here if nexessary

from models import Site

def load_json_file(filename):
    site = Site()
    rv = site.load_json(filename, True)
    if rv is None:
        print 'Error', filename
    else :
        print filename


"""
Load data from json files downloaded from 
'http://services.wvgis.wvu.edu/ArcGIS/rest/services/Map/wv_address_label/MapServer/0/{0}?f=json&pretty=true'
"""
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'Usage {0} [json_file] or [directory]'.format(sys.argv[0])
        sys.exit(1)
    pathname = sys.argv[1]
    if os.path.isdir(pathname) == False:
        load_json_file(pathname)    
    else:
        for (path, dirs, files) in os.walk(pathname):
            print 'Directory: ' + path
            for filename in files:
                fullfilename = os.path.join(path, filename)
                load_json_file(fullfilename)
