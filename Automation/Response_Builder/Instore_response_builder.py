import json
import random
import string
import threading
import time
import traceback
from API.Excel_operations import Excel_Operations
from API.Socket_API import Adsdk_Socket as socket
from API.config import config
from Request_Builder.Instore_request_builder import Transaction_Request_Builder

class Transaction_Processing :

    def __init__(self):

        self.Gcb_Transaction_Request = {}
        self.Gcb_Transaction_Response = {}
        self.Parent_Transaction_request = {}
        self.Parent_Transaction_response = {}
        self.Child_Transaction_response = {}
        self.Child_Transaction_request = {}
        self.GETUSERINPUT_Request = {}
        self.GETUSERINPUT_Response = {}

        self.Gcb_Transaction_CardType = None
        self.Gcb_Transaction_ResponseCode = None
        self.Gcb_Transaction_ResponseText = None
        self.Gcb_Transaction_CardToken = None
        self.Gcb_Transaction_CIToken = None
        self.Gcb_Transaction_CRMToken = None
        self.Gcb_Transaction_CashbackAmount = None

        self.GetUserInput_inputText = None

        self.Parent_Transaction_ResponseCode = None
        self.Parent_Transaction_ResponseText = None
        self.Parent_Transaction_TransactionAmount = None
        self.Parent_Transaction_TransactionIdentifier = None
        self.Parent_Transaction_AurusPayTicketNum = None

        self.Child_Transaction_ResponseText = None
        self.Child_Transaction_TransactionIdentifier = None
        self.Child_Transaction_AurusPayTicketNumber = None

        self.RandomNumberForInvoice = random.randint(100000, 999999)
        self.RandomNumberForPNR = ''.join(random.sample(string.ascii_uppercase + string.digits, k=6))
        self.port = config.Config_Indoor_port()
        self.OutdoorPort = config.Config_Outdoor_port()
        self.Transaction_Request_Builder = Transaction_Request_Builder()
        self.ip = config.Config_machine_ip()
        self.urlExtension = ""
        self.APIurl = ""
        self.url = rf"https://{self.ip}:{self.port}{self.urlExtension}{self.APIurl}"
        self.socket = socket()
        self.isHttps = config.commProtocol() != "5"
        self.isXml = config.request_format().upper() == "XML"
        self.isSignatureEnabled = "0"
        self.ParentTransactionType = ""
        self.ChildTransactionType = ""
        self.ErrorText = ""
        self.tokenForTransaction = ""

    def handleSocketRequest(self, request_data, bypassEnabled, bypassOption) :
        if not self.isXml: request_data = json.loads(request_data)
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
        else :
            threads = []
            response_list = []
            if bypassEnabled :
                bypassData = self.Transaction_Request_Builder.ByPassScreenRequest(bypassOption)
                if not self.isXml : bypassData = json.loads(bypassData)
                data = [request_data, bypassData]

                def send_request(url, request_data) :
                    self.socket.httpsRequest(url, request_data, config.request_format().lower())
                    response = self.socket.receiveResponsehttps()
                    if '{"ByPassScreenResponse":' not in response : response_list.append(response)

                for i in data :
                    thread = threading.Thread(target=send_request, args=(self.url, i))
                    threads.append(thread)
                    thread.start()
                    time.sleep(3)
                for thread in threads : thread.join()
                response = response_list[0]
                return response
            else :
                try:
                    self.socket.httpsRequest(self.url, request_data, config.request_format().lower())
                    try:
                        response = self.socket.receiveResponsehttps()
                        return response
                    except Exception as e:
                        self.ErrorText = f"Received response Fails @ {self.ip}::{self.port} ==> {e}"
                except Exception as e:
                    self.ErrorText = f"Connection Fails @ {self.ip}::{self.port} ==> {e}"

    def GetStatusRequest(self, RequestType, bypassEnabled, bypassOption) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.GetStatusRequest(RequestType), bypassEnabled, bypassOption)
        except Exception as e: self.ErrorText = f"Error in GetStatusRequest: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def RestartCCTRequestTransaction(self):
        try : self.handleSocketRequest(self.Transaction_Request_Builder.RestartCCTRequest(), "", "")
        except Exception as e: self.ErrorText = f"Error in RestartCCTRequest: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def Signature(self, bypassEnabled, bypassOption) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.SignatureRequest(), bypassEnabled, bypassOption)
        except Exception as e: self.ErrorText = f"Error in Signature: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def displayTicket(self, productCount, bypassEnabled, bypassOption) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.CCTTicketDisplayRequest(productCount), bypassEnabled, bypassOption)
        except Exception : self.ErrorText = f"Error in displayTicket: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def SHOWLIST(self, OptionsType, bypassEnabled, bypassOption) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.ShowListRequest(OptionsType), bypassEnabled, bypassOption)
        except Exception as e :   self.ErrorText = f"Error in SHOWLIST: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def BYPASSTransaction(self, bypassoption) :
        try : self.handleSocketRequest(self.Transaction_Request_Builder.ByPassScreenRequest(bypassoption), False, "")
        except Exception as e :  self.ErrorText = f"Error in Bypass: {e}\nTraceback:\n{traceback.format_exc()}"; self.CLOSETransaction()

    def SHOWSCREEN(self, message, flag, bypassEnabled, bypassOption) :
        try :
            message2 = self.GetUserInput_inputText if self.GetUserInput_inputText else ""
            showscrn = self.Transaction_Request_Builder.ShowScreenRequest(str(message), str(message2), flag)
            self.handleSocketRequest(showscrn, bypassEnabled, bypassOption)
        except Exception as e :
            self.ErrorText = f"Error in SHOWSCREEN: {e}\nTraceback:\n{traceback.format_exc()}"; print(self.ErrorText)
            self.CLOSETransaction()

    def GETUSERINPUT(self, message, option, bypassEnabled, bypassOption) :
        """Get user input."""
        try :
            gui = self.Transaction_Request_Builder.GetUserInputRequest(message, option)
            guiResponse = self.handleSocketRequest(gui, bypassEnabled, bypassOption)
            if guiResponse:
                self.GETUSERINPUT_Request = Excel_Operations.ConvertToJson(gui, self.isXml)
                self.GETUSERINPUT_Response = Excel_Operations.ConvertToJson(guiResponse, self.isXml)
                self.GetUserInput_inputText = self.GETUSERINPUT_Response.get("GetUserInputResponse", {}).get("InputData")
        except Exception as e :
            self.ErrorText = f"Error in GETUSERINPUT: {e}\nTraceback:\n{traceback.format_exc()}"; print(self.ErrorText)
            self.CLOSETransaction()

    def GCBTransaction(self,Transaction_type, AllowKeyedEntry, EntrySource, LookUpFlag, bypassEnabled, bypassOption, Token_type) :
        """Handle GCB transaction and parse the response."""
        try :
            Gcb_Transaction_Req = self.Transaction_Request_Builder.GetCardBINRequest(Transaction_type, AllowKeyedEntry, EntrySource, LookUpFlag)
            GCB_Transaction_res = self.handleSocketRequest(Gcb_Transaction_Req, bypassEnabled, bypassOption)
            if GCB_Transaction_res:
                try:
                    self.Gcb_Transaction_Request = Excel_Operations.ConvertToJson(Gcb_Transaction_Req, self.isXml)
                    self.Gcb_Transaction_Response = Excel_Operations.ConvertToJson(GCB_Transaction_res, self.isXml)
                    self.GcbResponse = self.Gcb_Transaction_Response.get("GetCardBINResponse", {})
                    self.Gcb_Transaction_ResponseCode = self.GcbResponse.get("ResponseCode", "")
                    self.Gcb_Transaction_ResponseText = self.GcbResponse.get("ResponseeText", "")
                    self.Gcb_Transaction_CardType = self.GcbResponse.get("CardType", "")
                    self.Gcb_Transaction_CashbackAmount = self.GcbResponse.get("CashBackAmount", "")
                    if self.Gcb_Transaction_ResponseCode.startswith("0") :
                        self.Gcb_Transaction_CardToken = self.GcbResponse.get("CardToken", "")
                        if LookUpFlag in ["16", "8"] :
                            self.Gcb_Transaction_CIToken = self.GcbResponse.get("ECOMMInfo", {}).get("CardIdentifier", "")
                            self.Gcb_Transaction_CRMToken = self.GcbResponse.get("CRMToken", "")
                        self.tokenForTransaction = {"01" : self.Gcb_Transaction_CardToken, "02" : self.Gcb_Transaction_CIToken, "03" : self.Gcb_Transaction_CRMToken}.get(Token_type, "")
                    else:
                        self.CLOSETransaction()
                except Exception:
                    self.ErrorText = f"Error :: ==> Request/response format not matched. :: Expected ==> { 'XML' if self.isXml else 'JSON' }"

        except Exception as e :
            self.ErrorText = f"Error in GCBTransaction: {e}\nTraceback:\n{traceback.format_exc()}"


    def ParentTransactionProcessing(self,AllowKeyedEntry, productCount, Token_type, TransactionType, TransAmount) :
        try :

            if self.Gcb_Transaction_ResponseCode is None or self.Gcb_Transaction_ResponseCode.startswith("0") :
                Parent_Transaction_req = self.Transaction_Request_Builder.Parent_Transaction(AllowKeyedEntry=AllowKeyedEntry,
                    RandomNumber=self.RandomNumberForInvoice, productCount=productCount, RandomPNR=self.RandomNumberForPNR,
                    Token_type=Token_type, Token=self.tokenForTransaction,
                    TransactionTypeID=TransactionType, CardType=self.Gcb_Transaction_CardType,
                    TransAmount=TransAmount, cashbackAmount=self.Gcb_Transaction_CashbackAmount

                )
                print("PNR:: ", self.RandomNumberForPNR)
                Parent_Transaction_res = self.handleSocketRequest(Parent_Transaction_req, False, "")
                if Parent_Transaction_res:
                    try :
                        self.Parent_Transaction_request = Excel_Operations.ConvertToJson(Parent_Transaction_req, self.isXml)
                        self.Parent_Transaction_response = Excel_Operations.ConvertToJson(Parent_Transaction_res, self.isXml)
                        TransType = self.Parent_Transaction_request.get("TransRequest").get("TransactionType")
                        trans_detail = self.Parent_Transaction_response.get("TransResponse", {}).get("TransDetailsData", {}).get("TransDetailData", {})
                        if isinstance(trans_detail, list) and len(trans_detail) > 0 : trans_detail = trans_detail[0]
                        self.Parent_Transaction_ResponseCode = trans_detail.get("ResponseCode", "")
                        self.Parent_Transaction_ResponseText = trans_detail.get("ResponseText", "")
                        self.Parent_Transaction_TransactionIdentifier = trans_detail.get('TransactionIdentifier', "")
                        self.Parent_Transaction_TransactionAmount = trans_detail.get('TotalApprovedAmount', "")
                        self.isSignatureEnabled = trans_detail.get("SignatureReceiptFlag", "") if trans_detail.get("SignatureReceiptFlag", "") is not None else self.isSignatureEnabled
                        self.Parent_Transaction_AurusPayTicketNum = self.Parent_Transaction_response.get("TransResponse", {}).get("AurusPayTicketNum", "")
                        self.ParentTransactionType = "Sale" if TransType == "01" else "Pre-auth" if TransType == "04" else "Refund w/o Sale" if TransType == "02" else "Gift Transactions"
                        if TransactionType not in ["20", "04_76"]:
                            self.CLOSETransaction()
                    except Exception:
                        self.ErrorText = f"Error :: ==> Request/ response format not matched. :: Expected ==> { 'XML' if self.isXml else 'JSON' }"
                        self.CLOSETransaction()
        except Exception as e :
            self.ErrorText = f"Error in TransRequest: {e}\nTraceback:\n{traceback.format_exc()}"; print(self.ErrorText)
            self.CLOSETransaction()

    print("\n")
    def ChildTransactionProcessing(self, childData, productCount, Child_TransactionType, TransAmount) :
        default_values = {
            'Parent_Transaction_ResponseCode' : self.Parent_Transaction_ResponseCode,
            'Parent_Transaction_TransactionIdentifier' : self.Parent_Transaction_TransactionIdentifier,
            'Parent_Transaction_AurusPayTicketNum' : self.Parent_Transaction_AurusPayTicketNum,
            'Gcb_Transaction_CardType' : self.Gcb_Transaction_CardType,
            'Parent_Transaction_TransactionAmount' : self.Parent_Transaction_TransactionAmount
        }
        print("PNR:: ", self.RandomNumberForPNR)
        if childData is not None :
            childData = json.loads(childData)
            default_values.update({
                'Parent_Transaction_ResponseCode' : childData.get('Parent_Transaction_ResponseCode'),
                'Parent_Transaction_TransactionIdentifier' : childData.get('Parent_Transaction_TransactionIdentifier'),
                'Parent_Transaction_AurusPayTicketNum' : childData.get('Parent_Transaction_AurusPayTicketNum'),
                'Gcb_Transaction_CardType' : childData.get('Parent_Transaction_CardType'),
                'Parent_Transaction_TransactionAmount' : childData.get('Parent_Transaction_TransactionAmount')
            })
        Parent_Transaction_ResponseCode = default_values['Parent_Transaction_ResponseCode']
        Parent_Transaction_TransactionIdentifier = default_values['Parent_Transaction_TransactionIdentifier']
        Parent_Transaction_AurusPayTicketNum = default_values['Parent_Transaction_AurusPayTicketNum']
        Gcb_Transaction_CardType = default_values['Gcb_Transaction_CardType']
        Parent_Transaction_TransactionAmount = default_values['Parent_Transaction_TransactionAmount'] if TransAmount is None else TransAmount
        if Parent_Transaction_ResponseCode is not None and Parent_Transaction_ResponseCode.startswith("0") :
            if Child_TransactionType in {"02", "03", "05", "06", "08", "20", "06_02_01", "04_76"} :
                Child_Transaction = self.Transaction_Request_Builder.Child_Transaction(
                    RandomNumber=self.RandomNumberForInvoice,
                    productCount=productCount,
                    Parent_TransactionID=Parent_Transaction_TransactionIdentifier,
                    Parent_AurusPayTicketNum=Parent_Transaction_AurusPayTicketNum,
                    CardType=Gcb_Transaction_CardType,
                    Transaction_total=Parent_Transaction_TransactionAmount,
                    TransactionTypeID=Child_TransactionType,
                    RandomPNR = self.RandomNumberForPNR
                )

                child_Transaction_res = self.handleSocketRequest(Child_Transaction, False, "")
                if child_Transaction_res:
                    try:
                        self.Child_Transaction_request = Excel_Operations.ConvertToJson(Child_Transaction, self.isXml)
                        self.Child_Transaction_response = Excel_Operations.ConvertToJson(child_Transaction_res, self.isXml)
                        trans_detail = self.Child_Transaction_response.get("TransResponse", {}).get("TransDetailsData", {}).get("TransDetailData", {})
                        if isinstance(trans_detail, list) and len(trans_detail) > 0 : trans_detail = trans_detail[0]
                        self.Child_Transaction_TransactionIdentifier = trans_detail.get("TransactionIdentifier", "")
                        self.Child_Transaction_AurusPayTicketNumber = self.Child_Transaction_response.get("TransResponse", {}).get("AurusPayTicketNum")
                        if Child_TransactionType == "06_02_01":
                            self.CLOSETransaction()
                            Child_Transaction = self.Transaction_Request_Builder.Child_Transaction(
                                RandomNumber=self.RandomNumberForInvoice,
                                productCount=productCount,
                                Parent_TransactionID=self.Child_Transaction_TransactionIdentifier,
                                Parent_AurusPayTicketNum=self.Child_Transaction_AurusPayTicketNumber,
                                CardType=Gcb_Transaction_CardType,
                                Transaction_total=Parent_Transaction_TransactionAmount,
                                TransactionTypeID="06",
                                 RandomPNR = self.RandomNumberForPNR
                            )

                            child_Transaction_res = self.handleSocketRequest(Child_Transaction, False, "")
                        self.Child_Transaction_request = Excel_Operations.ConvertToJson(Child_Transaction, self.isXml)
                        self.Child_Transaction_response = Excel_Operations.ConvertToJson(child_Transaction_res, self.isXml)
                        RequestTop_node = next(iter(self.Child_Transaction_request))
                        ResponseTopNode = next(iter(self.Child_Transaction_response))
                        TransType = self.Child_Transaction_request.get(RequestTop_node, {}).get("TransactionType")
                        trans_detail = self.Child_Transaction_response.get(ResponseTopNode, {}).get("TransDetailsData", {}).get("TransDetailData", {})
                        if isinstance(trans_detail, list) and len(trans_detail) > 0 : trans_detail = trans_detail[0]
                        self.Child_Transaction_ResponseText = trans_detail.get("ResponseText", "")
                        self.Child_Transaction_TransactionIdentifier = trans_detail.get("TransactionIdentifier", "")
                        self.ChildTransactionType = "Refund" if TransType == "02" else "Void" if TransType == "06" else "Post-auth" if TransType == "05" else "CancelLast" if TransType == "76" else None
                        self.CLOSETransaction()
                    except Exception:
                        self.ErrorText = f"Error :: ==> Request/response format not matched. :: Expected ==> { 'XML' if self.isXml else 'JSON' }"
                        self.CLOSETransaction()


    def CLOSETransaction(self) :
        """Close the transaction."""
        try :
           self.handleSocketRequest(self.Transaction_Request_Builder.CloseTransactionRequest(), False, "")
        except Exception as e :
            self.ErrorText = f"Error in CLOSETransaction: {e}\nTraceback:\n{traceback.format_exc()}"; print(self.ErrorText)