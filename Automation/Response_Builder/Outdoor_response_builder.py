import traceback

from API.Excel_operations import Excel_Operations
from API.Socket_API import Adsdk_Socket as socket
from API.config import config
from Request_Builder.Outdoor_request_builder import Outdoor_Request_Builder


class Transaction_Processing:

    def __init__(self):
        self.Gcb_Transaction_Request = {}
        self.Gcb_Transaction_Response = {}
        self.Parent_Transaction_request = {}
        self.Parent_Transaction_response = {}
        self.Child_Transaction_response = {}
        self.Child_Transaction_request = {}

        self.Gcb_Transaction_ResponseCode = None
        self.Gcb_Transaction_ResponseText = None
        self.Gcb_Transaction_CardType = None
        self.Parent_Transaction_ResponseCode = None
        self.Parent_Transaction_TransactionIdentifier = None
        self.Parent_Transaction_ResponseText = None
        self.Parent_Transaction_TransactionAmount = None
        self.Parent_Transaction_AurusPayTicketNum = None
        self.Parent_Transaction_TransactionSequenceNumber = None
        self.Child_Transaction_TransactionIdentifier = None
        self.Child_Transaction_ResponseText = None

        self.Outdoor_Request_Builder = Outdoor_Request_Builder()
        self.port = config.Config_Outdoor_port()
        self.operations = Excel_Operations()
        self.isXml = config.Outdoor_request_format().upper() == "XML"
        self.ip = config.Config_machine_ip()
        self.urlExtention = ""
        self.APIurl = ""
        self.isHttps = config.commProtocol() != "5"
        self.url = rf"https://{self.ip}:{self.port}{self.urlExtention}{self.APIurl}"
        self.socket = socket()
        self.ErrorText = ""


    def handleSocketRequest(self, request_data) :
        if self.isHttps :
            try:
                self.socket.openSocket(port=self.port)
                try:
                    self.socket.sendRequest(str(request_data))
                    try:
                        response = self.socket.receiveResponseFromSocket()
                        return response
                    except Exception as e:
                        self.ErrorText = f"Response not received from @ {self.ip}::{self.port} ==> {e}"
                except Exception as e:
                    self.ErrorText = f"Request send Fails @ {self.ip}::{self.port} ==> {e}"
            except Exception as e:
                self.ErrorText = f"Connection Fails @ {self.ip}::{self.port} ==> {e}"
        else:
            try:
                self.socket.httpsRequest(self.url, request_data, config.Outdoor_request_format().lower())
                try:
                    response = self.socket.receiveResponsehttps()
                    return response
                except Exception as e :
                    self.ErrorText = f"Response not received from @ {self.ip}::{self.port} ==> {e}"
            except Exception as e:
                self.ErrorText = f"Request send Fails @ {self.ip}::{self.port} ==> {e}"



    def GCBTransaction(self, lookUpFlag, TrackData, EncryptionMode, cardDataSource, EmvDetailsData, pinblock, ksnblock, PinBlockMode):
        try:
            Gcb_Transaction_Req = self.Outdoor_Request_Builder.gcb(lookUpFlag, TrackData, EncryptionMode, cardDataSource, EmvDetailsData, pinblock, ksnblock, PinBlockMode)
            GCB_Transaction_res = self.handleSocketRequest(Gcb_Transaction_Req)
            if GCB_Transaction_res:
                try:
                    self.Gcb_Transaction_Request = self.operations.ConvertToJson(Gcb_Transaction_Req, self.isXml)
                    self.Gcb_Transaction_Response = self.operations.ConvertToJson(GCB_Transaction_res, self.isXml)
                    self.Gcb_Transaction_ResponseCode = self.Gcb_Transaction_Response.get("GetCardBINResponse" ,{}).get("ResponseCode", "")
                    self.Gcb_Transaction_ResponseText = self.Gcb_Transaction_Response.get("GetCardBINResponse" ,{}).get("ResponseText", "")
                    self.Gcb_Transaction_CardType = self.Gcb_Transaction_Response.get("GetCardBINResponse" ,{}).get("CardType", "")
                except Exception:
                    self.ErrorText = f"Error :: ==> Request/response format not matched. :: Expected ==> { 'XML' if self.isXml else 'JSON' }"
        except Exception as e:
            self.ErrorText = f"Error GCB Transaction :: ==> {e}"

    def ParentTransactionProcessing(self, TransactionType,TrackData, EncryptionMode, cardDataSource, EmvDetailsData, pinblock, ksnblock, PinBlockMode, Transaction_total, product_count, TransactionSeqNum):
        try:
            if TransactionType == "22" or (self.Gcb_Transaction_ResponseCode is not None and self.Gcb_Transaction_ResponseCode.startswith("0")):
                Parent_Transaction_req = self.Outdoor_Request_Builder.Parent_Transaction(TransactionSeqNum, TransactionType, TrackData, EncryptionMode, cardDataSource, EmvDetailsData, pinblock, ksnblock, PinBlockMode, self.Gcb_Transaction_CardType, Transaction_total, product_count)
                Parent_Transaction_res = self.handleSocketRequest(Parent_Transaction_req)
                if Parent_Transaction_res:
                    try:
                        self.Parent_Transaction_request = self.operations.ConvertToJson(Parent_Transaction_req, self.isXml)
                        self.Parent_Transaction_response = self.operations.ConvertToJson(Parent_Transaction_res, self.isXml)
                        trans_detail = self.Parent_Transaction_response.get("TransResponse", {}).get("TransDetailsData", {}).get("TransDetailData", {})
                        if isinstance(trans_detail, list) and len(trans_detail) > 0: trans_detail = trans_detail[0]
                        self.Parent_Transaction_ResponseCode = trans_detail.get("ResponseCode", "")
                        self.Parent_Transaction_TransactionIdentifier = trans_detail.get('TransactionIdentifier', "")
                        self.Parent_Transaction_ResponseText = trans_detail.get('ResponseText', "")
                        self.Parent_Transaction_TransactionSequenceNumber = trans_detail.get('TransactionSequenceNumber', "")
                        self.Parent_Transaction_TransactionAmount = trans_detail.get('TotalApprovedAmount', " ")
                        self.Parent_Transaction_AurusPayTicketNum = self.Parent_Transaction_response.get("TransResponse", {}).get("AurusPayTicketNum", "")
                    except Exception:
                        self.ErrorText = f"Error :: ==> Request/response format not matched. :: Expected ==> { 'XML' if self.isXml else 'JSON' }"
        except Exception as e:
            tb = traceback.format_exc()
            self.ErrorText = f"Error in TransactionProcessing: {e}\nTraceback:\n{tb}"

    def ChildTransactionProcessing(self, TransactionType, TrackData, EncryptionMode, cardDataSource, EmvDetailsData, pinblock, ksnblock, PinBlockMode, Transaction_total, product_count, TransactionSeqNum):
        try:
            if self.Parent_Transaction_ResponseCode is not None and self.Parent_Transaction_ResponseCode.startswith("0", 0, 1):
                if TransactionType.upper() in ("03","06") : Transaction_total = self.Parent_Transaction_TransactionAmount
                if TransactionType.upper() == "09":
                    Child_Transaction_req = self.Outdoor_Request_Builder.Parent_Transaction(self.Parent_Transaction_TransactionSequenceNumber, "10", TrackData, EncryptionMode, cardDataSource,
                                                                                            EmvDetailsData, pinblock, ksnblock, PinBlockMode, self.Gcb_Transaction_CardType,
                                                                                            Transaction_total, product_count)
                    Child_Transaction_res = self.handleSocketRequest(Child_Transaction_req)
                else:
                    Child_Transaction_req = self.Outdoor_Request_Builder.Child_Transaction(
                        productCount=product_count, TransactionSeqNum=TransactionSeqNum,Transaction_Type=TransactionType, CardType=self.Gcb_Transaction_CardType,
                        Parent_TransactionID=self.Parent_Transaction_TransactionIdentifier,Parent_AurusPayTicketNum=self.Parent_Transaction_AurusPayTicketNum,
                        TransAmount=Transaction_total,DuplicateTransCheck="")
                    Child_Transaction_res = self.handleSocketRequest(Child_Transaction_req)
                    if TransactionType == "05_01":  #Post-auth retry scenario
                        Child_Transaction_req = self.Outdoor_Request_Builder.Child_Transaction(
                            productCount=product_count, TransactionSeqNum=TransactionSeqNum, Transaction_Type=TransactionType, CardType=self.Gcb_Transaction_CardType,
                            Parent_TransactionID=self.Parent_Transaction_TransactionIdentifier, Parent_AurusPayTicketNum=self.Parent_Transaction_AurusPayTicketNum,
                            TransAmount=Transaction_total,DuplicateTransCheck="1")
                        Child_Transaction_res = self.handleSocketRequest(Child_Transaction_req)
                    if TransactionType == "05_09":  #Post-auth reversal scenario
                        TransactionType = "099"
                        Child_Transaction_req = self.Outdoor_Request_Builder.Child_Transaction(
                            productCount=product_count, TransactionSeqNum=TransactionSeqNum, Transaction_Type=TransactionType, CardType=self.Gcb_Transaction_CardType,
                            Parent_TransactionID=self.Parent_Transaction_TransactionIdentifier,Parent_AurusPayTicketNum=self.Parent_Transaction_AurusPayTicketNum,
                            TransAmount=Transaction_total, DuplicateTransCheck="")
                        Child_Transaction_res = self.handleSocketRequest(Child_Transaction_req)
                if Child_Transaction_res:
                    try:
                        self.Child_Transaction_request = self.operations.ConvertToJson(Child_Transaction_req, self.isXml)
                        self.Child_Transaction_response = self.operations.ConvertToJson(Child_Transaction_res, self.isXml)
                        trans_detail = self.Child_Transaction_response.get("TransResponse", {}).get("TransDetailsData",{}).get("TransDetailData",{})
                        if isinstance(trans_detail, list) and len(trans_detail) > 0: trans_detail = trans_detail[0]
                        self.Child_Transaction_TransactionIdentifier = trans_detail.get('TransactionIdentifier', "")
                        self.Child_Transaction_ResponseText = trans_detail.get('ResponseText', "")
                    except Exception:
                        self.ErrorText = f"Error :: ==> Request/response format not matched. :: Expected ==> { 'XML' if self.isXml else 'JSON' }"
        except Exception as e:
            tb = traceback.format_exc()
            self.ErrorText = f"Error in TransactionProcessing: {e}\nTraceback:\n{tb}"