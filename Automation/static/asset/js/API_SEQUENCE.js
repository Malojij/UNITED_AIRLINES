// FULLY PATCHED API_SEQUENCE.js

// ======= API_SEQUENCE.js (patched) =======

let __trans_timer_interval = null;

function calculateTimeDifferences(datetimeObjects) {
    const differences = [];
    for (let i = 1; i < datetimeObjects.length; i++) {
        const diff = (datetimeObjects[i] - datetimeObjects[i - 1]) / 1000;
        differences.push(diff.toFixed(3));
    }
    return differences;
}

function createPerformableScenarios(data, RequestType) {
    const RequestArray = [];
    const timestampArray = [];

    data.forEach(item => {
        let parsedRequest;

        if (RequestType === "XML") {
            parsedRequest = item.api_request;
        } else if (RequestType === "JSON") {
            try {
                parsedRequest = JSON.parse(item.api_request);
            } catch (error) {
                console.error("Invalid JSON:", item.api_request);
                parsedRequest = null;
            }
        }

        timestampArray.push(item.timestamp);
        RequestArray.push(parsedRequest);
    });

    const allAPIKeys = [];
    const sortedRequests = [];
    const requestTimestampsDiff = [];
    const TimestampsAPI = [];
    const requestKeys = [];

    const zipper = (a, b) => a.map((k, i) => [k, b[i]]);
    const items = zipper(RequestArray, timestampArray);

    items.forEach(([requestApi, timestampStr]) => {
        const datee = new Date(timestampStr.replace(',', '.'));

        if (typeof requestApi === 'object' && requestApi !== null) {
            Object.keys(requestApi).forEach(key => {
                allAPIKeys.push(key);

                if (key.includes("Request") || key.includes("Response")) {
                    sortedRequests.push(requestApi);
                    requestTimestampsDiff.push(datee);
                    TimestampsAPI.push(timestampStr);
                    requestKeys.push(key);
                }
            });

        } else if (typeof requestApi === "string" && requestApi.trim().startsWith("<")) {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(requestApi, "text/xml");
            const rootTag = xmlDoc.documentElement.tagName;

            allAPIKeys.push(rootTag);

            if (rootTag.includes("Request") || rootTag.includes("Response")) {
                sortedRequests.push(requestApi);
                requestTimestampsDiff.push(datee);
                TimestampsAPI.push(timestampStr);
                requestKeys.push(rootTag);
            }
        } else {
            console.warn("Skipping invalid requestApi:", requestApi);
        }
    });

    const timeDifferences = [];
    for (let i = 1; i < requestTimestampsDiff.length; i++) {
        const diff = (requestTimestampsDiff[i] - requestTimestampsDiff[i - 1]) / 1000;
        timeDifferences.push(diff);
    }
    timeDifferences.push(0.001);

    return { timeDifferences, sortedRequests, requestKeys, TimestampsAPI };
}

function startCountdown(inputValue) {
    clearInterval(__trans_timer_interval);

    if (isNaN(inputValue) || inputValue <= 0) {
        alert("Please enter a valid number greater than 0.");
        return;
    }

    let countdownTime = inputValue;

    const updateTimer = () => {
        const seconds = Math.floor(countdownTime);
        const milliseconds = Math.floor((countdownTime % 1) * 1000);

        document.getElementById("trans_progress").innerText =
            `Time waiting for ${seconds}.${String(milliseconds).padStart(3, '0')}`;

        countdownTime -= 0.1;

        if (countdownTime < 0) {
            clearInterval(__trans_timer_interval);
            document.getElementById("trans_progress").innerText = "0.000";
        }
    };

    __trans_timer_interval = setInterval(updateTimer, 100);
}

function zip(...arrays) {
    const length = Math.min(...arrays.map(arr => arr.length));
    return Array.from({ length }, (_, i) => arrays.map(arr => arr[i]));
}

function colorTR(id, color) {
    if (id) document.getElementById(id).style.backgroundColor = color;
}

async function startProcessing(data) {
    try {
        if ((data.currentAPI.includes("Request") && data.nextAPI.includes("Request")) || data.currentAPI.includes("Response")) {
            updateMessage("Please wait for " + data.timediffArray + " seconds");
            startCountdown(data.timediffArray);
        }

        colorTR(data.currenttimestampASID, "#FFFF5D");

        const response = await $.ajax({
            type: "POST",
            dataType: "JSON",
            url: "./API_SEQUENCE_TESTING",
            data: data,
        });

        colorTR(data.currenttimestampASID, "#3eff3e");

    } catch (error) {
        console.error("Error in AJAX call:", error);
    } finally {
        $('#loader').hide();
    }
}

async function performAjaxCallScenarios(timediffArray, apiRequestArray, APIKEYArray, timestampASIDArray, csrf) {
    const length = Math.min(timediffArray.length, apiRequestArray.length, APIKEYArray.length, timestampASIDArray.length);

    for (let i = 0; i < length; i++) {
        const apiRequest = apiRequestArray[i];
        const timediff = timediffArray[i] || -1;
        const nextRequestTimeDiff = timediffArray[i + 1] || 0;

        const currenttimestampASID = timestampASIDArray[i].replace(/[- :,.]/g, '');
        const nexttimestampASID = timestampASIDArray[i + 1] ? timestampASIDArray[i + 1].replace(/[- :,.]/g, '') : null;

        const currentAPI = APIKEYArray[i];
        const nextAPI = APIKEYArray[i + 1] || "";
        const islast = nextAPI === "" ? 1 : 0;

        const data = {
            csrfmiddlewaretoken: csrf,
            timediffArray: timediff,
            nextRequestTimeDiff: nextRequestTimeDiff,
            apiRequestArray: apiRequest,
            currenttimestampASID: currenttimestampASID,
            nexttimestampASID: nexttimestampASID,
            currentAPI: currentAPI,
            nextAPI: nextAPI,
            Scenario: "1",
            islast: islast
        };

        console.log("CurrentAPI:", currentAPI, "NextAPI:", nextAPI, "TimeDiff:", timediff, "Next time:", nextRequestTimeDiff);

        await startProcessing(data);
    }
}
