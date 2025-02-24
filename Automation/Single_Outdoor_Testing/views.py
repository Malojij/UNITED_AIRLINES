from API.config import config
from Response_Builder.Outdoor_response_builder import Transaction_Processing
from django.shortcuts import render
import json
import dict2xml
import re


class Single_Outdoor_Testing:

    def __init__(self):
        self.transaction_processor = Transaction_Processing()
        self.RequestFormat = config.Outdoor_request_format()
        self.API_SEQUENCE = config.OUTDOOR_API_SEQUENCE().split(",")
        self.result = {}
        self.isXml = config.Outdoor_request_format().upper() == "XML"

    def Single_Outdoor_Testing(self, request):
        if request.method == 'POST':
            Iteration = 1
            TrackData = request.POST.get("TrackData", "")
            EmvDetailsData = request.POST.get("EmvData", "")
            PinBlockMode = request.POST.get("pin") if request.POST.get("pin") == "01" else ""
            PinBlock = request.POST.get("PinBlock", "")
            KsnBlock = request.POST.get("KsnBlock", "")
            TransactionType = request.POST.get("Transaction_Type", "")
            cardDataSource = request.POST.get('cds', "")
            TransactionAmount = "" if request.POST['Trn_amt'].upper() == "RANDOM" else request.POST['Trn_amt']
            product_count = "01"
            EncryptionMode = "00"
            PARENTTRANSREQUEST = None
            CHILDTRANSREQUEST = None
            Parent_TransactionType = "Sale" if TransactionType in ("01", "02", "03", ) else "Pre_auth" if TransactionType in ("04", "05","05_01", "06", "07", "09","05_09") else "Refund" if TransactionType == "22" else "GCB" if TransactionType == "00" else None
            Child_TransactionType = "Refund" if TransactionType in ("02", "07") else "Void" if TransactionType in ("03", "06") else "Post_auth" if TransactionType in ("05", "05_01", "05_09") else "Reversal" if TransactionType == "09" else None

            print(f'Performing # {Iteration} Transaction of {Child_TransactionType + " of" if Child_TransactionType is not None else ""} {Parent_TransactionType}')
            if Parent_TransactionType is not None :
                PARENTTRANSREQUEST = lambda : self.transaction_processor.ParentTransactionProcessing(TransactionType, TrackData, EncryptionMode, cardDataSource, EmvDetailsData, PinBlock, KsnBlock, PinBlockMode, TransactionAmount, product_count, Iteration)
            if Child_TransactionType is not None :
                CHILDTRANSREQUEST = lambda : self.transaction_processor.ChildTransactionProcessing(TransactionType, TrackData, EncryptionMode,cardDataSource, EmvDetailsData, PinBlock, KsnBlock, PinBlockMode, TransactionAmount, product_count, Iteration)

            if Parent_TransactionType or Child_TransactionType:
                method_mapping = {
                    'GCB': lambda: self.transaction_processor.GCBTransaction(lookUpFlag, TrackData, EncryptionMode, cardDataSource, EmvDetailsData, PinBlock, KsnBlock, PinBlockMode) if Parent_TransactionType and TransactionType != "22"  else None,
                    'TRANSREQUEST': [PARENTTRANSREQUEST, CHILDTRANSREQUEST] if TransactionType != "00" else None
                }
                for method_name in self.API_SEQUENCE:
                    method_name = method_name.upper().strip()
                    lookUpFlag = re.search(r'GCB(\d+)', method_name).group(1) if re.search(r'GCB(\d+)', method_name) else "4"
                    method_name = "GCB" if re.match(r'^GCB\d+', method_name) else method_name
                    method = method_mapping.get(method_name.upper().strip())
                    if method is not None:
                        if isinstance(method, list):
                            for sub_method in method:
                                if sub_method is not None:
                                    sub_method()  # Assuming each item in the list is callable
                        elif callable(method):
                            method()  # Call the function
                        else:
                            print(f"Method {method_name} not found or is not callable.")

            context = {
                "Data": {
                    "ErrorText" : self.transaction_processor.ErrorText,
                    "GCBResponseText": self.transaction_processor.Gcb_Transaction_ResponseText,
                    "GCBCardType": self.transaction_processor.Gcb_Transaction_CardType,
                    "ParentTransactionID": self.transaction_processor.Parent_Transaction_TransactionIdentifier,
                    "ParentResponseText": self.transaction_processor.Parent_Transaction_ResponseText,
                    "ChildTransactionID": self.transaction_processor.Child_Transaction_TransactionIdentifier,
                    "ChildResponseText": self.transaction_processor.Child_Transaction_ResponseText,
                    "gcb": "GCB Transaction",
                    "Parent_transaction": f"{Parent_TransactionType} Transaction",
                    "Child_transaction": f"{Child_TransactionType} Transaction",
                },
                "Result" : {
                    **({
                           "gcb_request": dict2xml.dict2xml(self.transaction_processor.Gcb_Transaction_Request),
                           "Parent_request": dict2xml.dict2xml(self.transaction_processor.Parent_Transaction_request),
                           "Child_request": dict2xml.dict2xml(self.transaction_processor.Child_Transaction_request),
                           "gcb_response": dict2xml.dict2xml(self.transaction_processor.Gcb_Transaction_Response),
                           "Parent_response": dict2xml.dict2xml(self.transaction_processor.Parent_Transaction_response),
                           "Child_response": dict2xml.dict2xml(self.transaction_processor.Child_Transaction_response),
                       } if self.isXml else {
                        "gcb_request": json.dumps(self.transaction_processor.Gcb_Transaction_Request, sort_keys=False, indent=2),
                        "Parent_request": json.dumps(self.transaction_processor.Parent_Transaction_request, sort_keys=False, indent=2),
                        "Child_request": json.dumps(self.transaction_processor.Child_Transaction_request, sort_keys=False, indent=2),
                        "gcb_response": json.dumps(self.transaction_processor.Gcb_Transaction_Response, sort_keys=False, indent=2),
                        "Parent_response": json.dumps(self.transaction_processor.Parent_Transaction_response, sort_keys=False, indent=2),
                        "Child_response": json.dumps(self.transaction_processor.Child_Transaction_response, sort_keys=False, indent=2),
                    })
                },
            }
            self.result.update(context)
            return render(request, "Single_Outdoor_Testing.html", context=self.result)
        else:
            return render(request, "Single_Outdoor_Testing.html")