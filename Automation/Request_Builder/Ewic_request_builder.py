import datetime
import json
from API.config import config
import xmltodict
from API.Excel_operations import Excel_Operations
from API.Product_data_mapping import Product_data_mapping
from API.Socket_API import Adsdk_Socket as Socket
from lxml import etree

Parent_TransactionTotal = "1.00"
Child_TransactionTotal = "10.00"
date = datetime.datetime.now().strftime('%Y/%m/%d')
date = date.replace("/", "")
ReferenceNumber = "12345"
InvoiceNumber = "03012300752001115323"
port = config.Config_Indoor_port()

class Ewic_request_builder:

    @staticmethod
    def Gcb():
        request = None
        if config.request_format().upper() == "XML":
            data = Excel_Operations.Read_Indoor_File("/EWIC/GetCardBINRequest.xml")
            if data:
                request = etree.tostring(data, pretty_print=False, encoding=str, method='html')
        if config.request_format().upper() == "JSON":
            data = Excel_Operations.Read_Indoor_File("/EWIC/GetCardBINRequest.json")
            if data:
                data = json.load(data)
                request = json.dumps(data)
        if request is not None:
            received_data = Socket.single_connection(request, port)
            print(request)
            print(received_data)
            if received_data == "Socket_Error":
                return {"ErrorCode": "1", "ErrorText": "Socket_Error"}
            else:
                try:
                    if config.request_format().upper() == "JSON":
                        received_data = json.loads(received_data)
                    return {"ErrorCode": "0", "Request": request, "Response": received_data}
                except:
                    return {"ErrorCode": "3", "ErrorText": "Format_Error"}
        else:
            return {"ErrorCode": "2", "ErrorText": "File_Not_Found"}

    @staticmethod
    def Ewic_Pin_Entry():
        request = None
        if config.request_format().upper() == "XML":
            data = Excel_Operations.Read_Indoor_File("/EWIC/Pin_Entry.xml")
            if data:
                data.find('.//TransactionDate').text = date
                request = etree.tostring(data, pretty_print=False, encoding=str)
        if request is not None:
            received_data = Socket.single_connection(request, port)
            if received_data == "Socket_Error":
                return {"ErrorCode": "1", "ErrorText": "Socket_Error"}
            else:
                try:
                    if config.request_format().upper() == "JSON":
                        received_data = json.loads(received_data)
                    return {"ErrorCode": "0", "Request": request, "Response": received_data}
                except:
                    return {"ErrorCode": "3", "ErrorText": "Format_Error"}
        else:
            return {"ErrorCode": "2", "ErrorText": "File_Not_Found"}

    @staticmethod
    def Ewic_Balance_Enquiry():
        request = None
        if config.request_format().upper() == "XML":
            data = Excel_Operations.Read_Indoor_File("/EWIC/Balance_enquiry.xml")
            if data:
                data.find('.//TransactionDate').text = date
                request = etree.tostring(data, pretty_print=False, encoding=str)
        if request is not None:
            received_data = Socket.single_connection(request, port)
            if received_data == "Socket_Error":
                return {"ErrorCode": "1", "ErrorText": "Socket_Error"}
            else:
                try:
                    if config.request_format().upper() == "JSON":
                        received_data = json.loads(received_data)
                    return {"ErrorCode": "0", "Request": request, "Response": received_data}
                except:
                    return {"ErrorCode": "3", "ErrorText": "Format_Error"}
        else:
            return {"ErrorCode": "2", "ErrorText": "File_Not_Found"}

    @staticmethod
    def Ewic_Transrequest(Products):
        request = None
        if config.request_format().upper() == "XML":
            data = Excel_Operations.Read_Indoor_File("/EWIC/Transrequest.xml")
            if data:
                root = data.getroot()
                data.find('.//TransactionDate').text = date
                products = Product_data_mapping.Ewic_Product_Mapping(Products)
                product_count = products["PrescriptionData"]["PrescriptionDataCount"]
                xml = xmltodict.unparse(products, encoding=str, full_document=False)
                xml_str = etree.fromstring(xml)
                PrescriptionData_xml = etree.SubElement(root, 'PrescriptionData')
                PrescriptionDataCount_xml = etree.SubElement(PrescriptionData_xml, 'PrescriptionDataCount')
                PrescriptionDataCount_xml.text = str(product_count)
                PrescriptionItems_xml = etree.SubElement(PrescriptionData_xml, 'PrescriptionItems')
                PrescriptionItems = xml_str.findall('.//PrescriptionItem')
                for item in PrescriptionItems:
                    PrescriptionItem_xml = etree.SubElement(PrescriptionItems_xml, 'PrescriptionItem')
                    Category = etree.SubElement(PrescriptionItem_xml, 'Category').text = item.find('.//Category').text
                    SubCategory = etree.SubElement(PrescriptionItem_xml, 'SubCategory').text = item.find('.//SubCategory').text
                    Quantity_xml = etree.SubElement(PrescriptionItem_xml, 'Quantity').text = "00100"
                request = etree.tostring(data, pretty_print=False, encoding=str)
        if request is not None:
            received_data = Socket.single_connection(request, port)
            if received_data == "Socket_Error":
                return {"ErrorCode": "1", "ErrorText": "Socket_Error"}
            else:
                try:
                    if config.request_format().upper() == "JSON":
                        received_data = json.loads(received_data)
                    return {"ErrorCode": "0", "Request": request, "Response": received_data}
                except:
                    return {"ErrorCode": "3", "ErrorText": "Format_Error"}
        else:
            return {"ErrorCode": "2", "ErrorText": "File_Not_Found"}

    @staticmethod
    def Ewic_Card_Removed():
        request = None
        if config.request_format().upper() == "XML":
            data = Excel_Operations.Read_Indoor_File("/EWIC/Card_Removed.xml")
            if data:
                data.find('.//TransactionDate').text = date
                request = etree.tostring(data, pretty_print=False, encoding=str)
        if request is not None:
            received_data = Socket.single_connection(request, port)
            if received_data == "Socket_Error":
                return {"ErrorCode": "1", "ErrorText": "Socket_Error"}
            else:
                try:
                    if config.request_format().upper() == "JSON":
                        received_data = json.loads(received_data)
                    return {"ErrorCode": "0", "Request": request, "Response": received_data}
                except:
                    return {"ErrorCode": "3", "ErrorText": "Format_Error"}
        else:
            return {"ErrorCode": "2", "ErrorText": "File_Not_Found"}
            
    @staticmethod
    def Ewic_Void():
        request = None
        if config.request_format().upper() == "XML":
            data = Excel_Operations.Read_Indoor_File("/EWIC/Ewic_void.xml")
            if data:
                data.find('.//TransactionDate').text = date
                request = etree.tostring(data, pretty_print=False, encoding=str)
        if request is not None:
            received_data = Socket.single_connection(request, port)
            if received_data == "Socket_Error":
                return {"ErrorCode": "1", "ErrorText": "Socket_Error"}
            else:
                try:
                    if config.request_format().upper() == "JSON":
                        received_data = json.loads(received_data)
                    return {"ErrorCode": "0", "Request": request, "Response": received_data}
                except:
                    return {"ErrorCode": "3", "ErrorText": "Format_Error"}
        else:
            return {"ErrorCode": "2", "ErrorText": "File_Not_Found"}