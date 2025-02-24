function before_data_send(i, message) {
    $('#loader').show();
    a = $('<div id="img">Icon</div><div id="desc">A notification message..</div>').hide();
    str = $('<div class="p-1"><div class="spinner-border text-white" role="status" style="vertical-align: middle;"></div><span class="text-center m-5"># ' + i +' '+message+'</span></div>').hide();
    $("#trans_progress").html(str);
    $(str).fadeIn(1000);
}

function finalizeUI() {
    $("#loader").remove();
    $('#itr').prop('disabled', false);
    $('#submit').prop('disabled', false);
    $('#Transaction_Type').prop('disabled', false);
    $('#export_btn').removeClass('d-none');
    $('#message').html('<p class="text-center text-danger"><b>Iteration Completed</b></p>').fadeIn(1500);
}

function onSubmitClick(){
    var g = document.getElementById('Transaction_Type').validity.valid;
    var t = document.getElementById('cds').validity.valid;
    if (g == false || t == false){
        alert("data missing");
    }
    else{
        $('#cds').prop('disabled', true);
        $('#submit').prop('disabled', true);
        $('#Transaction_Type').prop('disabled', true);
        $('#gcb_type').prop('disabled', true);
        $('#OnPinkey').prop('disabled', true);
        $('#product_count').prop('disabled', true);
        table_header = $('<tr id="head1"><th>CardToken</th><th>Request</th><th>EntryMode</th><th>TransType</th><th>SeqNum</th><th>ExpectedCardType</th><th>ActualCardType</th><th>SubCardType</th><th>TrnsAmt</th><th>ApprovedAmt</th><th>ResponseText</th><th>ResponseCode</th><th>TransactionID</th><th>AurusPayTicketNum</th><th>ApprovalCode</th></tr>').hide();
        $("#table_header").html(table_header);
        $(table_header).fadeIn("slow");
        setTimeout(function() {
            readExcel();
        }, 500);
    }
   }

function updateMessage(message) {
    $('#message').html(`<p class="text-center align-items-center text-danger"><b>${message}</b></p>`);
}

function showLoaderMessage(message) {
    const loaderHtml = `
        <div class="w-100 text-center p-2" id="loader">
            <span style="vertical-align: middle;"><i class="fa fa-solid fa-check" aria-hidden="true"></i></span>
            <span class="m-3">${message}</span>
        </div>`;
    $("#trans_progress").html(loaderHtml).hide().fadeIn(1500);
}

function switchBtn() {
    $(".panel-wrap").toggleClass("panel-unwrap");
    $(".sidepanel").toggleClass("sidepanel-unwrap");
    icon = $(this).find("i");
    if (icon.hasClass("fa-plus")){
        icon.addClass("fa-minus").removeClass("fa-plus");
      }else{
        icon.addClass("fa-plus").removeClass("fa-minus");
      }
}

function after_data_receive(data){
    if (data[0]["Error_count"] == "1") {
            $('#submit').prop('disabled', false);
            $('#cds').prop('disabled', false);
            $('#Transaction_Type').prop('disabled', false);
            $('#gcb_type').prop('disabled', false);
            $("#OnPinkey").prop('disabled', false);
			$('#product_count').prop('disabled', false);
            $('#trans_progress').hide();
            $("#table_header").hide();
			
         } else {
            str = $('<div data-aos-easing="ease" data-aos-duration="1000" data-aos-delay="0" class="w-100 text-center p-2" id="loader"><span style="vertical-align: middle;"><i class="fa fa-solid fa-check" aria-hidden="true"></i></span><span class="m-3">Transaction completed</span></div>').hide();
           $("#trans_progress").html(str);
           $(str).fadeIn(1500);
            setTimeout(function() {
               $("#loader").remove();
               $('#submit').prop('disabled', false);
               $('#cds').prop('disabled', false);
               $('#Transaction_Type').prop('disabled', false);
               $('#gcb_type').prop('disabled', false);
               $("#OnPinkey").prop('disabled', false);
			   $('#product_count').prop('disabled', false);
               $('#export_btn').removeClass('d-none');
               $("#ErrorDiv").html("")
            }, 2000);
         }
}

function exportToExcel() {
   let table = document.getElementsByTagName("table"); // you can use document.getElementById('tableId') as well by providing id to the table tag
   let currentDate = new Date();
   var today = currentDate.toISOString().slice(0, 10);
   var time = currentDate.getHours() + ":" + currentDate.getMinutes() + ":" + currentDate.getSeconds();
   today.replace("-", "");
   time.replace("_", "");
   TableToExcel.convert(table[0], { // html code may contain multiple tables so here we are refering to 1st table tag
      name: 'Outdoor_testing_'+today+'_'+time+'.xlsx', // fileName you could use any name
      sheet: {
         name: 'Testing_Result' // sheetName
      }
   });
}

function Transaction_report(response, Transaction_type, starttime, iteration) {
    var error = '<p class="red"><b>'+response.ErrorText+'</p></b>'
    $("#Error").html(error)
    requestFormat = response.requestFormat
    Parent_TransactionType = response.Parent_TransactionType
    Child_TransactionType = response.Child_TransactionType
    Gcb_TransactionType = response.GCB_TransactionType
    TrackData = response.TrackData.replace("%B", "").split('^')[0];
    Parent_Transaction_CardNumber = TrackData;
    Expectedcardtype = response?.Expectedcardtype ?? "";
    GCB_request = response.GCB_request.GetCardBINRequest
    GCB_response = response.GCB_response.GetCardBINResponse
    parentRequest = response.Parent_Transaction_request.TransRequest
    ParentResponse = response.Parent_Transaction_response.TransResponse
    ChildRequest = response.Child_Transaction_request.TransRequest
    ChildResponse = response.Child_Transaction_response.TransResponse
    GCB_UNKN = ""
    Gcb_fleet_prompts = GCB_response?.FleetPromptsFlag ?? "";
    Gcb_Transaction_CIToken = GCB_response?.ECOMMInfo?.CardIdentifier ?? "";
    Gcb_Transaction_CardToken = GCB_response?.CardToken ?? "";
    Gcb_Transaction_CRMToken = GCB_response?.CRMToken ?? "";
    Gcb_Transaction_CardEntryMode = GCB_response?.CardEntryMode ?? "";
    Gcb_Transaction_CardType = GCB_response.CardType ?? "";
    Gcb_Transaction_SubCardType = GCB_response?.SubCardType ?? "";
    Gcb_Transaction_ResponseText = GCB_response?.ResponseText ?? "";
    Gcb_Transaction_ResponseCode = GCB_response?.ResponseCode ?? "";
    Gcb_Transaction_TransactionID = GCB_response?.TransactionIdentifier ?? "";
    const GCBResponseTextcolor = Gcb_Transaction_ResponseText === "Approved" ? "green" : "red";
    var gcb = $('<tr><td>' + "GCB" + '</td><td>' + Gcb_Transaction_CardEntryMode + '</td><td>' + GCB_UNKN + '</td><td>' + GCB_UNKN + '</td><td>' + Expectedcardtype + '</td><td>' + Gcb_Transaction_CardType + '</td><td>' + Gcb_Transaction_SubCardType + '</td><td>' + GCB_UNKN + '</td><td>' + GCB_UNKN + '</td><td>' + Gcb_Transaction_ResponseText + '</td><td>' + Gcb_Transaction_ResponseCode + '</td><td>' + Gcb_Transaction_TransactionID + '</td><td>' + GCB_UNKN + '</td><td>' + GCB_UNKN + '</td></tr>').hide();
    var gcb_owl_data = '<div id="gcb_owl_data' + iteration + '" class="owl-carousel"><div class="item"><p class="text-center">' + ' GCB Request ' + '</p><hr><pre><code>' + JSON.stringify(GCB_request, null, 4) + '</code></pre></div><div class="item"><p class="text-center">' + ' GCB Response ' + '</p><hr><pre><code>' + JSON.stringify(GCB_response, null, 4) + '</code></pre></div></div>'
    var gcb_data = $('<div class="card ' + GCBResponseTextcolor + '"><div class="card-header" data-toggle="collapse" href="#collapseGCB_' + iteration + '"><a class="card-link"># ' + "GCB" + ' Transaction ' + iteration + '</a><i class="fa-solid fa-chevron-down fa-style"></i></div><div id="collapseGCB_' + iteration + '" class="collapse" data-parent="#accordion"><div class="card-body">' + gcb_owl_data + '</div></div></div>').hide();

    if (ParentResponse != undefined) {
        console.log(requestFormat)
        ParentTransactionDetails = (requestFormat === "JSON") ? ParentResponse.TransDetailsData.TransDetailData[0] : ParentResponse.TransDetailsData.TransDetailData;
        console.log(ParentTransactionDetails)
        Parent_Transaction_CardNumber = ParentTransactionDetails.CardNumber;
        Parent_Transaction_CIToken = ParentTransactionDetails?.CardIdentifier ?? "";
        Parent_Transaction_CRMToken = ParentTransactionDetails?.CRMToken ?? "";
        Parent_Transaction_CardEntryMode = ParentTransactionDetails?.CardEntryMode ?? "";
        Parent_Transaction_TransactionTypeCode = ParentTransactionDetails?.TransactionTypeCode ?? "";
        Parent_Transaction_TransactionSequenceNumber = ParentTransactionDetails?.TransactionSequenceNumber ?? "";
        Parent_Transaction_CardType = ParentTransactionDetails?.CardType ?? "";
        Parent_Transaction_SubCardType = ParentTransactionDetails?.SubCardType ?? "";
        Parent_Transaction_requestAmount = parentRequest?.TransAmountDetails?.TransactionTotal ?? "";
        Parent_Transaction_TransactionAmount = ParentTransactionDetails?.TransactionAmount ?? "";
        Parent_Transaction_ResponseText = ParentTransactionDetails?.ResponseText ?? "";
        Parent_Transaction_ResponseCode = ParentTransactionDetails?.ResponseCode ?? "";
        Parent_Transaction_TransactionIdentifier = ParentTransactionDetails?.TransactionIdentifier ?? "";
        Parent_Transaction_AurusPayTicketNum = ParentResponse?.AurusPayTicketNum ?? "";
        Parent_Transaction_ApprovalCode = ParentTransactionDetails?.ApprovalCode ?? "";
        Parent_Transaction_ProductCount = ParentTransactionDetails?.ProductCount ?? "";
        Parent_Transaction_ReceiptInfo = JSON.stringify(ParentTransactionDetails.ReceiptDetails, null, 4)
        Parent_Transaction_FleetPromptsData = JSON.stringify(ParentTransactionDetails.FleetPromptsData, null, 4)
        const productstoCheck = ["Level3ProductsData", "FleetData", "EPPDetailsInfo"];
        let foundData = null;
        for (const key of productstoCheck) {
            if (parentRequest.hasOwnProperty(key)) {
                foundData = parentRequest[key];
                break; // Exit loop once the first match is found
            }
        }
        Parent_Transaction_Products = JSON.stringify(foundData || {}, null, 4);
        const ResponseTextcolor = Parent_Transaction_ResponseText === "APPROVAL" ? "green" : "red";
        let tcolor = (Parent_Transaction_TransactionIdentifier?.length === 18) ? "green" : "red";
        var parent = $('<tr><td>' + Parent_TransactionType + '</td><td>' + Parent_Transaction_CardEntryMode + '</td><td>' + Parent_Transaction_TransactionTypeCode + '</td><td>' + Parent_Transaction_TransactionSequenceNumber + '</td><td>' + Expectedcardtype + '</td><td>' + Parent_Transaction_CardType + '</td><td>' + Parent_Transaction_SubCardType + '</td><td>' + Parent_Transaction_requestAmount + '</td><td>' + Parent_Transaction_TransactionAmount + '</td><td style="color:' + ResponseTextcolor + '">' + Parent_Transaction_ResponseText + '</td><td> ' + Parent_Transaction_ResponseCode + '<td style="color:' + tcolor + '">' + Parent_Transaction_TransactionIdentifier + '</td><td>' + Parent_Transaction_AurusPayTicketNum + '</td><td>' + Parent_Transaction_ApprovalCode + '</td></tr>').hide();
        var Parent_owl_data = '<div id="Parent_owl_data' + Parent_Transaction_TransactionIdentifier + '" class="owl-carousel"><div class="item"><p class="text-center">' + ' GCB Response ' + '</p><hr><pre><code>' + JSON.stringify(GCB_response, null, 4) + '</code></pre></div><div class="item"><p class="text-center">' + ' Receipt ' + '</p><hr><pre><code>' + Parent_Transaction_ReceiptInfo + '</code></pre></div><div class="item"><p class="text-center">' + ' Products ' + '</p><hr><pre><code>' + Parent_Transaction_Products + '</code></pre></div><div class="item"><p class="text-center">' + ' FleetPromptsData ' + '</p><hr><pre><code>' + Parent_Transaction_FleetPromptsData + '</code></pre></div></div>'
        var Parent_data = $('<div class="card ' + ResponseTextcolor + '"><div class="card-header" data-toggle="collapse" href="#collapse_' + Parent_Transaction_TransactionIdentifier + '"><a class="card-link"># ' + Parent_TransactionType + ' Transaction ' + Parent_Transaction_TransactionIdentifier + '</a><i class="fa-solid fa-chevron-down fa-style"></i></div><div id="collapse_' + Parent_Transaction_TransactionIdentifier + '" class="collapse" data-parent="#accordion"><div class="card-body">' + Parent_owl_data + '</div></div></div>').hide();

    }
    if (ChildResponse != undefined) {
        ChildTransactionDetails = (requestFormat === "JSON") ? ChildResponse.TransDetailsData.TransDetailData[0] : ChildResponse.TransDetailsData.TransDetailData;
        Child_Transaction_CardNumber = ChildTransactionDetails.CardNumber
        Child_Transaction_CIToken = ChildTransactionDetails.CardIdentifier
        Child_Transaction_CRMToken = ChildTransactionDetails.CRMToken
        Child_Transaction_CardEntryMode = ChildTransactionDetails.CardEntryMode
        Child_Transaction_TransactionTypeCode = ChildTransactionDetails.TransactionTypeCode
        Child_Transaction_TransactionSequenceNumber = ChildTransactionDetails.TransactionSequenceNumber
        Child_Transaction_CardType = ChildTransactionDetails.CardType
        Child_Transaction_SubCardType = ChildTransactionDetails.SubCardType
        Child_Transaction_requestAmount = ChildRequest.TransAmountDetails.TransactionTotal
        Child_Transaction_TransactionAmount = ChildTransactionDetails.TransactionAmount
        Child_Transaction_ResponseText = ChildTransactionDetails.ResponseText
        Child_Transaction_ResponseCode = ChildTransactionDetails.ResponseCode
        Child_Transaction_TransactionIdentifier = ChildTransactionDetails.TransactionIdentifier
        Child_Transaction_AurusPayTicketNum = ChildResponse.AurusPayTicketNum
        Child_Transaction_ApprovalCode = ChildTransactionDetails.ApprovalCode
        Child_Transaction_ProductCount = ChildTransactionDetails.ProductCount
        Child_Transaction_FleetPromptsData = JSON.stringify(ChildTransactionDetails.FleetPromptsData, null, 4)
        Child_Transaction_ReceiptInfo = JSON.stringify(ChildTransactionDetails.ReceiptDetails, null, 4)

        if (ChildRequest.hasOwnProperty("Level3ProductsData") && ChildRequest.hasOwnProperty("FleetData")) {
            Child_Transaction_Products = JSON.stringify("{}", null, 4)
        } else if (ChildRequest.hasOwnProperty("Level3ProductsData")) {
            Child_Transaction_Products = JSON.stringify(ChildRequest.Level3ProductsData, null, 4)
        } else if (ChildRequest.hasOwnProperty("FleetData")) {
            Child_Transaction_Products = JSON.stringify(ChildRequest.FleetData, null, 4)
        } else {
            Child_Transaction_Products = JSON.stringify("{}", null, 4)
        }
        const childResponseTextcolor = Child_Transaction_ResponseText === "APPROVAL" ? "green" : "red";
        let childtcolor = (Child_Transaction_TransactionIdentifier?.length === 18) ? "green" : "red";
        var child = $('<tr><td>' + Child_TransactionType + '</td><td>' + Child_Transaction_CardEntryMode + '</td><td>' + Child_Transaction_TransactionTypeCode + '</td><td>' + Child_Transaction_TransactionSequenceNumber + '</td><td>' + Expectedcardtype + '</td><td>' + Child_Transaction_CardType + '</td><td>' + Child_Transaction_SubCardType + '</td><td>' + Child_Transaction_requestAmount + '</td><td>' + Child_Transaction_TransactionAmount + '</td><td td style="color:' + childResponseTextcolor + '">' + Child_Transaction_ResponseText + '</td><td> ' + Child_Transaction_ResponseCode + '</td><td>' + Child_Transaction_TransactionIdentifier + '</td><td>' + Child_Transaction_AurusPayTicketNum + '</td><td>' + Child_Transaction_ApprovalCode + '</td></tr>').hide();
        var Child_owl_data = '<div id="Child_owl_data' + Child_Transaction_TransactionIdentifier + '" class="owl-carousel"><div class="item"><p class="text-center">' + ' Receipt ' + '</p><hr><pre><code>' + Child_Transaction_ReceiptInfo + '</code></pre></div><div class="item"><p class="text-center">' + ' Products ' + '</p><hr><pre><code>' + Child_Transaction_Products + '</code></pre></div><div class="item"><p class="text-center">' + ' FleetPromptsData ' + '</p><hr><pre><code>' + Child_Transaction_FleetPromptsData + '</code></pre></div></div>'
        var Child_data = $('<div class="card ' + childtcolor + '"><div class="card-header" data-toggle="collapse" href="#collapse_' + Child_Transaction_TransactionIdentifier + '"><a class="card-link"># ' + Child_TransactionType + ' Transaction ' + Child_Transaction_TransactionIdentifier + '</a><i class="fa-solid fa-chevron-down fa-style"></i></div><div id="collapse_' + Child_Transaction_TransactionIdentifier + '" class="collapse" data-parent="#accordion"><div class="card-body">' + Child_owl_data + '</div></div></div>').hide();
    }
    if (Transaction_type == "00") {
        var rowspan = "2"
    }
    if ((Transaction_type == "01") || (Transaction_type == "04") || (Transaction_type == "07") || (Transaction_type == "10") || (Transaction_type == "11") || (Transaction_type == "12")) {
        var rowspan = "3"
    }
    if ((Transaction_type == "02") || (Transaction_type == "03") || (Transaction_type == "05") || (Transaction_type == "06") || (Transaction_type == "08") || (Transaction_type == "09")) {
        var rowspan = "4"
    }
    if ((Transaction_type == "00") || (Transaction_type == "01") || (Transaction_type == "04") || (Transaction_type == "07") || (Transaction_type == "02") || (Transaction_type == "03") || (Transaction_type == "05") || (Transaction_type == "06") || (Transaction_type == "08") || (Transaction_type == "09")) {
        var first_row = $('<tr><td rowspan="' + rowspan + '">' + Parent_Transaction_CardNumber + '</td></tr>').hide();
        $("#divBody").append(first_row)
        $(first_row).fadeIn("slow");
        $("#divBody").append(gcb)
        $(gcb).fadeIn("slow");
    }

    if((Transaction_type == "00")){
        $("#accordion").append(gcb_data);
        $(gcb_data).fadeIn("slow");
        $("#gcb_owl_data" + iteration).owlCarousel({
            autoPlay: 3000,
            items: 3,
            margin: 10,
            itemsDesktop: [1199, 1],
            itemsDesktopSmall: [979, 1],
            navigation: false,
            responsiveClass: true,
            responsive: {
                0: {
                    items: 1,

                },
                600: {
                    items: 1,

                },
                1000: {
                    items: 1,

                }
            }

        });

    }
    if ((Transaction_type == "01") || (Transaction_type == "04") || (Transaction_type == "07") || (Transaction_type == "02") || (Transaction_type == "03") || (Transaction_type == "05") || (Transaction_type == "06") || (Transaction_type == "08") || (Transaction_type == "09") || (Transaction_type == "10") || (Transaction_type == "11") || (Transaction_type == "12")) {
        $("#divBody").append(parent)
        $(parent).fadeIn("slow");
        $("#accordion").append(Parent_data);
        $(Parent_data).fadeIn("slow");
        $("#Parent_owl_data" + Parent_Transaction_TransactionIdentifier).owlCarousel({
            autoPlay: 3000,
            items: 3,
            margin: 10,
            itemsDesktop: [1199, 1],
            itemsDesktopSmall: [979, 1],
            navigation: false,
            responsiveClass: true,
            responsive: {
                0: {
                    items: 1,

                },
                600: {
                    items: 1,

                },
                1000: {
                    items: 1,

                }
            }

        });
    }
    if ((Transaction_type == "02") || (Transaction_type == "03") || (Transaction_type == "05") || (Transaction_type == "06") || (Transaction_type == "08") || (Transaction_type == "09")) {
        $("#divBody").append(child);
        $(child).fadeIn("slow");
        $("#accordion").append(Child_data);
        $(Child_data).fadeIn("slow");
        $("#Child_owl_data" + Child_Transaction_TransactionIdentifier).owlCarousel({
            autoPlay: 3000,
            items: 3,
            margin: 10,
            itemsDesktop: [1199, 1],
            itemsDesktopSmall: [979, 1],
            navigation: false,
            responsiveClass: true,
            responsive: {
                0: {
                    items: 1,

                },
                600: {
                    items: 1,

                },
                1000: {
                    items: 1,

                }
            }
        });
    }
}