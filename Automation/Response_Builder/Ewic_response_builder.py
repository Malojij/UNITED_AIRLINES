import json
import xmltodict
from Request_Builder.Ewic_request_builder import Ewic_request_builder
from API.config import config
from lxml import etree

request_format = config.request_format()

class Transaction_Processing:

    @staticmethod
    def Ewic_Transaction_details(AllowKeyedEntry, request_type, request):
        Ewic_Balance_Enquiry_PrescriptionData, Gcb_Transaction_Request, Gcb_Transaction_Response, Gcb_Transaction_ResponseCode, Gcb_Transaction_ResponseText, Ewic_Pin_Entry_request, Ewic_Pin_Entry_response, Ewic_Pin_Entry_ResponseCode, Ewic_Pin_Entry_ResponseText, Ewic_Balance_Enquiry_response, Ewic_Balance_Enquiry_request, Ewic_Balance_Enquiry_ResponseCode, Ewic_Balance_Enquiry_ResponseText, Ewic_Transrequest_response, Ewic_Transrequest_request, Ewic_Transrequest_ResponseCode, Ewic_Transrequest_ResponseText, Ewic_Card_Removed_response, Ewic_Card_Removed_request = "", "", "", "" "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
        gcb = Ewic_request_builder.Gcb()
        ErrorCode = gcb["ErrorCode"]
        if ErrorCode == "0":
            if request_format.upper() == "XML":
                Gcb_Transaction_Request = xmltodict.parse(etree.tostring(etree.fromstring(gcb["Request"]), encoding=str))
                Gcb_Transaction_Response = xmltodict.parse(etree.tostring(etree.fromstring(gcb["Response"]), encoding=str))
            if request_format.upper() == "JSON":
                Gcb_Transaction_Request = json.loads(gcb["Request"])
                Gcb_Transaction_Response = json.loads(gcb["Response"])
            Gcb_Transaction_ResponseCode = Gcb_Transaction_Response['GetCardBINResponse']['ResponseCode'] if "ResponseCode" in Gcb_Transaction_Response['GetCardBINResponse'] else ""
            Gcb_Transaction_ResponseText = Gcb_Transaction_Response['GetCardBINResponse']['ResponseText'] if "ResponseText" in Gcb_Transaction_Response['GetCardBINResponse'] else ""
            if Gcb_Transaction_ResponseCode.startswith('0'):
                Ewic_Pin_Entry = Ewic_request_builder.Ewic_Pin_Entry()
                if request_format.upper() == "XML":
                    Ewic_Pin_Entry_request = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Pin_Entry["Request"]), encoding=str))
                    Ewic_Pin_Entry_response = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Pin_Entry["Response"]), encoding=str))
                if request_format.upper() == "JSON":
                    Ewic_Pin_Entry_request = json.loads(Ewic_Pin_Entry["Request"])
                    Ewic_Pin_Entry_response = json.loads(Ewic_Pin_Entry["Response"])
                Ewic_Pin_Entry_ResponseCode = Ewic_Pin_Entry_response['WICCardResponse']['ResponseCode'] if "ResponseCode" in Ewic_Pin_Entry_response["WICCardResponse"] else ""
                Ewic_Pin_Entry_ResponseText = Ewic_Pin_Entry_response['WICCardResponse']['ResponseText'] if "ResponseText" in Ewic_Pin_Entry_response["WICCardResponse"] else ""
                if Ewic_Pin_Entry_ResponseCode.startswith("0"):
                    Ewic_Balance_Enquiry = Ewic_request_builder.Ewic_Balance_Enquiry()
                    if request_format.upper() == "XML":
                        Ewic_Balance_Enquiry_response = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Balance_Enquiry["Response"]), encoding=str))
                        Ewic_Balance_Enquiry_request = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Balance_Enquiry["Request"]), encoding=str))
                    if request_format.upper() == "JSON":
                        Ewic_Balance_Enquiry_response = json.loads(Ewic_Balance_Enquiry["Response"])
                        Ewic_Balance_Enquiry_request = json.loads(Ewic_Balance_Enquiry["Request"])
                    Ewic_Balance_Enquiry_ResponseCode = Ewic_Balance_Enquiry_response["WICCardResponse"]["ResponseCode"] if "ResponseCode" in Ewic_Balance_Enquiry_response["WICCardResponse"] else ""
                    Ewic_Balance_Enquiry_ResponseText = Ewic_Balance_Enquiry_response["WICCardResponse"]["ResponseText"] if "ResponseText" in Ewic_Balance_Enquiry_response["WICCardResponse"] else ""
                    Ewic_Balance_Enquiry_PrescriptionData = Ewic_Balance_Enquiry_response["WICCardResponse"]["PrescriptionData"] if "PrescriptionData" in Ewic_Balance_Enquiry_response["WICCardResponse"] else ""
                    if Ewic_Balance_Enquiry_ResponseCode.startswith("0"):
                        Ewic_Transrequest = Ewic_request_builder.Ewic_Transrequest(Ewic_Balance_Enquiry_PrescriptionData)
                        if request_format.upper() == "XML":
                            Ewic_Transrequest_response = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Transrequest["Response"]), encoding=str))
                            Ewic_Transrequest_request = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Transrequest["Request"]), encoding=str))
                        if request_format.upper() == "JSON":
                            Ewic_Transrequest_response = json.loads(Ewic_Transrequest["Response"])
                            Ewic_Transrequest_request = json.loads(Ewic_Transrequest["Request"])
                        Ewic_Transrequest_ResponseCode = Ewic_Transrequest_response["WICCardResponse"]["ResponseCode"] if "ResponseCode" in Ewic_Transrequest_response["WICCardResponse"] else ""
                        Ewic_Transrequest_ResponseText = Ewic_Transrequest_response["WICCardResponse"]["ResponseText"] if "ResponseText" in Ewic_Transrequest_response["WICCardResponse"] else ""
                        if Ewic_Transrequest_ResponseCode.startswith("0"):
                            Ewic_Card_Removed = Ewic_request_builder.Ewic_Card_Removed()
                            if request_format.upper() == "XML":
                                Ewic_Card_Removed_response = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Card_Removed["Response"]), encoding=str))
                                Ewic_Card_Removed_request = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Card_Removed["Request"]), encoding=str))
                            if request_format.upper() == "JSON":
                                Ewic_Card_Removed_response = json.loads(Ewic_Card_Removed["Response"])
                                Ewic_Card_Removed_request = json.loads(Ewic_Card_Removed["Request"])
            result = {"Gcb_Transaction_Request": Gcb_Transaction_Request,
                      "Gcb_Transaction_Response": Gcb_Transaction_Response,
                      "Gcb_Transaction_ResponseCode": Gcb_Transaction_ResponseCode,
                      "Gcb_Transaction_ResponseText": Gcb_Transaction_ResponseText,
                      "Ewic_Pin_Entry_request": Ewic_Pin_Entry_request,
                      "Ewic_Pin_Entry_response": Ewic_Pin_Entry_response,
                      "Ewic_Pin_Entry_ResponseCode": Ewic_Pin_Entry_ResponseCode,
                      "Ewic_Pin_Entry_ResponseText": Ewic_Pin_Entry_ResponseText,
                      "Ewic_Balance_Enquiry_response": Ewic_Balance_Enquiry_response,
                      "Ewic_Balance_Enquiry_request": Ewic_Balance_Enquiry_request,
                      "Ewic_Balance_Enquiry_ResponseCode": Ewic_Balance_Enquiry_ResponseCode,
                      "Ewic_Balance_Enquiry_ResponseText": Ewic_Balance_Enquiry_ResponseText,
                      "Ewic_Transrequest_response": Ewic_Transrequest_response,
                      "Ewic_Transrequest_request": Ewic_Transrequest_request,
                      "Ewic_Transrequest_ResponseCode": Ewic_Transrequest_ResponseCode,
                      "Ewic_Transrequest_ResponseText": Ewic_Transrequest_ResponseText,
                      "Ewic_Card_Removed_response": Ewic_Card_Removed_response,
                      "Ewic_Card_Removed_request": Ewic_Card_Removed_request }
            result.update(result)
            result = json.dumps(result)
            return result
        else:
            return 0

    @staticmethod
    def Ewic_Void_Transaction_details(AllowKeyedEntry, request_type, request):
        Ewic_Balance_Enquiry_PrescriptionData, Gcb_Transaction_Request, Gcb_Transaction_Response, Gcb_Transaction_ResponseCode, Gcb_Transaction_ResponseText, Ewic_Pin_Entry_request, Ewic_Pin_Entry_response, Ewic_Pin_Entry_ResponseCode, Ewic_Pin_Entry_ResponseText, Ewic_Balance_Enquiry_response, Ewic_Balance_Enquiry_request, Ewic_Balance_Enquiry_ResponseCode, Ewic_Balance_Enquiry_ResponseText, Ewic_Transrequest_response, Ewic_Transrequest_request, Ewic_Transrequest_ResponseCode, Ewic_Transrequest_ResponseText, Ewic_Card_Removed_response, Ewic_Card_Removed_request = "", "", "", "" "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
        gcb = Ewic_request_builder.Gcb()
        if request_format.upper() == "XML":
            Gcb_Transaction_Request = xmltodict.parse(etree.tostring(etree.fromstring(gcb["Request"]), encoding=str))
            Gcb_Transaction_Response = xmltodict.parse(etree.tostring(etree.fromstring(gcb["Response"]), encoding=str))
        if request_format.upper() == "JSON":
            Gcb_Transaction_Request = json.loads(gcb["Request"])
            Gcb_Transaction_Response = json.loads(gcb["Response"])
        Gcb_Transaction_ResponseCode = Gcb_Transaction_Response['GetCardBINResponse']['ResponseCode'] if "ResponseCode" in Gcb_Transaction_Response['GetCardBINResponse'] else ""
        Gcb_Transaction_ResponseText = Gcb_Transaction_Response['GetCardBINResponse']['ResponseText'] if "ResponseText" in Gcb_Transaction_Response['GetCardBINResponse'] else ""
        if Gcb_Transaction_ResponseCode.startswith('0'):
            Ewic_Pin_Entry = Ewic_request_builder.Ewic_Pin_Entry()
            if request_format.upper() == "XML":
                Ewic_Pin_Entry_request = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Pin_Entry["Request"]), encoding=str))
                Ewic_Pin_Entry_response = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Pin_Entry["Response"]), encoding=str))
            if request_format.upper() == "JSON":
                Ewic_Pin_Entry_request = json.loads(Ewic_Pin_Entry["Request"])
                Ewic_Pin_Entry_response = json.loads(Ewic_Pin_Entry["Response"])
            Ewic_Pin_Entry_ResponseCode = Ewic_Pin_Entry_response['WICCardResponse']['ResponseCode'] if "ResponseCode" in Ewic_Pin_Entry_response["WICCardResponse"] else ""
            Ewic_Pin_Entry_ResponseText = Ewic_Pin_Entry_response['WICCardResponse']['ResponseText'] if "ResponseText" in Ewic_Pin_Entry_response["WICCardResponse"] else ""
            if Ewic_Pin_Entry_ResponseCode.startswith("0"):
                Ewic_Transrequest = Ewic_request_builder.Ewic_Void()
                if request_format.upper() == "XML":
                    Ewic_Transrequest_response = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Transrequest["Response"]), encoding=str))
                    Ewic_Transrequest_request = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Transrequest["Request"]), encoding=str))
                if request_format.upper() == "JSON":
                    Ewic_Transrequest_response = json.loads(Ewic_Transrequest["Response"])
                    Ewic_Transrequest_request = json.loads(Ewic_Transrequest["Request"])
                    Ewic_Transrequest_ResponseCode = Ewic_Transrequest_response["WICCardResponse"]["ResponseCode"] if "ResponseCode" in Ewic_Transrequest_response["WICCardResponse"] else ""
                    Ewic_Transrequest_ResponseText = Ewic_Transrequest_response["WICCardResponse"]["ResponseText"] if "ResponseText" in Ewic_Transrequest_response["WICCardResponse"] else ""
                    if Ewic_Transrequest_ResponseCode.startswith("0"):
                        Ewic_Card_Removed = Ewic_request_builder.Ewic_Card_Removed()
                        if request_format.upper() == "XML":
                            Ewic_Card_Removed_response = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Card_Removed["Response"]), encoding=str))
                            Ewic_Card_Removed_request = xmltodict.parse(etree.tostring(etree.fromstring(Ewic_Card_Removed["Request"]), encoding=str))
                        if request_format.upper() == "JSON":
                            Ewic_Card_Removed_response = json.loads(Ewic_Card_Removed["Response"])
                            Ewic_Card_Removed_request = json.loads(Ewic_Card_Removed["Request"])                            
        result = {"Gcb_Transaction_Request": Gcb_Transaction_Request,
                  "Gcb_Transaction_Response": Gcb_Transaction_Response,
                  "Gcb_Transaction_ResponseCode": Gcb_Transaction_ResponseCode,
                  "Gcb_Transaction_ResponseText": Gcb_Transaction_ResponseText,
                  "Ewic_Pin_Entry_request": Ewic_Pin_Entry_request,
                  "Ewic_Pin_Entry_response": Ewic_Pin_Entry_response,
                  "Ewic_Pin_Entry_ResponseCode": Ewic_Pin_Entry_ResponseCode,
                  "Ewic_Pin_Entry_ResponseText": Ewic_Pin_Entry_ResponseText,
                  "Ewic_Balance_Enquiry_response": Ewic_Balance_Enquiry_response,
                  "Ewic_Balance_Enquiry_request": Ewic_Balance_Enquiry_request,
                  "Ewic_Balance_Enquiry_ResponseCode": Ewic_Balance_Enquiry_ResponseCode,
                  "Ewic_Balance_Enquiry_ResponseText": Ewic_Balance_Enquiry_ResponseText,
                  "Ewic_Transrequest_response": Ewic_Transrequest_response,
                  "Ewic_Transrequest_request": Ewic_Transrequest_request,
                  "Ewic_Transrequest_ResponseCode": Ewic_Transrequest_ResponseCode,
                  "Ewic_Transrequest_ResponseText": Ewic_Transrequest_ResponseText,
                  "Ewic_Card_Removed_response": Ewic_Card_Removed_response,
                  "Ewic_Card_Removed_request": Ewic_Card_Removed_request }
        result.update(result)
        result = json.dumps(result)
        return result