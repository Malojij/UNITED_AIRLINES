import json

from API.Excel_operations import Excel_Operations
from django.shortcuts import render
from lxml import etree


def Transaction_Requests(request):
    if request.method == "POST" and request.POST.get('in_xml_req'):
        x = Excel_Operations.Read_indoor_Transrequest("xml", request.POST.get('in_xml_req') + '.xml')
        trn_request = etree.tostring(x, pretty_print=True, encoding=str)
        context = {
            "request_for": "Indoor",
            "Format": "XML",
            "request_name": request.POST.get('in_xml_req'),
            "trn_request": trn_request,
        }
        return render(request, 'Transaction_Requests.html', context)
    if request.method == "POST" and request.POST.get('in_json_req'):
        data = Excel_Operations.Read_indoor_Transrequest("json", request.POST.get('in_json_req') + ".json")
        Parent_Transaction = json.load(data)
        Parent_Transaction = json.dumps(Parent_Transaction, sort_keys=False, indent=2)
        context = {
            "request_for": "Indoor",
            "Format": "JSON",
            "request_name": request.POST.get('in_json_req'),
            "trn_request": Parent_Transaction,
        }
        return render(request, 'Transaction_Requests.html', context)
    if request.method == "POST" and request.POST.get('out_xml_req'):
        x = Excel_Operations.Read_outdoor_Transrequest("xml", request.POST.get('out_xml_req') + '.xml')
        trn_request = etree.tostring(x, pretty_print=True, encoding=str)
        context = {
            "request_for": "Outdoor",
            "Format": "XML",
            "request_name": request.POST.get('out_xml_req'),
            "trn_request": trn_request,
        }
        return render(request, 'Transaction_Requests.html', context)
    if request.method == "POST" and request.POST.get('out_json_req'):
        data = Excel_Operations.Read_outdoor_Transrequest("json", request.POST.get('out_json_req') + ".json")
        Parent_Transaction = json.load(data)
        Parent_Transaction = json.dumps(Parent_Transaction, sort_keys=False, indent=2)
        context = {
            "request_for": "Outdoor",
            "Format": "JSON",
            "request_name": request.POST.get('out_json_req'),
            "trn_request": Parent_Transaction,
        }
        return render(request, 'Transaction_Requests.html', context)
    if request.method == "POST" and request.POST.get('save'):
        print(request.POST["request_for"])
        request_for = request.POST['request_for']
        format = request.POST['format']
        req = request.POST['req']
        content = request.POST['handle']
        A = Excel_Operations.Write_into_file(request_for, req, format, content=content)
        context = {
            "success": "success",
        }
        return render(request, 'Transaction_Requests.html', context)
    else:
        return render(request, 'Transaction_Requests.html')
