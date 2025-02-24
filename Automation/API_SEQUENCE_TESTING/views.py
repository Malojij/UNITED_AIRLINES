import json
import os
import time
from datetime import datetime

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render

from API.Socket_API import Adsdk_Socket as socket
from API.config import config
from API.models import API_PARSER
from Miejer_Petro.settings import BASE_DIR


class ISSUE_SEQUENCE_TESTING :
    def __init__(self) :
        self.APIPARSER = API_PARSER()
        self.DateTimeNow = datetime.now().strftime("%H-%M-%S_%f")
        self.timePattern = "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+.*?\s+"
        self.apiPattern = "\s*(.*?)(?=\s*\d{4}-\d{2}-\d{2}|\Z)"

        self.patterns = {}
        self.allAPIKeys = []
        self.socketConnection = socket()
        self.port = config.Config_Indoor_port()
        self.comm = config.commProtocol()
        self.configPatterns = ""
        self.ip = config.Config_machine_ip()
        self.urlExtension = ""
        self.APIurl = ""
        self.url = rf"https://{self.ip}:{self.port}{self.urlExtension}{self.APIurl}"

    def issue_sequence_testing(self, request) :
        if request.method == 'POST' :
            if request.FILES.get('file') :
                return render(request, 'API_SEQUENCE_TESTING.html', self.handle_file_upload(request))
            return self.handle_api_request(request)
        return render(request, 'API_SEQUENCE_TESTING.html')

    def handle_api_request(self, request) :
        if not request.POST.get("Scenario") : return JsonResponse({'status' : 'error', 'message' : 'Scenario not provided'}, status=400)
        timediff = max(float(request.POST.get("timediffArray", 0)) - 30 / 1000, 0.020)
        apiRequestArray = request.POST.get("apiRequestArray", "")
        if apiRequestArray.startswith("{") :
            apiRequestArray = json.loads(apiRequestArray)
        currentAPI, nextAPI = request.POST.get("currentAPI", ""), request.POST.get("nextAPI", "")
        if "Request" in currentAPI :
            if self.comm == "5" :
                self.socketConnection.httpsRequest(self.url, apiRequestArray, "")
            else :
                self.socketConnection.openSocket(self.port)
                self.socketConnection.sendRequest(str(apiRequestArray))
        if "Response" in nextAPI :
            if self.comm == "5" :
                res = self.socketConnection.receiveResponsehttps()
            else:
                res = self.socketConnection.receiveResponseFromSocket()
            print(f"Received response: {res}")
        elif "Request" in nextAPI :
            time.sleep(float(timediff))
            print(f"Time delay added : {timediff}")
        return JsonResponse({'status' : 'complete', 'nexttimestampASID' : request.POST.get("nexttimestampASID", "")}, status=200)

    def handle_file_upload(self, request) :
        patterns = request.POST.get('patterns', "1")
        uploadedFileName = default_storage.save(
            os.path.join(BASE_DIR, "Log", f"{os.path.splitext(request.FILES['file'].name)[0]}_{self.DateTimeNow}{os.path.splitext(request.FILES['file'].name)[1]}"),
            ContentFile(request.FILES['file'].read())
        )
        self.configPatterns = "|".join(patterns.split(","))
        print(self.configPatterns)
        patterns = str(fr"{self.timePattern}(?:{self.configPatterns}){self.apiPattern}")
        logsValidation = self.APIPARSER.parse_log_file(uploadedFileName, patterns)
        data_list = [{'timestamp' : ts, 'api_request' : req, "allAPIKeys" : keys,"timedifferences" : time} for ts, req, time, keys in logsValidation]
        context = {'data' : data_list, 'message' : 'File uploaded successfully'}
        return context
