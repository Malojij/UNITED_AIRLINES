import json
import re
import time

import dict2xml
from django.http import JsonResponse
from django.shortcuts import render

from API.config import config
from Response_Builder.Instore_response_builder import Transaction_Processing
import logging

class InstoreTesting:

    def __init__(self):
        self.transaction_processor = Transaction_Processing()
        self.RequestFormat = config.request_format().upper()
        self.API_SEQUENCE = config.API_SEQUENCE().split(",")
        self.result = {}
        self.isXml = config.request_format().upper() == "XML"
        self.api_patterns = {
            "GETSTATUS": r"(GETSTATUSREQUEST|GETSTATUS|STATUS)(\d*)(?:\(\"(.+?)\"\))?",
            "SHOWSCREEN": r"(SHOWSCREENREQUEST|SHOWSCREEN|SCREENREQUEST)(\d*)(?:\(\"(.+?)\"\))?",
            "GCB": r"(GCB|GCBCHECK|GETCARDBINREQUEST|GETCARDBIN)(\d*)(?:\(\"(.+?)\"\))?",
            "CCTTICKETDISPLAYREQUEST": r"(CCTTICKETDISPLAYREQUEST)(\d*)(?:\(\"(.+?)\"\))?",
            "GETUSERINPUT": r"(GETUSERINPUTREQUEST|GETUSERINPUT)(\d*)(?:\(\"(.+?)\"\))?",
            "SHOWLIST": r"(SHOWLISTREQUEST|SHOWLIST)(\d*)(?:\(\"(.+?)\"\))?",
            "BYPASS": r"(BYPASSREQUEST|BYPASS|BYPASSSCREENREQUEST|BYPASSSCREEN)(\d*)(?:\(\"(.+?)\"\))?",
            "TIMEDELAY": r"(TIMEDELAY|TIMEWAIT)(\d*)(?:\(\"(.+?)\"\))?",
            "RESTARTCCTREQUEST" : r"(RESTARTCCT|RESTARTCCTREQUEST|CCTRESTART)(\d*)(?:\(\"(.+?)\"\))?",
            "TRANSREQUEST" : r"(TRANSREQUEST|TRANSACTIONREQUEST|TRANSACTION|TRANS)(\d*)(?:\(\"(.+?)\"\))?",
            "CLOSEREQUEST" : r"(CLOSEREQUEST|CLOSETRANSACTIONREQUEST|CLOSE|CLOSETRANS)(\d*)(?:\(\"(.+?)\"\))?"
        }

    print(f"------------------------------------------------------------------------------------------------------------------------------------------------------------")
    def Instore_Testing(self, request):
        # Initialize variables from config
        if request.method == 'POST':
            Transaction_type = request.POST.get('Trans_type', None)
            singleTransactionCheck = request.POST.get('singleTransactionCheck', '0')
            Iteration = request.POST.get('Iteration', "1")
            AllowKeyedEntry = request.POST.get('gcb_type', "N")
            Token_type = request.POST.get('token_type', "01")
            product_count = int(request.POST.get('product_count', 0))
            EntrySource = ""  # This is statically assigned as empty string in your code
            amount = None if not request.POST.get('amount') else request.POST.get('amount', None)
            transactionSequence = request.POST.get('transactionSequence', "0")
            childData = request.POST.get('childData', None)
            CHILDTRANSREQUEST = None
            PARENTTRANSREQUEST = None
            if transactionSequence in ("0", "1"):
                if Transaction_type in ("01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","20","06_02_01"):
                    PARENTTRANSREQUEST = lambda : self.transaction_processor.ParentTransactionProcessing(AllowKeyedEntry, product_count, Token_type, Transaction_type, amount)

            if transactionSequence in ("0", "2"):
                if Transaction_type in ("2","02","03","05","06","08","15","16","20", "06_02_01"):
                    CHILDTRANSREQUEST = lambda : self.transaction_processor.ChildTransactionProcessing(childData, product_count,Transaction_type, amount)

            logging.info(f'Performing # {Iteration} Transaction')
            method_mapping = {
                'GETSTATUS': lambda : self.transaction_processor.GetStatusRequest(int(api_number), bypassEnabled, bypassOption),
                'TIMEDELAY': lambda : time.sleep(float(api_message)),
                'SHOWLIST': lambda : self.transaction_processor.SHOWLIST(int(api_number), bypassEnabled, bypassOption),
                'CCTTICKETDISPLAYREQUEST': lambda: self.transaction_processor.displayTicket(int(api_number), bypassEnabled, bypassOption),
                'GCB': lambda: self.transaction_processor.GCBTransaction(Transaction_type, AllowKeyedEntry, EntrySource, str(api_number), bypassEnabled, bypassOption, Token_type),
                'GETUSERINPUT': lambda: self.transaction_processor.GETUSERINPUT(str(api_message), int(api_number), bypassEnabled, bypassOption),
                'SHOWSCREEN': lambda : self.transaction_processor.SHOWSCREEN(str(api_message), int(api_number), bypassEnabled, bypassOption),
                'TRANSREQUEST':  [PARENTTRANSREQUEST, CHILDTRANSREQUEST],
                'RESTARTCCTREQUEST' : lambda : self.transaction_processor.RestartCCTRequestTransaction(),
                'CLOSEREQUEST' : lambda :self.transaction_processor.CLOSETransaction()
            }

            def extract_api_details(api_string):
                for api_name, pattern in self.api_patterns.items():
                    api_string = api_string.upper().strip()
                    match = re.match(pattern, api_string, re.IGNORECASE)
                    if match:
                        number = match.group(2) if match.group(2) else str("4") if "BIN" in api_string else "0"
                        message = match.group(3) if match.group(3) else "Enter Message in API"  # Extract message (optional)
                        return api_name, number, message
                return api_string, None, ""  # Return original name if no match

            # Process each API in sequence
            for api in self.API_SEQUENCE :
                api_name, api_number, api_message = extract_api_details(api)
                method_name = api_name.upper().strip()

                bypassEnabled = True if "BYPASS" in method_name else False
                bypassOption = int(re.search(r'BYPASS(\d+)', method_name).group(1)) if re.search(r'BYPASS(\d+)', method_name) else 0
                method = method_mapping.get(method_name)
                if isinstance(method, list):
                    for sub_method in method:
                        if sub_method is not None:
                            sub_method()  # Assuming each item in the list is callable
                elif callable(method):
                    method()  # Call the function
                else:
                    print(f"Method {method_name} not found or is not callable.")
            if singleTransactionCheck == "1":
                context = {
                    "Data": {
                        "GCBResponseText" : self.transaction_processor.Gcb_Transaction_ResponseText,
                        "GCBCardType" : self.transaction_processor.Gcb_Transaction_CardType,
                        "ParentTransactionID" : self.transaction_processor.Parent_Transaction_TransactionIdentifier,
                        "ParentResponseText" : self.transaction_processor.Parent_Transaction_ResponseText,
                        "ChildTransactionID" : self.transaction_processor.Child_Transaction_TransactionIdentifier,
                        "ChildResponseText" : self.transaction_processor.Child_Transaction_ResponseText,
                        "gcb" : "GCB Transaction",
                        "Parent_transaction" : f"{self.transaction_processor.ParentTransactionType} Transaction",
                        "Child_transaction" : f"{self.transaction_processor.ChildTransactionType} Transaction",
                        "ErrorText" : self.transaction_processor.ErrorText,
                    },
                    "Result": {
                        **(
                            {
                            "gcb_request": dict2xml.dict2xml(self.transaction_processor.Gcb_Transaction_Request),
                            "Parent_request" : dict2xml.dict2xml(self.transaction_processor.Parent_Transaction_request),
                            "Child_request" : dict2xml.dict2xml(self.transaction_processor.Child_Transaction_request),
                            "gcb_response" : dict2xml.dict2xml(self.transaction_processor.Gcb_Transaction_Response),
                            "Parent_response" : dict2xml.dict2xml(self.transaction_processor.Parent_Transaction_response),
                            "Child_response" : dict2xml.dict2xml(self.transaction_processor.Child_Transaction_response),
                    } if self.isXml else {
                            "gcb_request" : json.dumps(self.transaction_processor.Gcb_Transaction_Request, sort_keys=False, indent=2),
                            "Parent_request" : json.dumps(self.transaction_processor.Parent_Transaction_request, sort_keys=False, indent=2),
                            "Child_request" : json.dumps(self.transaction_processor.Child_Transaction_request, sort_keys=False, indent=2),
                            "gcb_response" : json.dumps(self.transaction_processor.Gcb_Transaction_Response, sort_keys=False, indent=2),
                            "Parent_response" : json.dumps(self.transaction_processor.Parent_Transaction_response, sort_keys=False, indent=2),
                            "Child_response" : json.dumps(self.transaction_processor.Child_Transaction_response, sort_keys=False, indent=2),
                    })
                },
            }
                self.result.update(context)
                return render(request, 'Single_Instore_Testing.html', self.result)
            else :
                context = {
                    "ErrorText": self.transaction_processor.ErrorText,
                    "RequestFormat" : self.RequestFormat,
                    "GCB_request" : self.transaction_processor.Gcb_Transaction_Request,
                    "GCB_response" : self.transaction_processor.Gcb_Transaction_Response,
                    "Parent_Transaction_request" : self.transaction_processor.Parent_Transaction_request if self.transaction_processor.Parent_Transaction_request else None,
                    "Parent_Transaction_response" : self.transaction_processor.Parent_Transaction_response if self.transaction_processor.Parent_Transaction_response else None,
                    "Child_Transaction_request": self.transaction_processor.Child_Transaction_request if self.transaction_processor.Child_Transaction_request else None,
                    "Child_Transaction_response" : self.transaction_processor.Child_Transaction_response if self.transaction_processor.Child_Transaction_response else None,
                    "Parent_TransactionType" : self.transaction_processor.ParentTransactionType,
                    "Child_TransactionType" : self.transaction_processor.ChildTransactionType,
                }
                self.result.update(context)
                return JsonResponse(self.result, safe=False)
        else:
            return render(request, 'Instore_Testing.html')
