import time

from config import config
import re
from datetime import datetime
import socket


def extract_time_and_xml_from_log():
    log_file_path = 'D:\Ganesh\Meijer\Automation_tool\Miejer_Petro\logs.txt'
    format_str = "%Y-%m-%d %H:%M:%S,%f"
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) INFO     \[AesdkLibraryOp\]\s+Final Received Request is in XML Format ::\s+(<(\w+Request)>.*?</\3>)', re.IGNORECASE | re.DOTALL )
    timestamp = []
    requests = []
    orginaltime = "2024-09-10 14:51:54,076"
    with open(log_file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                timestampInlog = match.group(1)
                dt1 = datetime.strptime(timestampInlog, format_str)
                dt2 = datetime.strptime(str(orginaltime), format_str)
                time_difference = (dt1 - dt2)
                time_difference = time_difference.total_seconds()
                request = match.group(2)
                requests.append(request)
                orginaltime = timestampInlog
                timestamp.append(time_difference)
                requests.append(request)
        return timestamp, requests


def perform_operation(delays, request):
    for t, req in zip(delays, request):
        time.sleep(t)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('localhost', 8060))  # Adjust the address and port as needed
            sock.sendall(req.encode())  # Send request, ensuring it's in bytes


#aa = extract_time_and_xml_from_log()
#perform_operation(aa[0], aa[1])