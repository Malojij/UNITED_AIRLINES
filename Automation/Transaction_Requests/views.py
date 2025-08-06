import json
from API.Excel_operations import Excel_Operations
from django.shortcuts import render
from lxml import etree


def Transaction_Requests(request):
    if request.method == "POST":
        # Indoor XML
        if request.POST.get('in_xml_req'):
            x = Excel_Operations.Read_indoor_Transrequest("xml", request.POST.get('in_xml_req') + '.xml')
            if not x or not hasattr(x, 'getroot'):
                return render(request, 'Transaction_Requests.html', {
                    "error": f"Invalid or missing XML file: {request.POST.get('in_xml_req')}"
                })
            trn_request = etree.tostring(x.getroot(), pretty_print=True, encoding=str)
            context = {
                "request_for": "Indoor",
                "Format": "XML",
                "request_name": request.POST.get('in_xml_req'),
                "trn_request": trn_request,
            }
            return render(request, 'Transaction_Requests.html', context)

        # Indoor JSON
        elif request.POST.get('in_json_req'):
            data = Excel_Operations.Read_indoor_Transrequest("json", request.POST.get('in_json_req') + ".json")
            if data is False:
                return render(request, 'Transaction_Requests.html', {
                    "error": f"JSON file not found: {request.POST.get('in_json_req')}"
                })
            try:
                Parent_Transaction = json.load(data)
                Parent_Transaction = json.dumps(Parent_Transaction, sort_keys=False, indent=2)
            except Exception as e:
                return render(request, 'Transaction_Requests.html', {
                    "error": f"Failed to parse JSON file: {e}"
                })
            context = {
                "request_for": "Indoor",
                "Format": "JSON",
                "request_name": request.POST.get('in_json_req'),
                "trn_request": Parent_Transaction,
            }
            return render(request, 'Transaction_Requests.html', context)

        # Outdoor XML
        elif request.POST.get('out_xml_req'):
            x = Excel_Operations.Read_outdoor_Transrequest("xml", request.POST.get('out_xml_req') + '.xml')
            if not x or not hasattr(x, 'getroot'):
                return render(request, 'Transaction_Requests.html', {
                    "error": f"Invalid or missing XML file: {request.POST.get('out_xml_req')}"
                })
            trn_request = etree.tostring(x.getroot(), pretty_print=True, encoding=str)
            context = {
                "request_for": "Outdoor",
                "Format": "XML",
                "request_name": request.POST.get('out_xml_req'),
                "trn_request": trn_request,
            }
            return render(request, 'Transaction_Requests.html', context)

        # Outdoor JSON
        elif request.POST.get('out_json_req'):
            data = Excel_Operations.Read_outdoor_Transrequest("json", request.POST.get('out_json_req') + ".json")
            if data is False:
                return render(request, 'Transaction_Requests.html', {
                    "error": f"JSON file not found: {request.POST.get('out_json_req')}"
                })
            try:
                Parent_Transaction = json.load(data)
                Parent_Transaction = json.dumps(Parent_Transaction, sort_keys=False, indent=2)
            except Exception as e:
                return render(request, 'Transaction_Requests.html', {
                    "error": f"Failed to parse JSON file: {e}"
                })
            context = {
                "request_for": "Outdoor",
                "Format": "JSON",
                "request_name": request.POST.get('out_json_req'),
                "trn_request": Parent_Transaction,
            }
            return render(request, 'Transaction_Requests.html', context)

        # Save Request
        elif request.POST.get('save'):
            request_for = request.POST.get('request_for')
            format = request.POST.get('format')
            req = request.POST.get('req')
            content = request.POST.get('handle')
            try:
                Excel_Operations.Write_into_file(request_for, req, format, content=content)
                context = {"success": "Saved successfully."}
            except Exception as e:
                context = {"error": f"Save failed: {str(e)}"}
            return render(request, 'Transaction_Requests.html', context)

    # GET or fallback
    return render(request, 'Transaction_Requests.html')
