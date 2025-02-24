import json

from django.shortcuts import render
import re

from .models import decrypt
import base64
# Create your views here.

class Aurus_Decryptor:

    def __init__(self) :
        pass

    def Decryptor(self, request):
        decrypted_data = ""
        if request.method == 'POST':
            Payload = request.POST.get("encryptedRequest", "")
            Payload = re.sub(r'\s+', '', Payload)
            print(Payload)
            Payload = json.loads(Payload)
            print(Payload)
            encryptionFlag = Payload.get("encryptionFlag") if "encryptionFlag" in Payload else Payload.get("EncFlag") if "EncFlag" in Payload else ""
            formFactorId = Payload.get("formFactorId")
            txnDateTime = Payload.get("txnDateTime") if "txnDateTime" in Payload else Payload.get("DateTime") if "DateTime" in Payload else ""
            macAuthData = Payload.get("macAuthData", "").replace("STX", "").replace("ETX", "").split("[FS]")
            response =  Payload.get("response") if "response" in Payload else Payload.get("Payload") if "Payload" in Payload else Payload.get("payload") if "payload" else ""
            response = response.replace("STX", "").replace("ETX", "").split("[FS]")
            macData = macAuthData[2] if len(macAuthData) >= 2 else ""
            responseData = response[2] if encryptionFlag not in ("00", "07") else response[0]
            DataToDecrypt = responseData
            print(DataToDecrypt)
            if encryptionFlag == "00":
                decrypted_data = bytes.fromhex(DataToDecrypt)
                decrypted_data = str(decrypted_data.decode('utf-8'))
            if encryptionFlag == "07":
                decrypted_data = base64.b64decode(DataToDecrypt)
                decrypted_data = str(decrypted_data.decode('utf-8'))
            if encryptionFlag in ("05", "02") :
                static_key = ("K@P!T0!HAP45$IUE5K" + txnDateTime)
                print(f"Encrypted Data :{DataToDecrypt}")
                try:
                    decryptText = decrypt(static_key, DataToDecrypt)
                    decrypted_data = base64.b64decode(decryptText) if encryptionFlag == "05" else decryptText
                    decrypted_data = str(decrypted_data.decode('utf-8'))
                    print(f"Decrypted Text: {decrypted_data}")
                except Exception as e:
                    decrypted_data = f"Decryption Failed : {e}"
            if encryptionFlag in ("01", "03", "06"):
                #deviceSerialNumber = "452406755"
                deviceSerialNumber = request.POST.get("deviceSerialNumber", "")
                static_key = f"5UC355K3Y{deviceSerialNumber}{txnDateTime}"
                print(f"Encrypted Data :{DataToDecrypt}")
                try :
                    decryptText = decrypt(static_key, DataToDecrypt)
                    decrypted_data = base64.b64decode(decryptText) if encryptionFlag in ("00","06") else decryptText
                    decrypted_data = str(decrypted_data.decode('utf-8'))
                except Exception as e :
                    decrypted_data = f"Decryption Failed : {e}"
            print(f"Decrypted Text: {decrypted_data}")
            try:
                decrypted_data = json.dumps(json.loads(decrypted_data), sort_keys=False, indent=4)
            except Exception as e:
                print("unable to convert to json")
            context = {"EncryptedData" : json.dumps(Payload, sort_keys=False, indent=2), "DecryptedData" : decrypted_data}
            return render(request, 'Aurus_Decryptor.html', context)
        return render(request, 'Aurus_Decryptor.html')