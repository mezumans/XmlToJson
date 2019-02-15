import xml.etree.ElementTree as ET    
import json
from functools import wraps
from time import time

def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print ('Function executing:{}\n Elapsed time: {} ms, {}'.format(f.__name__,(end-start)*1000,end-start))
           
        return result
    return wrapper

IMAGE_FOLDER = 'JPEGImages'
FOLDER = 'VOC2007'
@timing
def open_file(path):
   try:
      with open(path,mode = 'r') as file:
         return file.read()
   except IOError:
      print("Error: {} does not exist".format(path))

   
#************************************************XML PARSING************************************
def parse_xml(xml_string):
   root = ET.fromstring(xml_string)
   return root
   
@timing
def create_dict_from_xml(root):
   dict = {}
   dict['uri'] = get_uri(root)
   dict['width'] = get_size(root,'width')
   dict['height'] = get_size(root,'height')
   dict['objs'] = get_objs(root)
   return dict

def get_uri(root):
   folder = root.find('./folder').text
   file_name = root.find('./filename').text
   uri = "{}/{}/{}".format(folder,IMAGE_FOLDER,file_name)
   return uri

def get_size(root,orientation):
   for markup in root.findall('./size/{}'.format(orientation)):
      return markup.text

def get_objs(root):
   objects = root.findall('./object')
   result = list(map(create_dict_from_object,objects))
   return result

#gets an object and creates dicitonary   
def create_dict_from_object(object):
   dict = {}
   label = get_object_label(object)
   bndbox = get_bndbox(object)
   points = calc_polygon_from_bndbox(bndbox)
   dict['label'] = label
   dict['points'] = points
   return dict

def get_object_label(object):
   return try_find('./name',object)
  

def get_bndbox(object):
   result = object.find('./bndbox')
   if (result == None):
      print("Error: Could not find bndbox in object")
      return -1
   else:   
      return result

def calc_polygon_from_bndbox(bndbox):
   xmin = int(try_find('./xmin',bndbox))
   ymin = int(try_find('./ymin',bndbox))
   xmax = int(try_find('./xmax',bndbox))
   ymax = int(try_find('./ymax',bndbox)) 
   return [[xmin,ymin],[xmin,ymax],[xmax,ymin],[xmax,ymax]]
  
def try_find(child,parent):
   try:
      result = parent.find(child).text
   except AttributeError:
      print("Error: Could not find {} in {}".format(child,parent))   
      return -1
   return result
#***********************************XML PARSING END*********************************************

@timing
def write_json(dict,path):
   try:
      with open(path, 'w') as file:
         json.dump(dict, file,indent=4)
   except IOError:
      print("Error: {} does not exist".format(path))
      return -1
   return 1


