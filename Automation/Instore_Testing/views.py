import json
import re
import time

import dict2xml
from django.http import JsonResponse
from django.shortcuts import render

from API.config import config
from Response_Builder.Instore_response_builder import Transaction_Processing


class InstoreTesting:

    def __init__(self):
        self.transaction_processor = Transaction_Processing()
        self.RequestFormat = config.request_format().upper()
        self.API_SEQUENCE = config.API_SEQUENCE().split(",")
        self.result = {}
        self.isXml = config.request_format().upper() == "XML"

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
                if Transaction_type in ("01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","20","06_02_01", "04_76"):
                    PARENTTRANSREQUEST = lambda : self.transaction_processor.ParentTransactionProcessing(AllowKeyedEntry, product_count, Token_type, Transaction_type, amount)

            if transactionSequence in ("0", "2"):
                if Transaction_type in ("2","02","03","05","06","08","15","16","20", "06_02_01", "04_76"):
                    CHILDTRANSREQUEST = lambda : self.transaction_processor.ChildTransactionProcessing(childData, product_count,Transaction_type, amount)

            print(f'Performing # {Iteration} Transaction')
            method_mapping = {
                'GETSTATUS': lambda : self.transaction_processor.GetStatusRequest(statusType, bypassEnabled, bypassOption),
                'TIMEDELAY': lambda : time.sleep(float(delay)),
                'SIGNATURE': lambda : self.transaction_processor.Signature(bypassEnabled, bypassOption),
                'SHOWLIST': lambda : self.transaction_processor.SHOWLIST(optionType, bypassEnabled, bypassOption),
                'CCTTICKETDISPLAYREQUEST': lambda: self.transaction_processor.displayTicket(int(productList), bypassEnabled, bypassOption),
                'GCB': lambda: self.transaction_processor.GCBTransaction(Transaction_type, AllowKeyedEntry, EntrySource, lookUpFlag, bypassEnabled, bypassOption, Token_type),
                'GETUSERINPUT': lambda: self.transaction_processor.GETUSERINPUT(getuserinputText, getuserinputOption, bypassEnabled, bypassOption),
                'SHOWSCREEN': lambda : self.transaction_processor.SHOWSCREEN(showMessage, showscreenFlag, bypassEnabled, bypassOption),
                'TRANSREQUEST':  [PARENTTRANSREQUEST, CHILDTRANSREQUEST],
                'RESTARTCCTREQUEST' : lambda : self.transaction_processor.RestartCCTRequestTransaction()
            }

            for method_name in self.API_SEQUENCE:
                method_name = method_name.upper().strip()
                showscreenFlag = re.search(r'SHOWSCREEN(\d+)', method_name).group(1) if re.search(r'SHOWSCREEN(\d+)', method_name) else ""
                getuserinputOption = re.search(r'GETUSERINPUT(\d+)', method_name).group(1) if re.search(r'GETUSERINPUT(\d+)', method_name) else ""
                lookUpFlag = re.search(r'GCB(\d+)', method_name).group(1) if re.search(r'GCB(\d+)', method_name) else "4"
                bypassOption = re.search(r'BYPASS(\d+)', method_name).group(1) if re.search(r'BYPASS(\d+)', method_name) else 0
                bypassEnabled = 1 if "BYPASS" in method_name else ""
                showMessage = re.search(r'SHOWSCREEN(\d+)\("(.+?)"\)', method_name).group(2) if re.search(r'SHOWSCREEN(\d+)\("(.+?)"\)', method_name) else ""
                getuserinputText = re.search(r'GETUSERINPUT(\d+)\("(.+?)"\)', method_name).group(2) if re.search(r'GETUSERINPUT(\d+)\("(.+?)"\)', method_name) else ""
                optionType = re.search(r'SHOWLIST(\d+)', method_name).group(1) if re.search(r'SHOWLIST(\d+)', method_name) else ""
                productList = re.search(r'CCTTICKETDISPLAYREQUEST(\d+)', method_name).group(1) if re.search(r'CCTTICKETDISPLAYREQUEST(\d+)', method_name) else product_count
                delay = re.search(r"TIMEDELAY\((.+?)\)", method_name).group(1) if re.search(r"TIMEDELAY\((.+?)\)", method_name) else ""
                statusType = re.search(r'GETSTATUSREQUEST(\d+)', method_name).group(1) if re.search(r'GETSTATUSREQUEST(\d+)', method_name) else ""
                method_name = re.sub(r"BYPASS[0-9]{1,2}", "", method_name) if re.match(r'^BYPASS\d+', method_name) else method_name
                method_name = "RESTARTCCTREQUEST" if re.match(r'^RESTARTCCTREQUEST\d+', method_name) else "GCB" if re.match(r'^GCB\d+', method_name) else "GETSTATUS" if re.match(r'^GETSTATUSREQUEST\d+', method_name) else "GETUSERINPUT" if re.match(r'^GETUSERINPUT\d+', method_name) else "SHOWSCREEN" if re.match(r'^SHOWSCREEN\d+', method_name) else "CCTTICKETDISPLAYREQUEST" if re.match(r'^CCTTICKETDISPLAYREQUEST\d+', method_name) else "SHOWLIST" if re.match(r'^SHOWLIST\d+', method_name) else "SIGNATURE" if re.match(r'^SIGNATURE\d+', method_name) else "TIMEDELAY" if re.match(r'^TIMEDELAY', method_name) else  method_name
                # Fetch the corresponding method from the mapping
                method = method_mapping.get(method_name.upper().strip())
                if isinstance(method, list):
                    for sub_method in method:
                        if sub_method is not None:
                            sub_method()  # Assuming each item in the list is callable
                elif callable(method):
                    method()  # Call the function
                else:
                    print(f"Method {method_name} not found or is not callable.")
            print(f" ErrorText :: {self.transaction_processor.ErrorText}")
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