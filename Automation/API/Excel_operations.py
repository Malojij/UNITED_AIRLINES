import json

import xmltodict
from lxml import etree

from API.config import config


class Excel_Operations :

    @staticmethod
    def readIndoorFile(filename):
        file_path = rf"{config.Full_Indoor_file_path()}{filename}"
        with open(file_path, 'r') as file :
            request = json.load(file)
        return request

    @staticmethod
    def readOutdoorFile(filename) :
        file_path = rf"{config.Full_Outdoor_file_path()}{filename}"
        with open(file_path, 'r') as file :
            request = json.load(file)
        return request

    @staticmethod
    def ConvertToXml(data):
        request = xmltodict.unparse(data, encoding=str)
        request = request.split("?>", 1)[-1].strip()  # remove xml declaration <?xml version="1.0" encoding="utf-8"?>
        return request

    @staticmethod
    def ConvertToJson(data, isXml=True):
        request = None
        if isXml:
            data =  data.split("?>", 1)[-1].strip()  # remove xml declaration <?xml version="1.0" encoding="utf-8"?>
            request = xmltodict.parse(etree.tostring(etree.fromstring(data), encoding=str))
        else:
            request = json.loads(data)
        return request


    @staticmethod
    def Read_indoor_Transrequest(format, filename) :
        if format.upper() == "XML" :
            try :
                parser = etree.XMLParser(remove_blank_text=True)
                x = etree.parse(config.Indoor_xml_request_path() + filename, parser)
                return x
            except :
                return False
        if format.upper() == "JSON" :
            try :
                x = open(config.Indoor_json_request_path() + filename)
                return x
            except :
                return False

    @staticmethod
    def Read_outdoor_Transrequest(format, filename) :
        if format.upper() == "XML" :
            try :
                parser = etree.XMLParser(remove_blank_text=True)
                x = etree.parse(config.Outdoor_xml_request_path() + filename, parser)
                return x
            except :
                return False
        if format.upper() == "JSON" :
            try :
                x = open(config.Outdoor_json_request_path() + filename)
                return x
            except :
                return False

