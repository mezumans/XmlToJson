import os
from XmlToJson import *

IMAGE_FOLDER = 'JPEGImages'
FOLDER = 'VOC2007'

def xml_to_json(file_name):
    data  = open_file("{}//Annotations//{}".format(FOLDER,file_name))
    root = parse_xml(data)
    dict = create_dict_from_xml(root)
    return write_json(dict,"{}//Jsons//{}.json".format(FOLDER,file_name))

def main():
  files = os.listdir('VOC2007/Annotations')
  result = list(map(xml_to_json,files))
  errors = [i for i,ans in enumerate(result) if ans == 1]
  print(errors)  

if __name__== "__main__":
  main()

