import configparser
import os
from Miejer_Petro.settings import BASE_DIR


class config :
    configData = configparser.RawConfigParser()
    configData.read(".\\Config.ini")

    @staticmethod
    def POSID() : return config.configData.get('AESDKParameter', 'POSID')

    @staticmethod
    def CCTID() : return config.configData.get('AESDKParameter', 'CCTID')

    @staticmethod
    def ADSDKSpecVer() : return config.configData.get('AESDKParameter', 'ADSDKSpecVer')

    @staticmethod
    def SessionId() : return config.configData.get('AESDKParameter', 'SessionId')

    @staticmethod
    def LanguageIndicator() : return config.configData.get('AESDKParameter', 'LanguageIndicator')

    @staticmethod
    def commProtocol() : return config.configData.get('SensitiveData', 'wrap_comm_type')

    @staticmethod
    def Instore_file_path() : return config.configData.get('SensitiveData', 'Instore_file_path')

    @staticmethod
    def Outdoor_file_path() : return config.configData.get('SensitiveData', 'Outdoor_file_path')

    @staticmethod
    def Config_machine_ip() : return config.configData.get('SensitiveData', 'MachineIp')

    @staticmethod
    def Config_Indoor_port() : return config.configData.get('SensitiveData', 'Indoor_Port')

    @staticmethod
    def Config_Outdoor_port() : return config.configData.get('SensitiveData', 'outdoor_Port')

    @staticmethod
    def processor() : return config.configData.get('SensitiveData', 'Processor')

    @staticmethod
    def request_format() : return config.configData.get('SensitiveData', 'Indoor_Request_Format')

    @staticmethod
    def Outdoor_request_format() : return config.configData.get('SensitiveData', 'Outdoor_request_Format')

    @staticmethod
    def xls_file_path() : return config.configData.get('SensitiveData', 'card_data_xls')

    @staticmethod
    def API_SEQUENCE() : return config.configData.get("SensitiveData", "API_SEQUENCE")

    @staticmethod
    def OUTDOOR_API_SEQUENCE() : return config.configData.get("SensitiveData", "OUTDOOR_API_SEQUENCE")

    @staticmethod
    def ISSUE_SEQUENCE() : return config.configData.get("SensitiveData", "Issue_Sequence_Testing")

    @staticmethod
    def Full_Outdoor_file_path() : return os.path.join(BASE_DIR, config.Outdoor_file_path())

    @staticmethod
    def Full_Indoor_file_path() : return os.path.join(BASE_DIR, config.Instore_file_path())

    @staticmethod
    def Full_xls_file_path() : return os.path.join(BASE_DIR, config.xls_file_path())

    @staticmethod
    def Indoor_xml_request_path() : return os.path.join(BASE_DIR, config.Instore_file_path() + "XML" + "\\")

    @staticmethod
    def Indoor_json_request_path() : return os.path.join(BASE_DIR, config.Instore_file_path() + "JSON" + "\\")

    @staticmethod
    def Outdoor_xml_request_path() : return os.path.join(BASE_DIR, config.Outdoor_file_path() + "XML" + "\\")

    @staticmethod
    def Outdoor_json_request_path() : return os.path.join(BASE_DIR, config.Outdoor_file_path() + "JSON" + "\\")