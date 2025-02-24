import json

from API.config import config
from Response_Builder.Ewic_response_builder import Transaction_Processing as Response
from dict2xml import dict2xml
from django.shortcuts import render


def Ewic_Testing(request):
    request_format = config.request_format()
    if request.method == 'POST':
        AllowKeyedEntry = request.POST['gcb_type']
        AllowKeyedEntry = "N" if AllowKeyedEntry == "00" or AllowKeyedEntry == "01" else "Y"
        TransactionType = request.POST['Transaction_Type']
        if TransactionType == "00":
            Transaction = Response.Ewic_Transaction_details(AllowKeyedEntry=AllowKeyedEntry, request_type=TransactionType, request=request)
            Transaction = json.loads(Transaction)
        if TransactionType == "01":
            Transaction = Response.Ewic_Void_Transaction_details(AllowKeyedEntry=AllowKeyedEntry, request_type=TransactionType, request=request)
            Transaction = json.loads(Transaction)
        if request_format.upper() == "JSON":
            Gcb_Transaction_Request = json.loads(Transaction['Gcb_Transaction_Request'])
            Gcb_Transaction_Response = json.loads(Transaction['Gcb_Transaction_Response'])
            Gcb_Transaction_ResponseCode = json.loads(Transaction['Gcb_Transaction_ResponseCode'])
            Gcb_Transaction_ResponseText = json.loads(Transaction['Gcb_Transaction_ResponseText'])
            Ewic_Pin_Entry_request = json.loads(Transaction['Ewic_Pin_Entry_request'])
            Ewic_Pin_Entry_response = json.loads(Transaction['Ewic_Pin_Entry_response'])
            Ewic_Pin_Entry_ResponseCode = json.loads(Transaction['Ewic_Pin_Entry_ResponseCode'])
            Ewic_Pin_Entry_ResponseText = json.loads(Transaction['Ewic_Pin_Entry_ResponseText'])
            Ewic_Balance_Enquiry_response = json.loads(Transaction['Ewic_Balance_Enquiry_response'])
            Ewic_Balance_Enquiry_request = json.loads(Transaction['Ewic_Balance_Enquiry_request'])
            Ewic_Balance_Enquiry_ResponseCode = json.loads(Transaction['Ewic_Balance_Enquiry_ResponseCode'])
            Ewic_Balance_Enquiry_ResponseText = json.loads(Transaction['Ewic_Balance_Enquiry_ResponseText'])
            Ewic_Transrequest_response = json.loads(Transaction['Ewic_Transrequest_response'])
            Ewic_Transrequest_request = json.loads(Transaction['Ewic_Transrequest_request'])
            Ewic_Transrequest_ResponseCode = json.loads(Transaction['Ewic_Transrequest_ResponseCode'])
            Ewic_Transrequest_ResponseText = json.loads(Transaction['Ewic_Transrequest_ResponseText'])
            Ewic_Card_Removed_response = json.loads(Transaction['Ewic_Card_Removed_response'])
            Ewic_Card_Removed_request = json.loads(Transaction['Ewic_Card_Removed_request'])
            Gcb_Transaction_Request = json.dumps(Gcb_Transaction_Request, sort_keys=False, indent=0)
            Gcb_Transaction_Response = json.dumps(Gcb_Transaction_Response, sort_keys=False, indent=0)
            Gcb_Transaction_ResponseCode = json.dumps(Gcb_Transaction_ResponseCode, sort_keys=False, indent=2)
            Gcb_Transaction_ResponseText = json.dumps(Gcb_Transaction_ResponseText, sort_keys=False, indent=2)
            Ewic_Pin_Entry_request = json.dumps(Ewic_Pin_Entry_request, sort_keys=False, indent=2)
            Ewic_Pin_Entry_response = json.dumps(Ewic_Pin_Entry_response, sort_keys=False, indent=2)
            Ewic_Pin_Entry_ResponseCode = json.dumps(Ewic_Pin_Entry_ResponseCode, sort_keys=False, indent=2)
            Ewic_Pin_Entry_ResponseText = json.dumps(Ewic_Pin_Entry_ResponseText, sort_keys=False, indent=2)
            Ewic_Balance_Enquiry_response = json.dumps(Ewic_Balance_Enquiry_response, sort_keys=False, indent=2)
            Ewic_Balance_Enquiry_request = json.dumps(Ewic_Balance_Enquiry_request, sort_keys=False, indent=2)
            Ewic_Balance_Enquiry_ResponseCode = json.dumps(Ewic_Balance_Enquiry_ResponseCode, sort_keys=False, indent=2)
            Ewic_Balance_Enquiry_ResponseText = json.dumps(Ewic_Balance_Enquiry_ResponseText, sort_keys=False, indent=2)
            Ewic_Transrequest_response = json.dumps(Ewic_Transrequest_response, sort_keys=False, indent=2)
            Ewic_Transrequest_request = json.dumps(Ewic_Transrequest_request, sort_keys=False, indent=2)
            Ewic_Transrequest_ResponseCode = json.dumps(Ewic_Transrequest_ResponseCode, sort_keys=False, indent=2)
            Ewic_Transrequest_ResponseText = json.dumps(Ewic_Transrequest_ResponseText, sort_keys=False, indent=2)
            Ewic_Card_Removed_response = json.dumps(Ewic_Card_Removed_response, sort_keys=False, indent=2)
            Ewic_Card_Removed_request = json.dumps(Ewic_Card_Removed_request, sort_keys=False, indent=2)
        if request_format.upper() == "XML":
            Gcb_Transaction_Request = dict2xml(Transaction['Gcb_Transaction_Request'])
            Gcb_Transaction_Response = dict2xml(Transaction['Gcb_Transaction_Response'])
            Gcb_Transaction_ResponseCode = dict2xml(Transaction['Gcb_Transaction_ResponseCode'])
            Gcb_Transaction_ResponseText = dict2xml(Transaction['Gcb_Transaction_ResponseText'])
            Ewic_Pin_Entry_request = dict2xml(Transaction['Ewic_Pin_Entry_request'])
            Ewic_Pin_Entry_response = dict2xml(Transaction['Ewic_Pin_Entry_response'])
            Ewic_Pin_Entry_ResponseCode = dict2xml(Transaction['Ewic_Pin_Entry_ResponseCode'])
            Ewic_Pin_Entry_ResponseText = Transaction['Ewic_Pin_Entry_ResponseText']
            Ewic_Balance_Enquiry_response = dict2xml(Transaction['Ewic_Balance_Enquiry_response'])
            Ewic_Balance_Enquiry_request = dict2xml(Transaction['Ewic_Balance_Enquiry_request'])
            Ewic_Balance_Enquiry_ResponseCode = dict2xml(Transaction['Ewic_Balance_Enquiry_ResponseCode'])
            Ewic_Balance_Enquiry_ResponseText = dict2xml(Transaction['Ewic_Balance_Enquiry_ResponseText'])
            Ewic_Transrequest_response = dict2xml(Transaction['Ewic_Transrequest_response'])
            Ewic_Transrequest_request = dict2xml(Transaction['Ewic_Transrequest_request'])
            Ewic_Transrequest_ResponseCode = dict2xml(Transaction['Ewic_Transrequest_ResponseCode'])
            Ewic_Transrequest_ResponseText = dict2xml(Transaction['Ewic_Transrequest_ResponseText'])
            Ewic_Card_Removed_response = dict2xml(Transaction['Ewic_Card_Removed_response'])
            Ewic_Card_Removed_request = dict2xml(Transaction['Ewic_Card_Removed_request'])
        context = { "gcb": "GCB",
                    "Gcb_Transaction_Request" : Gcb_Transaction_Request,
                    "Gcb_Transaction_Response" : Gcb_Transaction_Response,
                    "Gcb_Transaction_ResponseCode" : Gcb_Transaction_ResponseCode,
                    "Gcb_Transaction_ResponseText" : Gcb_Transaction_ResponseText,
                    "Ewic_Pin_Entry_request" : Ewic_Pin_Entry_request,
                    "Ewic_Pin_Entry_response" : Ewic_Pin_Entry_response,
                    "Ewic_Pin_Entry_ResponseCode" : Ewic_Pin_Entry_ResponseCode,
                    "Ewic_Pin_Entry_ResponseText" : Ewic_Pin_Entry_ResponseText,
                    "Ewic_Balance_Enquiry_response" : Ewic_Balance_Enquiry_response,
                    "Ewic_Balance_Enquiry_request" : Ewic_Balance_Enquiry_request,
                    "Ewic_Balance_Enquiry_ResponseCode" : Ewic_Balance_Enquiry_ResponseCode,
                    "Ewic_Balance_Enquiry_ResponseText" : Ewic_Balance_Enquiry_ResponseText,
                    "Ewic_Transrequest_response" : Ewic_Transrequest_response,
                    "Ewic_Transrequest_request" : Ewic_Transrequest_request,
                    "Ewic_Transrequest_ResponseCode" : Ewic_Transrequest_ResponseCode,
                    "Ewic_Transrequest_ResponseText" : Ewic_Transrequest_ResponseText,
                    "Ewic_Card_Removed_response" : Ewic_Card_Removed_response,
                    "Ewic_Card_Removed_request" : Ewic_Card_Removed_request

            }
        return render(request, 'Ewic_Testing.html', context)
    else:
        return render(request, "Ewic_Testing.html")