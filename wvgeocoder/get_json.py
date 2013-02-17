#! /usr/bin/env python
"""
Downloads address records from WVGIS server and saves as json files
"""
import json

def GetUrl(URL):
    import httplib2
    h = httplib2.Http()
    resp, content = h.request(URL, "GET")
    return content

def WriteFile(i, txt):
    text_file = open("json/{0}.json".format(i), "w")
    text_file.write(txt)
    text_file.close()

template = 'http://services.wvgis.wvu.edu/ArcGIS/rest/services/Map/wv_address_label/MapServer/0/{0}?f=json&pretty=true'
for i in range(333835, 400000):
    url = template.format(i)
    json = GetUrl(url)
    if "error" in json: 
        print i, "error in json"
    else:
        print i
        WriteFile(i, json)
