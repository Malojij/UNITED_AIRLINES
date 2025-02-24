import datetime
import json
import time

from API.Excel_operations import Excel_Operations
from API.Fleet_Processor import fleet_processor, fleet_data_appender
from API.Gift_Processor import Gift_processor
from API.Product_data_mapping import Product_data_mapping
from API.config import config


class Outdoor_Request_Builder :

    def __init__(self) :
        self.Request = None
        self.POSID = config.POSID()
        self.CCTID = config.CCTID()
        self.SessionId = config.SessionId()
        self.ADSDKSpecVer = config.ADSDKSpecVer()
        self.APPID = "01"
        self.defaultAmount = "10.00"
        self.TodaysDate = datetime.datetime.now().strftime('%m/%d/%Y').replace("/", "")
        self.YYMMDD = datetime.datetime.now().strftime('%y/%m/%d').replace("/", "")
        self.currentTime = time.strftime("%H:%M:%S:%MS", time.localtime()).replace(":", "")[:-3]
        self.RandomNumber = 123456
        self.isXml = config.Outdoor_request_format().upper() == "XML"
        self.ParentTransactionTypeMapping = {
            "01" : "01", "02" : "01", "03" : "01", "15" : "01", "16" : "01", "20" : "01",                       # for sale
            "04" : "04", "05" : "04", "06" : "04", "07" : "04", "09" : "04", "05_01" : "04", "05_09" : "04",     # for pre-auth
            "10" : "09",                                                                                        # for Reversal
            "22" : "02"
        }
        self.ChildTransactionTypeMapping = {
            "02" : "02", "07" : "02",                                                           #for refund
            "03" : "06", "06" : "06",                                                           #for void
            "05" : "05", "05_01" : "05","05_09" : "05",                                                         #for post-auth
            "099" : "09"                                                                        #for reversal of post-auth
        }

    def gcb(self, lookUpFlag, TrackData, EncryptionMode, CardDataSource, EMVDetailsData, PINBlock, KSNBlock, PinBlockMode) :
        data = Excel_Operations.readOutdoorFile("GetCardBINRequest.txt")
        if data :
            data["GetCardBINRequest"].update({
                "POSID" : self.POSID,
                "APPID" : self.APPID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "LookUpFlag" : lookUpFlag,
                "CardDataInfo" : {
                    "CardDataSource" : CardDataSource,
                    "EncryptionMode" : EncryptionMode,
                    "TrackData" : TrackData,
                    "EMVDetailsData" : EMVDetailsData,
                    "PINBlock" : PINBlock,
                    "KSNBlock" : KSNBlock,
                    "PinBlockMode" : PinBlockMode,
                }
            })
            self.Request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.Request

    def Parent_Transaction(self, TransactionSeqNum, TransactionTypeID, TrackData, EncryptionMode, CardDataSource, EMVDetailsData, PINBlock, KSNBlock, PinBlockMode, CardType, TransAmount, productCount) :
        data = Excel_Operations.readOutdoorFile("parentTransRequest.txt")
        if data :
            TransactionTypeToRequest = self.ParentTransactionTypeMapping.get(TransactionTypeID)
            self.defaultAmount = self.defaultAmount if TransAmount == "" else TransAmount
            CardType = "VIC" if CardType is None else CardType
            Parent = data["TransRequest"]
            TransAmountDetails = Parent["TransAmountDetails"]
            Parent.update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "TransactionType" : TransactionTypeToRequest,
                "TransactionSequenceNumber" : str(TransactionSeqNum).zfill(6),
                "CRMToken" : TrackData if TransactionTypeID == "22" else "",
                **(
                    {
                        "SubTransType" : "04" if TransactionTypeToRequest in ("16", "11") else "",
                         "BlackHawkUpc" : Gift_processor.BlackHawkUpc_finder(fleet_processor.cardnumber_finder(TrackData, CardDataSource)),
                         "ProgramId" : "11" if CardType.upper().endswith("P") else "",
                    } if CardType.upper().startswith("GC") else {}
                ),
                "CardType" : CardType,
                **(
                    {"CardDataInfo" :
                        {
                            "CardDataSource" : CardDataSource,
                            "EncryptionMode" : EncryptionMode,
                            "TrackData" : TrackData,
                            "EMVDetailsData" : EMVDetailsData,
                            "PINBlock" : PINBlock,
                            "KSNBlock" : KSNBlock,
                            "PinBlockMode" : PinBlockMode,
                        }
                    } if TransactionTypeID != "22" else {}
                ),
                "ReferenceNumber" : f"{self.TodaysDate}{self.currentTime}{self.RandomNumber}" if CardType.upper() != "EPP" else f"{self.TodaysDate}1234",
                "InvoiceNumber" : f"{self.TodaysDate}{self.currentTime}{self.RandomNumber + 1}",
                "TransactionDate" : self.TodaysDate,
                "TransactionTime" : self.currentTime,
            })
            TransAmountDetails.update({
                "TransactionTotal" : self.defaultAmount,
                "TenderAmount" : self.defaultAmount,
            })
            if int(productCount) != 0 and TransactionTypeToRequest not in "09" and not CardType.upper().endswith("S") :
                productCount = 1 if TransactionTypeToRequest == "04" else int(productCount)
                if config.processor().upper() == "CHASE" and CardType.endswith("D") or CardType.endswith("C") :
                    products = Product_data_mapping.ProductData_Mapping(self.defaultAmount, "", "l3productdata", productCount)
                    Parent.update({
                        "Level3ProductsData" :
                            {"Level3ProductCount" : products['Product_count'],
                             "Level3Products" :
                                 {"Level3Product" : products['Product_list']}
                             }
                    })
                if config.processor().upper() == "FD" or (CardType.endswith("F") and CardType.upper() != "EBF") :
                    products = Product_data_mapping.ProductData_Mapping(self.defaultAmount, "", "fleetproductdata", productCount)
                    Parent.update({
                        "FleetData" :
                            {"FleetProductCount" : products['Product_count'],
                             "FleetProducts" :
                                 {"FleetProduct" : products['Product_list']}}})
            if CardType.endswith('F') and TransactionTypeToRequest.upper() not in ["09", "02"] :
                prompts = fleet_processor.Track_data_prompt_finder(TrackData, CardDataSource, CardType)
                cnumber = fleet_processor.cardnumber_finder(TrackData, CardDataSource)
                prompts_appender = fleet_data_appender.Prompt_finder_by_value(prompts, CardType, cnumber)
                Parent.update({
                    "FleetPromptsData" : prompts_appender
                })
            self.Request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.Request

    def Child_Transaction(self, productCount, TransactionSeqNum, Transaction_Type, CardType, Parent_TransactionID, Parent_AurusPayTicketNum, TransAmount, DuplicateTransCheck) :
        data = Excel_Operations.readOutdoorFile("childTransRequest.txt")
        if data:
            TransactionTypeToRequest = self.ChildTransactionTypeMapping.get(Transaction_Type)
            Parent = data["TransRequest"]
            TransAmountDetails = Parent["TransAmountDetails"]
            Parent.update({
                "APPID" : self.APPID,
                "POSID" : self.POSID,
                "SessionId" : self.SessionId,
                "ADSDKSpecVer" : self.ADSDKSpecVer,
                "TransactionType" : TransactionTypeToRequest,
                "TransactionSequenceNumber" : str(TransactionSeqNum).zfill(6),
                "ReferenceNumber" : f"{self.TodaysDate}{self.RandomNumber}{self.currentTime}" if CardType.upper() != "EPP" else f"{self.TodaysDate}1234",
                "InvoiceNumber" : f"{self.TodaysDate}{self.RandomNumber}{self.currentTime}",
                "TransactionDate" : self.TodaysDate,
                "TransactionTime" : self.currentTime,
                "OrigTransactionIdentifier" : Parent_TransactionID,
                "OrigAurusPayTicketNum" : Parent_AurusPayTicketNum,
                "DuplicateTransCheck" : DuplicateTransCheck,
                "OfflineTicketNumber" : f"O{self.YYMMDD}12345678001" if DuplicateTransCheck == "1" else ""
            })
            TransAmountDetails.update({
                "TransactionTotal" :TransAmount if TransactionTypeToRequest.upper() == "06" else self.defaultAmount,
                "TenderAmount" : TransAmount if TransactionTypeToRequest.upper() == "06" else self.defaultAmount
            })
            if int(productCount) != 0 and TransactionTypeToRequest in ("05", "02") and not CardType.upper().endswith("S") :
                if config.processor().upper() == "CHASE" and (CardType.endswith("D") or CardType.endswith("C")) :
                    products = Product_data_mapping.ProductData_Mapping(self.defaultAmount, "", "l3productdata", productCount)
                    Parent.update({
                        "Level3ProductsData" :
                            {"Level3ProductCount" : products['Product_count'],
                             "Level3Products" :
                                 {"Level3Product" : products['Product_list']}
                             }
                    })
                if config.processor().upper() == "FD" or (CardType.endswith("F") and CardType.upper() != "EBF") :
                    products = Product_data_mapping.ProductData_Mapping(self.defaultAmount, "", "fleetproductdata", productCount)
                    Parent.update({
                        "FleetData" :
                            {"FleetProductCount" : products['Product_count'],
                             "FleetProducts" :
                                 {"FleetProduct" : products['Product_list']}
                             }
                    })
            self.Request = Excel_Operations.ConvertToXml(data) if self.isXml else json.dumps(data)
        return self.Request