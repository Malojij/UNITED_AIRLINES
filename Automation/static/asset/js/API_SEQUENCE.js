function FileUpload() {
    const timePattern = '(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2},\\d{3})\\s+INFO\\s+.*?\\]\\s+';
    const xmlRequestPattern = "Final Received Request is in XML Format ::\\s*(\\<.*\\>)";
    const jsonRequestPattern = "Final Received Request is in JSON Format ::\\s*(\\{.*\\})";
    const xmlResponsePattern = "sendResponsePOS response send to POS ::\\s*(\\<.*\\>)";
    const jsonResponsePattern = "sendResponsePOS response send to POS ::\\s*(\\{.*\\})";
    const pedRequestPattern = "PED REQUEST\\s*:\\s*(.*?)(?=\\s*\\d{4}-\\d{2}-\\d{2}|\\Z)";
    const pedResponsePattern = "Alert : Received response from PED for encryption\\s*:\\s*(.*?)(?=\\s*\\d{4}-\\d{2}-\\d{2}|\\Z)";

    const fileInput = document.getElementById('file');
    const requestType = document.getElementById('requestType').value.toUpperCase().trim();
    const getDataAs = document.getElementById('getDataAs').value.toUpperCase().trim();
    const timedifferences = ["0.000"];
    const timestamps = [];
    const getAPIKeys = [];
    const processedLogs = [];
    let aesdkRequests = [];

    if (!fileInput.files.length) {
        alert('Please select a file to upload.');
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function(event) {
        const fileContent = event.target.result;

        const patterns = {
            "1": new RegExp(`${timePattern}(?:${requestType === "XML" ? xmlRequestPattern : jsonRequestPattern})`, 'g'),
            "2": new RegExp(`${timePattern}(?:(?:${requestType === "XML" ? xmlRequestPattern : jsonRequestPattern})|${requestType === "XML" ? xmlResponsePattern : jsonResponsePattern})`, 'g'),
            "3": new RegExp(`${timePattern}(?:(?:(?:(?:${requestType === "XML" ? xmlRequestPattern : jsonRequestPattern})|${requestType === "XML" ? xmlResponsePattern : jsonResponsePattern})|${pedRequestPattern})|${pedResponsePattern})`, 'g')
        };

        const requestResponsePattern = patterns[getDataAs];
        const matches = fileContent.matchAll(requestResponsePattern);

        for (const match of matches) {
            const timestamp = match[1]; // Adjust index based on your regex capturing groups
            timestamps.push(timestamp);

            if (getDataAs === "1") {
                aesdkRequests.push(match[2]);
            } else if (getDataAs === "2") {
                aesdkRequests.push(match[2] || match[3]);
            } else if (getDataAs === "3") {
                aesdkRequests.push(match[2] || match[3] || match[4] || match[5]);
            }
        }
        const datetimeObjects = timestamps.map(ts => new Date(ts.replace(',', '.'))); // Adjust for your date format
        timedifferences.push(...calculateTimeDifferences(datetimeObjects));
        console.log(timedifferences);
        document.getElementById('result').textContent = JSON.stringify(dataList, null, 2);
    };
    reader.readAsText(file);
}


function calculateTimeDifferences(datetimeObjects) {
    const differences = [];
    for (let i = 1; i < datetimeObjects.length; i++) {
        const difference = (datetimeObjects[i] - datetimeObjects[i - 1]) / 1000; // Difference in seconds
        differences.push(difference.toFixed(3)); // Format to 3 decimal places
    }
    return differences;
}


function createPerformableScenarios(data, RequestType) {
    const RequestArray = [];
    const timestampArray = [];
    data.forEach(item => {
        let parsedRequest;
        // Check the request type and handle accordingly
        if (RequestType === "XML") {
            parsedRequest = item.api_request; // Assume this is XML as a string
        } else if (RequestType === "JSON") {
            try {
                parsedRequest = JSON.parse(item.api_request);
            } catch (error) {
                console.error(`Invalid JSON: ${error}`);
                return; // Handle error appropriately
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
    datee = new Date(timestampStr.replace(',', '.'))
        if (typeof requestApi === 'object' && requestApi !== null) {
            Object.keys(requestApi).forEach(key => {
                allAPIKeys.push(key);
                if (key.includes("Request") || key.includes("Response")) {
                    sortedRequests.push(requestApi);
                    requestTimestampsDiff.push(datee);
                    TimestampsAPI.push(timestampStr)
                    requestKeys.push(key);
                }
            });
        } else if (requestApi.startsWith("<")) {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(requestApi, "text/xml");
            const rootTag = xmlDoc.documentElement.tagName;
            allAPIKeys.push(rootTag);
            if (rootTag.includes("Request") || rootTag.includes("Response")) {
                sortedRequests.push(requestApi);
                requestTimestampsDiff.push(datee);
                TimestampsAPI.push(timestampStr)
                requestKeys.push(rootTag);
            }
        }
    });

    const timeDifferences = [];
    for (let i = 1; i < requestTimestampsDiff.length; i++) {
        const diff = (requestTimestampsDiff[i] - requestTimestampsDiff[i - 1]) / 1000; // Difference in seconds
        timeDifferences.push(diff);
    }
    timeDifferences.push(0.001);

    // Adding a zero for the last element
    return {timeDifferences, sortedRequests, requestKeys, TimestampsAPI};
}

function startCountdown(inputValue) {
            // Clear any existing timer
            let timerInterval;
            clearInterval(timerInterval);

            if (isNaN(inputValue) || inputValue <= 0) {
                alert("Please enter a valid number greater than 0.");
                return;
            }

            let countdownTime = inputValue; // Starting point in seconds

            // Function to update the timer
            const updateTimer = () => {
                // Calculate seconds and milliseconds
                const seconds = Math.floor(countdownTime);
                const milliseconds = Math.floor((countdownTime % 1) * 1000);

                // Format the display correctly
                document.getElementById("trans_progress").innerText = 'Time waiting for ' + seconds + '.' + String(milliseconds).padStart(3, '0');
                // Format the display

                // Decrease the countdown time by 0.1 seconds
                countdownTime -= 0.1;

                // Stop the timer when it reaches zero
                if (countdownTime < 0) {
                    clearInterval(timerInterval);
                    document.getElementById("trans_progress").innerText = "0.000";
                }
            };

            // Update the timer every 100 milliseconds
            timerInterval = setInterval(updateTimer, 100);
        }

function zip(...arrays) {
    const length = Math.min(...arrays.map(arr => arr.length));
    const zipped = [];
    for (let i = 0; i < length; i++) {
        zipped.push(arrays.map(arr => arr[i]));
    }
    return zipped;
}

function colorTR(id, color){
if(id != null){
    document.getElementById(id).style.backgroundColor = color;
}
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
        await new Promise(resolve => {
            colorTR(data.currenttimestampASID, "#3eff3e");
            resolve();
        });
    } catch (error) {
        console.error('Error in AJAX call:', error);
    } finally {
        $('#loader').hide();
    }
}

async function performAjaxCallScenarios(timediffArray, apiRequestArray, APIKEYArray, timestampASIDArray, csrf) {
    const length = Math.min(timediffArray.length, apiRequestArray.length, APIKEYArray.length, timestampASIDArray.length);

    for (let i = 0; i < length; i++) {
        const apiRequest = apiRequestArray[i];
        let timediff = timediffArray[i] || -1;
        let nextRequestTimeDiff = (i + 1 < timediffArray.length) ? timediffArray[i + 1] || 0 : 0;
        const currenttimestampASID = timestampASIDArray[i].replace(/[- :,.]/g, '');
        const nexttimestampASID = (i + 1 < timestampASIDArray.length) ? timestampASIDArray[i + 1].replace(/[- :,.]/g, '') : null;
        const currentAPI = APIKEYArray[i];
        const nextAPI  =  (i + 1 < APIKEYArray.length) ? APIKEYArray[i + 1] : "";
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
        console.log("CurrentAPI:", currentAPI, "NextAPI:", nextAPI, "TimeDiff:", timediff, "Next time: ", nextRequestTimeDiff);
        await startProcessing(data); // Uncomment this line when you're ready to call it
    }
}