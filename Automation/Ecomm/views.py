from django.http import JsonResponse
from django.shortcuts import render
import json

# Create your views here.
from Response_Builder.Instore_response_builder import Transaction_Processing


def Ecomm_Testing(request):
    if request.method == 'POST':
        Transaction_type = request.POST["Trans_type"]
        Iteration = request.POST["Iteration"]
        EntrySource = request.POST["gcb_type"]
        Token_type = "01"
        product_count = int(request.POST["product_count"])
        EntrySource = "" if EntrySource == "00" else "" if EntrySource == "01" else "K" if EntrySource == "02" else "B" if EntrySource == "03" else ""
        AllowKeyedEntry = "N"
        Parent_TransactionType = "Bal_enq" if Transaction_type == "001" else "EPP_Sale" if Transaction_type in ("002", "02") else None
        Child_TransactionType = "Refund" if Transaction_type == "02" else "Void" if Transaction_type in ("03", "06", "08") else "Post_auth" if Transaction_type == "05" else None
        print(f'Performing # {Iteration} Transaction of {Parent_TransactionType} {Child_TransactionType}')
        if Parent_TransactionType is not None or Child_TransactionType is not None:
            result = Transaction_Processing.Ecomm_Transaction_details(Product_count=product_count, Token_type=Token_type, AllowKeyedEntry=AllowKeyedEntry, EntrySource=EntrySource, Request_Type=Transaction_type, Parent_TransactionType=Parent_TransactionType, Child_TransactionType=Child_TransactionType)
            result = json.loads(result)
        else:
            result = ""
        return JsonResponse(result, safe=False)
    else:
        return render(request, "Ecomm_Testing.html")