function before_data_send(i, message) {
    $('#loader').show();
    const str = $('<div class="p-1"><div class="spinner-border text-white" role="status" style="vertical-align: middle;"></div><span class="text-center m-5"># ' + i + ' ' + message + '</span></div>').hide();
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
    const g = document.getElementById('Transaction_Type').validity.valid;
    const t = document.getElementById('cds').validity.valid;
    if (!g || !t) {
        alert("data missing");
        return;
    }

    // disable UI while processing
    $('#cds, #submit, #Transaction_Type, #gcb_type, #OnPinkey, #product_count').prop('disabled', true);

    const table_header = $('<tr id="head1"><th>CardToken</th><th>Request</th><th>EntryMode</th><th>TransType</th><th>SeqNum</th><th>ExpectedCardType</th><th>ActualCardType</th><th>SubCardType</th><th>TrnsAmt</th><th>ApprovedAmt</th><th>ResponseText</th><th>ResponseCode</th><th>TransactionID</th><th>AurusPayTicketNum</th><th>ApprovalCode</th></tr>').hide();
    $("#table_header").html(table_header);
    $(table_header).fadeIn("slow");
    setTimeout(function() {
        readExcel();
    }, 500);
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
}

function after_data_receive(data){
    if (!Array.isArray(data) || data.length === 0) return;
    if (data[0]["Error_count"] == "1") {
        $('#submit, #cds, #Transaction_Type, #gcb_type, #OnPinkey, #product_count').prop('disabled', false);
        $('#trans_progress').hide();
        $("#table_header").hide();
    } else {
        const str = $('<div data-aos-easing="ease" data-aos-duration="1000" data-aos-delay="0" class="w-100 text-center p-2" id="loader"><span style="vertical-align: middle;"><i class="fa fa-solid fa-check" aria-hidden="true"></i></span><span class="m-3">Transaction completed</span></div>').hide();
        $("#trans_progress").html(str);
        $(str).fadeIn(1500);
        setTimeout(function() {
            $("#loader").remove();
            $('#submit, #cds, #Transaction_Type, #gcb_type, #OnPinkey, #product_count').prop('disabled', false);
            $('#export_btn').removeClass('d-none');
            $("#ErrorDiv").html("")
        }, 2000);
    }
}

function exportToExcel() {
   const table = document.getElementsByTagName("table");
   if (!table || table.length === 0) return;
   const currentDate = new Date();
   const today = currentDate.toISOString().slice(0, 10);
   const time = currentDate.getHours() + ":" + currentDate.getMinutes() + ":" + currentDate.getSeconds();
   TableToExcel.convert(table[0], {
      name: 'Outdoor_testing_'+today+'_'+time+'.xlsx',
      sheet: { name: 'Testing_Result' }
   });
}

// ===== Utility helpers =====
function safeGet(obj, path, defaultVal) {
    try {
        const parts = path.split('.');
        let cur = obj;
        for (const p of parts) {
            if (cur == null) return defaultVal;
            cur = cur[p];
        }
        return cur == null ? defaultVal : cur;
    } catch (e) {
        return defaultVal;
    }
}

// Map internal transaction types to readable labels
const RequestLabelMap = {
    '00': 'GCB',
    '01': 'Sale',
    '02': 'Refund',
    '03': 'Void',
    '04': 'Pre_auth',
    '05': 'Post_auth',
    '05_01': 'Post_auth (Retry)',
    '05_09': 'Reversal of Post-auth',
    '06': 'Void',
    '07': 'Refund',
    '08': 'Other',
    '09': 'Reversal',
    '10': 'Reversal',
    '11': 'Other',
    '12': 'Other',
    '099': 'Reversal of Post-auth'
};

function transactionLabel(type) {
    return RequestLabelMap[type] || type || '';
}

function normalizeTransType(txType) {
    // Ensure consistent tokens for checks (server may send 099 for 05_09)
    if (txType === '099') return '099';
    return ('' + txType).trim();
}

// ===== Main renderer =====
function Transaction_report(response, Transaction_type, starttime, iteration) {
    // Clear previous error
    $("#Error").html('');

    // Normalize inputs
    const requestFormat = response.requestFormat || '';
    Transaction_type = normalizeTransType(Transaction_type);

    const Parent_TransactionType = response.Parent_TransactionType || '';
    let Child_TransactionType = response.Child_TransactionType || '';
    const Gcb_TransactionType = response.Gcb_TransactionType || '';

    // Track data/card
    const TrackData = (response.TrackData || '').replace('%B', '').split('^')[0] || '';
    let Parent_Transaction_CardNumber = TrackData;
    const Expectedcardtype = response.Expectedcardtype || '';

    // Prepare raw request/response objects
    const GCB_request = safeGet(response, 'GCB_request.GetCardBINRequest', safeGet(response, 'GCB_request', {}));
    const GCB_response = safeGet(response, 'GCB_response', {});
    const parentRequest = safeGet(response, 'Parent_Transaction_request.TransRequest', safeGet(response, 'Parent_Transaction_request', {}));
    const ParentResponse = safeGet(response, 'Parent_Transaction_response.TransResponse', undefined);
    const ChildRequest = safeGet(response, 'Child_Transaction_request.TransRequest', safeGet(response, 'Child_Transaction_request', {}));
    const ChildResponse = safeGet(response, 'Child_Transaction_response.TransResponse', undefined);

    // Normalize GCB
    const GCB = (GCB_response && GCB_response.GetCardBINResponse) ? GCB_response.GetCardBINResponse : (GCB_response || {});
    const Gcb_fleet_prompts = GCB.FleetPromptsFlag || '';
    const Gcb_Transaction_CardEntryMode = GCB.CardEntryMode || '';
    const Gcb_Transaction_CardType = GCB.CardType || '';
    const Gcb_Transaction_SubCardType = GCB.SubCardType || '';
    const Gcb_Transaction_ResponseText = GCB.ResponseText || '';
    const Gcb_Transaction_ResponseCode = GCB.ResponseCode || '';
    const Gcb_Transaction_TransactionID = GCB.TransactionIdentifier || '';

    const GCBResponseTextcolor = Gcb_Transaction_ResponseText === 'Approved' ? 'green' : 'red';

    // build GCB row element (but only append when meaningful)
    const gcbRow = $('<tr/>').hide();
    gcbRow.append($('<td/>').text('GCB'));
    gcbRow.append($('<td/>').text(Gcb_Transaction_CardEntryMode));
    gcbRow.append($('<td/>').text(''));
    gcbRow.append($('<td/>').text(''));
    gcbRow.append($('<td/>').text(Expectedcardtype));
    gcbRow.append($('<td/>').text(Gcb_Transaction_CardType));
    gcbRow.append($('<td/>').text(Gcb_Transaction_SubCardType));
    gcbRow.append($('<td/>').text(''));
    gcbRow.append($('<td/>').text(''));
    gcbRow.append($('<td/>').text(Gcb_Transaction_ResponseText).css('color', GCBResponseTextcolor));
    gcbRow.append($('<td/>').text(Gcb_Transaction_ResponseCode));
    gcbRow.append($('<td/>').text(Gcb_Transaction_TransactionID));
    gcbRow.append($('<td/>').text(''));
    gcbRow.append($('<td/>').text(''));

    // Build GCB accordion card HTML
    const gcb_owl_data = `<div id="gcb_owl_data${iteration}" class="owl-carousel"><div class="item"><p class="text-center"> GCB Request </p><hr><pre><code>${JSON.stringify(GCB_request, null, 4)}</code></pre></div><div class="item"><p class="text-center"> GCB Response </p><hr><pre><code>${JSON.stringify(GCB, null, 4)}</code></pre></div></div>`;
    const gcb_card = $(`<div class="card ${GCBResponseTextcolor}"><div class="card-header" data-toggle="collapse" href="#collapseGCB_${iteration}"><a class="card-link"># GCB Transaction ${iteration}</a><i class="fa-solid fa-chevron-down fa-style"></i></div><div id="collapseGCB_${iteration}" class="collapse" data-parent="#accordion"><div class="card-body">${gcb_owl_data}</div></div></div>`).hide();

    // Parent normalization
    let parentRow, parent_card;
    if (ParentResponse !== undefined) {
        let pDetails = safeGet(ParentResponse, 'TransDetailsData.TransDetailData', {});
        pDetails = Array.isArray(pDetails) ? pDetails[0] : (pDetails || {});

        Parent_Transaction_CardNumber = pDetails.CardNumber || Parent_Transaction_CardNumber;
        const Parent_Transaction_CardEntryMode = pDetails.CardEntryMode || '';
        const Parent_Transaction_TransactionTypeCode = pDetails.TransactionTypeCode || '';
        const Parent_Transaction_TransactionSequenceNumber = pDetails.TransactionSequenceNumber || '';
        const Parent_Transaction_CardType = pDetails.CardType || '';
        const Parent_Transaction_SubCardType = pDetails.SubCardType || '';
        const Parent_Transaction_requestAmount = safeGet(parentRequest, 'TransAmountDetails.TransactionTotal', '');
        const Parent_Transaction_TransactionAmount = pDetails.TransactionAmount || '';
        const Parent_Transaction_ResponseText = pDetails.ResponseText || '';
        const Parent_Transaction_ResponseCode = pDetails.ResponseCode || '';
        const Parent_Transaction_TransactionIdentifier = pDetails.TransactionIdentifier || '';
        const Parent_Transaction_AurusPayTicketNum = ParentResponse.AurusPayTicketNum || '';
        const Parent_Transaction_ApprovalCode = pDetails.ApprovalCode || '';
        const Parent_Transaction_ReceiptInfo = JSON.stringify(pDetails.ReceiptDetails || {}, null, 4);

        parentRow = $('<tr/>').hide();
        parentRow.append($('<td/>').text(transactionLabel(Parent_TransactionType)));
        parentRow.append($('<td/>').text(Parent_Transaction_CardEntryMode));
        parentRow.append($('<td/>').text(Parent_Transaction_TransactionTypeCode));
        parentRow.append($('<td/>').text(Parent_Transaction_TransactionSequenceNumber));
        parentRow.append($('<td/>').text(Expectedcardtype));
        parentRow.append($('<td/>').text(Parent_transaction_safe(Parent_Transaction_CardType)));
        parentRow.append($('<td/>').text(Parent_Transaction_SubCardType));
        parentRow.append($('<td/>').text(Parent_Transaction_requestAmount));
        parentRow.append($('<td/>').text(Parent_Transaction_TransactionAmount));
        parentRow.append($('<td/>').text(Parent_Transaction_ResponseText).css('color', Parent_Transaction_ResponseText === 'APPROVAL' ? 'green' : 'red'));
        parentRow.append($('<td/>').text(Parent_Transaction_ResponseCode));
        parentRow.append($('<td/>').text(Parent_Transaction_TransactionIdentifier));
        parentRow.append($('<td/>').text(Parent_Transaction_AurusPayTicketNum));
        parentRow.append($('<td/>').text(Parent_Transaction_ApprovalCode));

        const Parent_owl_data = `<div id="Parent_owl_data${Parent_Transaction_TransactionIdentifier}" class="owl-carousel"><div class="item"><p class="text-center"> GCB Response </p><hr><pre><code>${JSON.stringify(GCB, null, 4)}</code></pre></div><div class="item"><p class="text-center"> Receipt </p><hr><pre><code>${Parent_Transaction_ReceiptInfo}</code></pre></div></div>`;
        parent_card = $(`<div class="card ${(Parent_Transaction_ResponseText === 'APPROVAL' ? 'green' : 'red')}"><div class="card-header" data-toggle="collapse" href="#collapse_${Parent_Transaction_TransactionIdentifier}"><a class="card-link"># ${transactionLabel(Parent_TransactionType)} Transaction ${Parent_Transaction_TransactionIdentifier}</a><i class="fa-solid fa-chevron-down fa-style"></i></div><div id="collapse_${Parent_Transaction_TransactionIdentifier}" class="collapse" data-parent="#accordion"><div class="card-body">${Parent_owl_data}</div></div></div>`).hide();
    }

    // Child normalization
    let childRow, child_card;
    if (ChildResponse !== undefined) {
        let cDetails = safeGet(ChildResponse, 'TransDetailsData.TransDetailData', {});
        cDetails = Array.isArray(cDetails) ? cDetails[0] : (cDetails || {});

        const Child_Transaction_CardEntryMode = cDetails.CardEntryMode || '';
        const Child_Transaction_TransactionTypeCode = cDetails.TransactionTypeCode || '';
        const Child_Transaction_TransactionSequenceNumber = cDetails.TransactionSequenceNumber || '';
        const Child_Transaction_CardType = cDetails.CardType || '';
        const Child_Transaction_SubCardType = cDetails.SubCardType || '';
        const Child_Transaction_requestAmount = safeGet(ChildRequest, 'TransAmountDetails.TransactionTotal', '');
        const Child_Transaction_TransactionAmount = cDetails.TransactionAmount || '';
        const Child_Transaction_ResponseText = cDetails.ResponseText || '';
        const Child_Transaction_ResponseCode = cDetails.ResponseCode || '';
        const Child_Transaction_TransactionIdentifier = cDetails.TransactionIdentifier || '';
        const Child_Transaction_AurusPayTicketNum = ChildResponse.AurusPayTicketNum || '';
        const Child_Transaction_ApprovalCode = cDetails.ApprovalCode || '';
        const Child_Transaction_ReceiptInfo = JSON.stringify(cDetails.ReceiptDetails || {}, null, 4);

        childRow = $('<tr/>').hide();
        childRow.append($('<td/>').text(transactionLabel(Child_TransactionType)));
        childRow.append($('<td/>').text(Child_Transaction_CardEntryMode));
        childRow.append($('<td/>').text(Child_Transaction_TransactionTypeCode));
        childRow.append($('<td/>').text(Child_Transaction_TransactionSequenceNumber));
        childRow.append($('<td/>').text(Expectedcardtype));
        childRow.append($('<td/>').text(Child_Transaction_CardType));
        childRow.append($('<td/>').text(Child_Transaction_SubCardType));
        childRow.append($('<td/>').text(Child_Transaction_requestAmount));
        childRow.append($('<td/>').text(Child_Transaction_TransactionAmount));
        childRow.append($('<td/>').text(Child_Transaction_ResponseText).css('color', Child_Transaction_ResponseText === 'APPROVAL' ? 'green' : 'red'));
        childRow.append($('<td/>').text(Child_Transaction_ResponseCode));
        childRow.append($('<td/>').text(Child_Transaction_TransactionIdentifier));
        childRow.append($('<td/>').text(Child_Transaction_AurusPayTicketNum));
        childRow.append($('<td/>').text(Child_Transaction_ApprovalCode));

        const Child_owl_data = `<div id="Child_owl_data${Child_Transaction_TransactionIdentifier}" class="owl-carousel"><div class="item"><p class="text-center"> Receipt </p><hr><pre><code>${Child_Transaction_ReceiptInfo}</code></pre></div><div class="item"><p class="text-center"> Products </p><hr><pre><code>${JSON.stringify(safeGet(ChildRequest, 'Level3ProductsData', safeGet(ChildRequest, 'FleetData', {})), null, 4)}</code></pre></div></div>`;
        child_card = $(`<div class="card ${(Child_Transaction_ResponseText === 'APPROVAL' ? 'green' : 'red')}"><div class="card-header" data-toggle="collapse" href="#collapse_${Child_Transaction_TransactionIdentifier}"><a class="card-link"># ${transactionLabel(Child_TransactionType)} Transaction ${Child_Transaction_TransactionIdentifier}</a><i class="fa-solid fa-chevron-down fa-style"></i></div><div id="collapse_${Child_Transaction_TransactionIdentifier}" class="collapse" data-parent="#accordion"><div class="card-body">${Child_owl_data}</div></div></div>`).hide();
    }

    // ===== Calculate dynamic rowspan correctly =====
    let rowspan = 1; // base for CardToken cell
    try {
        if (GCB && Object.keys(GCB).length > 0) rowspan++;
    } catch (e) {}
    if (ParentResponse !== undefined) rowspan++;
    if (ChildResponse !== undefined) rowspan++;

    // Only create card entries for relevant transaction groups
    const renderableTypes = new Set(['00','01','02','03','04','05','05_01','05_09','06','07','08','09','10','11','12','099']);

    if (renderableTypes.has(Transaction_type)) {
        const first_row = $(`<tr><td rowspan="${rowspan}">${Parent_Transaction_CardNumber}</td></tr>`).hide();
        $("#divBody").append(first_row);
        $(first_row).fadeIn('slow');

        // Append GCB row if present
        if (GCB && Object.keys(GCB).length > 0) {
            $("#divBody").append(gcbRow);
            $(gcbRow).fadeIn('slow');
        }
    }

    // Render parent if exists
    if (ParentResponse !== undefined && typeof parentRow !== 'undefined') {
        $("#divBody").append(parentRow);
        $(parentRow).fadeIn('slow');
        if (parent_card) {
            $("#accordion").append(parent_card);
            $(parent_card).fadeIn('slow');
            try { $(`#Parent_owl_data${safeGet(parentRequest, 'TransDetailsData.TransDetailData.TransactionIdentifier', '')}`).owlCarousel({ autoPlay:3000, items:3, margin:10, responsiveClass:true, responsive:{0:{items:1},600:{items:1},1000:{items:1}}}); } catch(e){}
        }
    }

    // Render child if exists
    if (ChildResponse !== undefined && typeof childRow !== 'undefined') {
        $("#divBody").append(childRow);
        $(childRow).fadeIn('slow');
        if (child_card) {
            $("#accordion").append(child_card);
            $(child_card).fadeIn('slow');
            try { $(`#Child_owl_data${safeGet(ChildResponse, 'TransDetailsData.TransDetailData.TransactionIdentifier', '')}`).owlCarousel({ autoPlay:3000, items:3, margin:10, responsiveClass:true, responsive:{0:{items:1},600:{items:1},1000:{items:1}}}); } catch(e){}
        }
    }

}

// small helper to avoid occasional undefined casing for parent card type
function Parent_transaction_safe(val) { return val || ''; }
