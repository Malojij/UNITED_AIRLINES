import json
import re

from django.http import JsonResponse
from django.shortcuts import render

from API.config import config
from Response_Builder.Outdoor_response_builder import Transaction_Processing


class OutdoorTesting:

    def __init__(self):
        self.transaction_processor = Transaction_Processing()
        self.RequestFormat = config.Outdoor_request_format()
        self.API_SEQUENCE = config.OUTDOOR_API_SEQUENCE().split(",")
        self.result = {}

    def Outdoor_Testing(self, request):
        if request.method == 'POST':
            CHILDTRANSREQUEST = None
            PARENTTRANSREQUEST = None
            EncryptionMode = "00"
            TransactionType = request.POST.get('Trans_type')
            cardDataSource = request.POST.get('cds')
            rowData = request.POST.get('rowData', None)  # Use get to avoid KeyError
            product_count = request.POST.get('product_count', 0)
            Iteration = request.POST.get('Iteration')
            PinBlockMode = request.POST.get('pbm', "")
            Transaction_total = request.POST.get('Trn_amt', "")
            if rowData is not None:
                rowData = json.loads(rowData)
                TrackData = rowData.get("TrackData", "")
                EmvDetailsData = rowData.get("EmvDetailsData", "")
                ExpectedCardType = rowData.get("CardType")
                Feature = rowData.get("Feature", None)
                if Feature and Feature.upper().replace(" ", "") == "ONLINEPIN":
                    pinblock, ksnblock = {
                        "01": (rowData.get("Omnikey_PinBlock"), rowData.get("Omnikey_KSNBlock")),
                        "00": (rowData.get("Chasekey_PinBlock"), rowData.get("Chasekey_KSNBlock")),
                        "02": (rowData.get("Fdkey_PinBlock"), rowData.get("Fdkey_KSNBlock"))
                    }.get(PinBlockMode, ("", ""))
                    PinBlockMode = "01" if PinBlockMode == "01" else ""
                else:
                    PinBlockMode = pinblock = ksnblock = ""
                Gcb_TransactionType = "GCB" if TransactionType == "00" else None
                Parent_TransactionType = "Sale" if TransactionType in (
                "01", "02", "03",) else "Pre_auth" if TransactionType in ("04", "05", "05_01", "06", "07", "09",
                                                                          "05_09") else "Refund" if TransactionType == "22" else "GCB" if TransactionType == "00" else None
                Child_TransactionType = "Refund" if TransactionType in ("02", "07") else "Void" if TransactionType in (
                "03", "06") else "Post_auth" if TransactionType in (
                "05", "05_01", "05_09") else "Reversal" if TransactionType == "09" else None

                print(f'Performing # {Iteration} Transaction of {Child_TransactionType + " of" if Child_TransactionType is not None else ""} {Parent_TransactionType}')

                if Parent_TransactionType is not None:
                    PARENTTRANSREQUEST = lambda: self.transaction_processor.ParentTransactionProcessing(TransactionType, TrackData, EncryptionMode, cardDataSource, EmvDetailsData, pinblock, ksnblock, PinBlockMode, Transaction_total, product_count, Iteration)
                if Child_TransactionType is not None:
                    CHILDTRANSREQUEST = lambda: self.transaction_processor.ChildTransactionProcessing(TransactionType, TrackData, EncryptionMode, cardDataSource, EmvDetailsData, pinblock, ksnblock, PinBlockMode, Transaction_total, product_count, Iteration)

                if Parent_TransactionType or Child_TransactionType:
                    method_mapping = {
                        'GCB': lambda: self.transaction_processor.GCBTransaction(lookUpFlag, TrackData, EncryptionMode, cardDataSource, EmvDetailsData, pinblock, ksnblock, PinBlockMode) if Parent_TransactionType else None,
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
                self.result.update({
                    "ErrorText" : self.transaction_processor.ErrorText,
                    "TrackData": TrackData,
                    "requestFormat" : self.RequestFormat,
                    "Expectedcardtype": ExpectedCardType,
                    "GCB_request": self.transaction_processor.Gcb_Transaction_Request,
                    "GCB_response": self.transaction_processor.Gcb_Transaction_Response,
                    "Parent_Transaction_request": self.transaction_processor.Parent_Transaction_request,
                    "Parent_Transaction_response": self.transaction_processor.Parent_Transaction_response,
                    "Child_Transaction_request": self.transaction_processor.Child_Transaction_request,
                    "Child_Transaction_response": self.transaction_processor.Child_Transaction_response,
                    "Parent_TransactionType": Parent_TransactionType,
                    "Child_TransactionType": Child_TransactionType,
                    "Gcb_TransactionType": Gcb_TransactionType
                })
                return JsonResponse(self.result, safe=False)
        else:
            return render(request, "Outdoor_Testing.html")