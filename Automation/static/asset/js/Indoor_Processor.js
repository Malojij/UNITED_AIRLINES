
// Show loader message
function showLoaderMessage(message) {
    const loaderHtml = `
        <div class="w-100 text-center p-2" id="loader">
            <span style="vertical-align: middle;"><i class="fa fa-solid fa-check" aria-hidden="true"></i></span>
            <span class="m-3">${message}</span>
        </div>`;
    $("#trans_progress").html(loaderHtml).hide().fadeIn(1500);
}

// Update the status message
function updateMessage(message) {
    $('#message').html(`<p class="text-center align-items-center text-danger"><b>${message}</b></p>`);
}

function Refresh(){
    window.location.reload();
}

function onSubmitClick() {

    if($('#gcb_type').val() == "00"){  $('#GcbTypeP').text("Select Entry Mode"); } else {  $('#GcbTypeP').text("") }
    if($('#token_type').val() == "00"){  $('#TokenTypeP').text("Select Token") } else {  $('#TokenTypeP').text("") }
    if($('#Transaction_Type').val() == "00"){  $('#TransactionTypeP').html("Select Transaction") }  else {  $('#TransactionTypeP').text("") }
    if($('#itr').val() == ""){  $('#itrP').html("Enter Iterations") }  else {  $('#itrP').text("") }
    $('#itr').prop('disabled', true);
    $('#submit').prop('disabled', true);
    $('#Transaction_Type').prop('disabled', true);
    $('#myTable').removeClass('d-none');
    if($('#gcb_type').val()  != "00" && $('#token_type').val()  != "00" && $('#Transaction_Type').val()  != "00"){
    table_header = $('<tr id="head1"><th>CardToken</th><th>Test Card</th><th>Request</th><th>EntryMode</th><th>TransType</th><th>CardType</th><th>SubCardType</th><th>TrnsAmt</th><th>ApprovedAmt</th><th>ResponseText</th><th>ResponseCode</th><th>TransactionID</th><th>AurusPayTicketNum</th><th>ApprovalCode</th></tr>').hide();
    $("#table_header").html(table_header);
    $(table_header).fadeIn("slow");
        setTimeout(function() {
            BindConnection();
        }, 0);
    }
    finalizeUI();
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function switchBtn() {
    $(".panel-wrap").toggleClass("panel-unwrap");
    $(".sidepanel").toggleClass("sidepanel-unwrap");
    icon = $(this).find("i");
    if (icon.hasClass("fa-plus")) {
        icon.addClass("fa-minus").removeClass("fa-plus");
    } else {
        icon.addClass("fa-plus").removeClass("fa-minus");
    }
}

function getRandomNumber(min, max, decimalPlaces) {
  // Generate a random number between min (inclusive) and max (exclusive)
  let randomInteger = Math.floor(Math.random() * (max - min + 1)) + min;

  // Format the number with ".00" appended
  return randomInteger + ".00";

  }

function before_data_send(i, message) {
    $('#loader').show();
    a = $('<div id="img">Icon</div><div id="desc">A notification message..</div>').hide();
    str = $('<div class="p-1"><div class="spinner-border text-white" role="status" style="vertical-align: middle;"></div><span class="text-center m-5"># ' + i +' '+message+'</span></div>').hide();
    $("#trans_progress").html(str);
    $(str).fadeIn(1000);
}

function exportToExcel(id, par1, par2) {
    if(id === "0"){ //instore Testing
        let currentDate = new Date();
        var par1 = currentDate.toISOString().slice(0, 10);
        var par2 = currentDate.getHours() + ":" + currentDate.getMinutes() + ":" + currentDate.getSeconds();
        par1.replace("-", "");
        par2.replace("_", "");
        fileName =  'Instore_testing_' + par1 + '_' + par2 + '.xlsx'
    }
    if(id === "1"){ // Dual Processor
        if(par2 === "1"){
            processor = "Chase"
        }else{
            processor = "Worldpay"
        }
        amount = "100."+par1
        fileName = 'DualProcessor_testing_' + processor + '_' + amount + '.xlsx'
    }
     if(id === "2"){ //instore Testing
        let currentDate = new Date();
        var par1 = currentDate.toISOString().slice(0, 10);
        var par2 = currentDate.getHours() + ":" + currentDate.getMinutes() + ":" + currentDate.getSeconds();
        par1.replace("-", "");
        par2.replace("_", "");
        fileName =  'SequenceValidation' + par1 + '_' + par2 + '.xlsx'
    }
    let table = document.getElementsByTagName("table"); // you can use document.getElementById('tableId') as well by providing id to the table tag
    TableToExcel.convert(table[0], { // html code may contain multiple tables so here we are refering to 1st table tag
        name: fileName, // fileName you could use any name
        sheet: {
            name: 'Testing_Result' // sheetName
        }
    });
}

function chaseProcessorResponseCode(code){
    responsecodes =  {
    "00": "Approved authorization or transaction",
    "01": "Refer to card issuer",
    "02": "Refer to card issuer's special conditions",
    "03": "Invalid merchant or terminal",
    "04": "Pick up",
    "05": "Do not honor Note: If this error code was returned on a Mastercard transaction attempted at the point of sale in Europe, the merchant must request additional cardholder authentication prior to resubmitting the transaction.",
    "06": "Error",
    "07": "EFT Velocity parameter record is missing",
    "08": "Approved authorization, Honor with identification",
    "09": "Location Velocity limit has been exceeded",
    "10": "Group Velocity limit has been exceeded",
    "11": "Approved authorization, VIP Approval",
    "12": "Invalid transaction",
    "13": "Invalid amount",
    "14": "Invalid card number",
    "15": "Invalid Issuer",
    "16": "Account not active",
    "17": "Declined per cardholder request",
    "18": "Reversal failed due to transaction already was reversed, was not found, or did not require reversal (error, decline).",
    "19": "Re-enter transaction",
    "20": "A non-CRIN (inside) transaction has been found in the Velocity file",
    "21": "An unknown Velocity error has occurred",
    "23": "Exact duplicate batch detected on upload. Upload not allowed or required.",
    "24": "Batch upload error. Refer to Bit 48 tag ZZ and Bit 62 tag H2.",
    "28": "Declined. Bad authorization number.",
    "30": "Format error, invalid value in message",
    "32": "Duplicate reference number error",
    "33": "Expired card",
    "36": "Additional Cardholder Authentication Required Visa and American Express Only",
    "38": "Invalid PIN",
    "39": "An invalid PIN has been entered the maximum number of times.",
    "40": "Requested function not supported",
    "43": "Lost or stolen card",
    "51": "INSUFFICIENT FUND FOR EBT TRANSACTIONS",
    "54": "Invalid Expiry Date",
    "57": "Tran Not Allowed For Cardholder",
    "58": "Transaction not permitted to terminal",
    "61": "Exceeds withdrawal limits",
    "62": "Restricted Card",
    "63": "MAC not verified or Incorrect MAC",
    "64": "Sender details not provided",
    "65": "Activity count limit exceeded",
    "81": "Invalid PIN block or Security violation",
    "84": "Security Counter error",
    "85": "No keys",
    "86": "ZEK sync error",
    "87": "ZPK sync error",
    "88": "ZAK sync error",
    "91": "Issuer or switch operative",
    "92": "Unable to Determine Network Routing",
    "93": "Busy – Pls Retry",
    "96": "Encryption Error",
    "97": "System Error",
    "98": "Database Error",
    "99": "Unable to send transaction to be authorized by issuer."
}
    return responsecodes[code]

}

function report_Generator(itr, data) {
    requestData = data
    lenData = data.length
    for(let i = 0; i <= lenData; i++){
        if( [i].includes("<")){
           console.log("xml")
        }
        else if(requestData[i].includes("{")){
            console.log("json")
            if(requestData[i].includes("GetCardBINRequest")){
                gcbreqdata = {"GCB_request" :requestData[i], "GCB_response" :  {}, "parent_Request" : {}, "Parent_Response" : {}, "Child_Request" : {}, "Child_Response" : {} }
                Transaction_report(1, gcbreqdata, "")
            }
            if(requestData[i].includes("GetCardBINResponse")){
                gcbresdata = {"GCB_request" : {}, "GCB_response" : requestData[i], "parent_Request" : {}, "Parent_Response" : {}, "Child_Request" : {}, "Child_Response" : {} }
                Transaction_report(1, gcbresdata, "")
            }
            if(requestData[i].includes("TransRequest")){
                Transreqdata = {"GCB_request" : {}, "GCB_response" : {}, "parent_Request" : requestData[i], "Parent_Response" : {}, "Child_Request" : {}, "Child_Response" : {} }
                Transaction_report(1, Transreqdata, "")
            }
            if(requestData[i].includes("TransResponse")){
                Transresdata = {"GCB_request" : {}, "GCB_response" : {}, "parent_Request" : {}, "Parent_Response" : requestData[i], "Child_Request" : {}, "Child_Response" : {} }
                Transaction_report(1, Transresdata, "")
            }
        }
    }
}

function Transaction_report(itr, data, Transaction_type) {
    var error = '<p class="red"><b>'+data.ErrorText+'</p></b>'
    $("#error").html(error)
    let gcbRow = null, parentRow = null, childRow = null, Gcb_Transaction_CardToken = null, rowspan = "0";
    var CARDNAME = null;
    Parent_TransactionType = data.Parent_TransactionType
    Child_TransactionType = data.Child_TransactionType
    requestFormat = data.RequestFormat
    GCB_request = data.GCB_request
	GCB_response = data.GCB_response
	parent_Request = data.Parent_Transaction_request
    Parent_Response = data.Parent_Transaction_response
    Child_Request =  data.Child_Transaction_request
    Child_Response = data.Child_Transaction_response
    if(GCB_response != null) {
        rowspan = "2"
        GCB_UNKN = ""
        GCBRquest = GCB_request.GetCardBINRequest
        GCBResponse = GCB_response.GetCardBINResponse
        Gcb_Transaction_CIToken = GCBResponse?.ECOMMInfo?.CardIdentifier ?? "";
        Gcb_Transaction_CardToken = GCBResponse?.CardToken ?? "";
        Gcb_Transaction_CRMToken = GCBResponse?.CRMToken ?? "";
        Gcb_LookupFlag = GCBRquest?.LookUpFlag ?? "";
        Gcb_Transaction_CardEntryMode = GCBResponse?.CardEntryMode ?? "";
        Gcb_Transaction_CardType = GCBResponse?.CardType ?? "";
        Gcb_Transaction_SubCardType = GCBResponse?.SubCardType ?? "";
        Gcb_Transaction_ResponseText = GCBResponse?.ResponseText ?? "";
        Gcb_Transaction_ResponseCode = GCBResponse?.ResponseCode ?? "";
		Gcb_Transaction_NonFinancialToken = GCBResponse?.NonFinancialToken ?? "";
		CARDNAME =  GCBResponse?.FirstName ?? "";
        gcbRow = $('<tr><td>' + "GCB" + Gcb_LookupFlag +'</td><td>' + Gcb_Transaction_CardEntryMode + '</td><td>' + Gcb_Transaction_NonFinancialToken + '</td><td>' + Gcb_Transaction_CardType + '</td><td>' + Gcb_Transaction_SubCardType + '</td><td>' + GCB_UNKN + '</td><td>' + GCB_UNKN + '</td><td>' + Gcb_Transaction_ResponseText + '</td><td>' + Gcb_Transaction_ResponseCode + '</td><td>' + GCB_UNKN + '</td><td>' + GCB_UNKN + '</td><td>' + GCB_UNKN + '</td></tr>').hide();
   }
    if (Parent_TransactionType != null &&  Parent_Response != null) {
        rowspan = "3"
        parentRequest = parent_Request.TransRequest
        ParentResponse = Parent_Response.TransResponse
        ParentTransactionDetails = (requestFormat === "JSON") ? ParentResponse.TransDetailsData.TransDetailData[0] : ParentResponse.TransDetailsData.TransDetailData;
        if(CARDNAME == null || CARDNAME == ""){
            CARDNAME = ParentTransactionDetails.CustomerName;
        }
        Parent_Transaction_CardNumber = ParentTransactionDetails.CardNumber;
        Parent_Transaction_CIToken = ParentTransactionDetails.CardIdentifier;
        Parent_Transaction_CRMToken = ParentTransactionDetails.CRMToken;
        Parent_Transaction_CardEntryMode = ParentTransactionDetails.CardEntryMode;
        Parent_Transaction_TransactionTypeCode = ParentTransactionDetails.TransactionTypeCode;
        Parent_Transaction_TransactionSequenceNumber = ParentTransactionDetails.TransactionSequenceNumber;
        Parent_Transaction_CardType = ParentTransactionDetails.CardType;
        Parent_Transaction_BalAmount = ParentTransactionDetails.BalanceAmount;
        Parent_Transaction_SubCardType = ParentTransactionDetails.SubCardType;
        Parent_Transaction_requestAmount = parentRequest.TransAmountDetails.TransactionTotal;
        Parent_Transaction_TransactionAmount = ParentTransactionDetails.TotalApprovedAmount;
        Parent_Transaction_ResponseText = ParentTransactionDetails.ResponseText;
        Parent_Transaction_ResponseCode = ParentTransactionDetails.ResponseCode;
        Parent_Transaction_TransactionIdentifier = ParentTransactionDetails?.TransactionIdentifier ?? "";
        Parent_Transaction_AurusPayTicketNum = ParentResponse.AurusPayTicketNum;
        parent_Transaction_ProcessorMerchantId = ParentTransactionDetails.ProcessorMerchantId;
        parent_Transaction_ProcessorResponseCode = ParentTransactionDetails.ProcessorResponseCode;
        Parent_Transaction_ApprovalCode = ParentTransactionDetails.ApprovalCode;
        Parent_Transaction_ProductCount = ParentTransactionDetails.ProductCount;
        Parent_Transaction_ReceiptInfo =  JSON.stringify(ParentTransactionDetails.ReceiptDetails, null, 4)
        Parent_Transaction_FleetPromptsData = JSON.stringify(ParentTransactionDetails.FleetPromptsData, null, 4)
        if (parentRequest.hasOwnProperty("Level3ProductsData") && parentRequest.hasOwnProperty("FleetData")) {
            Parent_Transaction_Products = JSON.stringify("{}", null, 4)
        } else if (parentRequest.hasOwnProperty("Level3ProductsData")) {
            Parent_Transaction_Products = JSON.stringify(parentRequest.Level3ProductsData, null, 4)
        } else if (parentRequest.hasOwnProperty("FleetData")) {
            Parent_Transaction_Products = JSON.stringify(parentRequest.FleetData, null, 4)
        } else if (parentRequest.hasOwnProperty("EPPDetailsInfo")) {
            Parent_Transaction_Products = JSON.stringify(parentRequest.EPPDetailsInfo, null, 4)
        } else {
            Parent_Transaction_Products = JSON.stringify("{}", null, 4)
        }
        const ResponseTextcolor = Parent_Transaction_ResponseText === "APPROVAL"  ? "green" : "red";
        let tcolor = (Parent_Transaction_TransactionIdentifier?.length === 18) ? "green" : "red";
        parentRow = $('<tr><td>' + Parent_TransactionType + '</td><td>' + Parent_Transaction_CardEntryMode + '</td><td>' + Parent_Transaction_TransactionTypeCode + '</td><td>' + Parent_Transaction_CardType + '</td><td>' + Parent_Transaction_SubCardType + '</td><td>' + Parent_Transaction_requestAmount + '</td><td>' + Parent_Transaction_TransactionAmount + '</td><td style="color:' + ResponseTextcolor + '">' + Parent_Transaction_ResponseText +  '</td><td> ' + Parent_Transaction_ResponseCode + '<td style="color:' + tcolor + '">' + Parent_Transaction_TransactionIdentifier + '</td><td>' + Parent_Transaction_AurusPayTicketNum + '</td><td>' + Parent_Transaction_ApprovalCode + '</td></tr>').hide();
        var Parent_owl_data = '<div id="Parent_owl_data' + Parent_Transaction_TransactionIdentifier + '" class="owl-carousel"><div class="item"><p class="text-center">' + ' GCB RESPONSE ' + '</p><hr><pre><code>' + JSON.stringify(GCB_response, null, 4) + '</code></pre></div><div class="item"><p class="text-center">' + ' Receipt ' + '</p><hr><pre><code>' + Parent_Transaction_ReceiptInfo + '</code></pre></div><div class="item"><p class="text-center">' + ' Products ' + '</p><hr><pre><code>' + Parent_Transaction_Products + '</code></pre></div><div class="item"><p class="text-center">' + ' FleetPromptsData ' + '</p><hr><pre><code>' + Parent_Transaction_FleetPromptsData + '</code></pre></div></div>'
        var Parent_data = $('<div class="card ' + ResponseTextcolor + '"><div class="card-header" data-toggle="collapse" href="#collapse_' + Parent_Transaction_TransactionIdentifier + '"><a class="card-link"># ' + Parent_TransactionType + ' Transaction ' + Parent_Transaction_TransactionIdentifier + '</a><i class="fa-solid fa-chevron-down fa-style"></i></div><div id="collapse_' + Parent_Transaction_TransactionIdentifier + '" class="collapse" data-parent="#accordion"><div class="card-body">' + Parent_owl_data + '</div></div></div>').hide();
        $("#accordion").append(Parent_data);
        $(Parent_data).fadeIn("slow");
		$("#Parent_owl_data" + Parent_Transaction_TransactionIdentifier).owlCarousel({
        autoPlay: 3000,
        items: 1,
        margin: 10,
        itemsDesktop: [1199, 1],
        itemsDesktopSmall: [979, 1],
        navigation: false,
        responsiveClass: true,
        responsive: { 0: { items: 1, }, 600: { items: 1, }, 1000: { items: 1, } }
    });
    }
    if (Child_TransactionType != null && Child_Response != null){
        rowspan = "4"
        ChildRequest = (Transaction_type != "20" && Transaction_type != "04_76") ? Child_Request.TransRequest : Child_Request.CancelLastTransRequest;
        transactionType = ChildRequest?.TransactionType ?? "00"
        ChildResponse = (transactionType != "76") ? Child_Response.TransResponse : Child_Response.CancelLastTransResponse
        ChildTransactionDetails = (transactionType == "76") ? ChildTransactionDetails = ChildResponse : (requestFormat === "JSON") ? ChildResponse?.TransDetailsData?.TransDetailData?.[0] ?? "" : ChildResponse?.TransDetailsData?.TransDetailData ?? "";
        Child_Transaction_CardNumber = ChildTransactionDetails?.CardNumber ?? ""
        Child_Transaction_CIToken = ChildTransactionDetails?.CardIdentifier ?? ""
        Child_Transaction_CRMToken = ChildTransactionDetails?.CRMToken ?? ""
        Child_Transaction_CardEntryMode = ChildTransactionDetails?.CardEntryMode ?? ""
        Child_Transaction_TransactionTypeCode = ChildTransactionDetails?.TransactionTypeCode ?? ""
        Child_Transaction_TransactionSequenceNumber = ChildTransactionDetails?.TransactionSequenceNumber ?? ""
        Child_Transaction_CardType = ChildTransactionDetails?.CardType ?? ""
        Child_Transaction_SubCardType = ChildTransactionDetails?.SubCardType ?? ""
        Child_Transaction_requestAmount = ChildRequest?.TransAmountDetails?.TransactionTotal ?? ""
        Child_Transaction_TransactionAmount = ChildTransactionDetails?.TotalApprovedAmount ?? ""
        Child_Transaction_ResponseText = ChildTransactionDetails?.ResponseText ?? ""
        Child_Transaction_ResponseCode = ChildTransactionDetails?.ResponseCode ?? ""
        Child_Transaction_TransactionIdentifier = ChildTransactionDetails?.TransactionIdentifier ?? ""
        Child_Transaction_AurusPayTicketNum = ChildResponse?.AurusPayTicketNum ?? ""
        Child_Transaction_ApprovalCode = ChildTransactionDetails?.ApprovalCode ?? ""
        Child_Transaction_ProductCount = ChildTransactionDetails?.ProductCount ?? ""
        Child_Transaction_ProcessorMerchantId = ChildTransactionDetails?.ProcessorMerchantId ?? ""
        Child_Transaction_ProcessorResponseCode =  ChildTransactionDetails?.ProcessorResponseCode ?? ""
        Child_Transaction_ReceiptInfo = (Transaction_Type !== "20")? JSON.stringify(ChildTransactionDetails?.ReceiptDetails ?? {}, null, 4)  : "";
		Child_Transaction_FleetPromptsData = (Transaction_Type !== "20")?  JSON.stringify(ChildTransactionDetails?.FleetPromptsData ?? {}, null, 4) : "";
        if (ChildRequest.hasOwnProperty("Level3ProductsData") && ChildRequest.hasOwnProperty("FleetData")) {
            Child_Transaction_Products = JSON.stringify("{}", null, 4)
        } else if (ChildRequest.hasOwnProperty("Level3ProductsData")) {
            Child_Transaction_Products = JSON.stringify(ChildRequest.Level3ProductsData, null, 4)
        } else if (ChildRequest.hasOwnProperty("FleetData")) {
            Child_Transaction_Products = JSON.stringify(ChildRequest.FleetData, null, 4)
        } else {
            Child_Transaction_Products = JSON.stringify("{}", null, 4)
        }
        if (Child_Transaction_ResponseText == "APPROVAL" || Child_Transaction_ResponseText == "SUCCESS") {
            var Child_color = "green"
            var Child_Transaction_ResponseText = "<p style='color:green'>" + Child_Transaction_ResponseText + "</p>"
        } else {
            var Child_color = "red"
            var Child_Transaction_ResponseText = "<p style='color:red'>" + Child_Transaction_ResponseText + "</p>"
        }
        let tcolor = (Child_Transaction_TransactionIdentifier?.length === 18) ? "green" : "red";
        childRow = $('<tr><td>' + Child_TransactionType + '</td><td>' + Child_Transaction_CardEntryMode + '</td><td>' + Child_Transaction_TransactionTypeCode + '</td><td>' + Child_Transaction_CardType + '</td><td>' + Child_Transaction_SubCardType + '</td><td>' + Child_Transaction_requestAmount + '</td><td>' + Child_Transaction_TransactionAmount + '</td><td>' + Child_Transaction_ResponseText + '</td><td> ' + Child_Transaction_ResponseCode + '</td><td>' + Child_Transaction_TransactionIdentifier + '</td><td>' + Child_Transaction_AurusPayTicketNum + '</td><td>' + Child_Transaction_ApprovalCode + '</td></tr>').hide();
        var Child_owl_data = '<div id="Child_owl_data' + Child_Transaction_TransactionIdentifier + '" class="owl-carousel"><div class="item"><p class="text-center">' + ' Receipt ' + '</p><hr><pre><code>' + Child_Transaction_ReceiptInfo + '</code></pre></div><div class="item"><p class="text-center">' + ' Products ' + '</p><hr><pre><code>' + Child_Transaction_Products + '</code></pre></div><div class="item"><p class="text-center">' + ' FleetPromptsData ' + '</p><hr><pre><code>' + Child_Transaction_FleetPromptsData + '</code></pre></div></div>'
        var Child_data = $('<div class="card ' + Child_color + '"><div class="card-header" data-toggle="collapse" href="#collapse_' + Child_Transaction_TransactionIdentifier + '"><a class="card-link"># ' + Child_TransactionType + ' Transaction ' + Child_Transaction_TransactionIdentifier + '</a><i class="fa-solid fa-chevron-down fa-style"></i></div><div id="collapse_' + Child_Transaction_TransactionIdentifier + '" class="collapse" data-parent="#accordion"><div class="card-body">' + Child_owl_data + '</div></div></div>').hide();
        $("#accordion").append(Child_data);
        $(Child_data).fadeIn("slow");
		$("#Child_owl_data" + Child_Transaction_TransactionIdentifier).owlCarousel({
        autoPlay: 3000, // Automatically transitions to the next slide every 3 seconds (3000 ms)
        items: 1, // Displays 1 item per slide
        margin: 10, // Adds a 10px margin between items
        itemsDesktop: [1199, 1], // For screens 1199px wide or larger, display 1 item
        itemsDesktopSmall: [979, 1], // For screens between 979px and 1199px, display 1 item
        navigation: false, // Disables navigation buttons (Next/Prev)
        responsiveClass: true, // Enables responsive class switching
        responsive: { 0: { items: 1, }, 600: { items: 1, }, 1000: { items: 1, } }  // On screens smaller than 600/1000px, display 1 i
    });
}
    var first_row = $('<tr><td rowspan="' + rowspan + '">' + Gcb_Transaction_CardToken + '</td><td rowspan="' + rowspan + '">' + CARDNAME + '</td></tr>').hide();
    if (gcbRow != null) {
        $("#divBody").append(first_row); $(first_row).fadeIn("slow");
        $("#divBody").append(gcbRow); $(gcbRow).fadeIn("slow");
    }
    if (parentRow != null) { $("#divBody").append(parentRow); $(parentRow).fadeIn("slow"); }
    if (childRow != null) { $("#divBody").append(childRow); $(childRow).fadeIn("slow"); }
  }

function ChildTransactionOnly(data) {
    // Extract ParentResponse and requestFormat from the input data
    const ParentResponse = data.Parent_Transaction_response?.TransResponse;
    const requestFormat = data.RequestFormat;

    // Ensure ParentResponse is defined
    if (ParentResponse !== undefined) {
        let ParentTransactionDetails;

        // Choose the correct format for ParentTransactionDetails based on requestFormat
        if (requestFormat === "JSON") {
            ParentTransactionDetails = ParentResponse.TransDetailsData?.TransDetailData[0];
        } else {
            ParentTransactionDetails = ParentResponse.TransDetailsData?.TransDetailData;
        }

        // Ensure ParentTransactionDetails is defined
        if (ParentTransactionDetails !== undefined) {
            // Extract required details
            const Parent_Transaction_CardType = ParentTransactionDetails.CardType;
            const Parent_Transaction_TransactionAmount = ParentTransactionDetails.TransactionAmount;
            const Parent_Transaction_ResponseCode = ParentTransactionDetails.ResponseCode;
            const Parent_Transaction_TransactionIdentifier = ParentTransactionDetails.TransactionIdentifier;
            const Parent_Transaction_AurusPayTicketNum = ParentResponse.AurusPayTicketNum;

            // Create and return the JSON object
            const transdata = {
                "Parent_Transaction_CardType": Parent_Transaction_CardType,
                "Parent_Transaction_TransactionAmount": Parent_Transaction_TransactionAmount,
                "Parent_Transaction_ResponseCode": Parent_Transaction_ResponseCode,
                "Parent_Transaction_TransactionIdentifier": Parent_Transaction_TransactionIdentifier,
                "Parent_Transaction_AurusPayTicketNum": Parent_Transaction_AurusPayTicketNum,
            };
            return transdata;
        }
    }
    // Return null or an empty object if the conditions are not met
    return null;
}

function finalizeUI() {
    $("#loader").remove();
    $('#itr').prop('disabled', false);
    $('#submit').prop('disabled', false);
    $('#Transaction_Type').prop('disabled', false);
    $('#export_btn').removeClass('d-none');
    $('#message').html('<p class="text-center text-danger"><b>Iteration Completed</b></p>').fadeIn(1500);
}