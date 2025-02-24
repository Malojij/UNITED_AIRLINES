import xmltodict
import xml.etree.ElementTree as ET
import json
from datetime import datetime
import re


class API_PARSER:

    def __init__(self):
        self.logTextification = []

    def parse_log_file(self, file_path, pattern):
        """Reads the log file and extracts timestamps and JSON/XML data."""
        timedifferences = ["0.000"]
        timestamps = []
        aesdk_requests = []
        APIKeys = []
        with open(file_path, 'r') as file:
            for line in file :
                matches = re.findall(pattern, line.strip(), re.DOTALL)
                if matches:
                    timestamps.append(matches[0][0])
                    aesdk_requests.append(matches[0][1])
        if aesdk_requests:
            for logline in aesdk_requests :
                if logline.startswith("<") and not "<<STX>>" in logline :
                    APIKeys.append(ET.fromstring(logline).tag)
                elif logline.startswith("{") :
                    json_log = json.loads(logline)
                    APIKeys.extend(json_log.keys())
                else :
                    APIKeys.append("PED REQUEST")
        datetime_objects = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S,%f") for ts in timestamps]
        timedifferences.extend(self.calculate_time_differences(datetime_objects))
        return zip(timestamps, aesdk_requests, timedifferences, APIKeys)


    def calculate_time_differences(self, datetime_objects):
        """Calculate time differences between consecutive timestamps."""
        return [(datetime_objects[i] - datetime_objects[i - 1]).total_seconds() for i in range(1, len(datetime_objects))]