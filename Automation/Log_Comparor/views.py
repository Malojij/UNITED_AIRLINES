from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
from Miejer_Petro.settings import BASE_DIR
from API.config import config
from datetime import datetime
from API.models import API_PARSER
from itertools import zip_longest

class LogComparor:

    def __init__(self):
        self.RequestFormat = config.request_format()
        self.APIPARSER = API_PARSER()
        self.APIPARSER2 = API_PARSER()
        self.DateTimeNow = datetime.now().strftime("%H-%M-%S_%f")  # Use '-' and '_' to avoid invalid characters
        self.logTextification = []
        self.progress_storage = {}
        self.RequestResponsePattern = ""
        self.timePattern = "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+.*?\s+"
        self.apiPattern = "\s*(.*?)(?=\s*\d{4}-\d{2}-\d{2}|\Z)"
        self.allAPIKeys = []
        self.configPatterns = ""

    def CompareLog(self, request):
        if request.method == 'POST' and (request.FILES.get('file1') and request.FILES.get('file2')):
            file1 = request.FILES["file1"]
            file2 = request.FILES["file2"]
            patterns = request.POST.get('patterns', "1")
            self.configPatterns = "|".join(patterns.split(","))
            uploadedFileName = default_storage.save(
                os.path.join(BASE_DIR, "Log", f"{os.path.splitext(file1.name)[0]}_{self.DateTimeNow}{os.path.splitext(file1.name)[1]}"), ContentFile(file1.open("rb").read())
            )
            uploadedFileName2 = default_storage.save(
                os.path.join(BASE_DIR, "Log", f"{os.path.splitext(file2.name)[0]}_{self.DateTimeNow}{os.path.splitext(file2.name)[1]}"), ContentFile(file2.open("rb").read())
            )
            patterns = str(fr"{self.timePattern}(?:{self.configPatterns}){self.apiPattern}")
            logsValidation = self.APIPARSER.parse_log_file(uploadedFileName,patterns)
            logsValidationForFILE2 = self.APIPARSER2.parse_log_file(uploadedFileName2,patterns)
            data = zip_longest(logsValidation, logsValidationForFILE2, fillvalue="")
            data = [{"file1sequence" : File1LogRequestandResponses, "file2sequence" : File2LogRequestandResponses} for File1LogRequestandResponses, File2LogRequestandResponses in data]
            result = {
                "data" : data,
              }
            print(result)
            return JsonResponse(result, safe=False)
        else:
            return render(request, 'Log_Comparor.html')
