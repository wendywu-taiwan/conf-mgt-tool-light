let DROPDOWN_OPTION_SELECT = "Select";
let loadingGIF;

$(function () {
    let csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    let loadingGif =
        setToken(csrftoken);
});

function initLoadingGIF(url) {
    loadingGIF = url;
}

function stopDialog() {
    swal.close();
}

function showWaitingDialog() {
    showDialog("Please Wait..");
}

function showDialog(title) {
    swal({
        title: title,
        imageUrl: loadingGIF,
        // imageUrl: "../icons/loading.gif",
        closeOnConfirm: false,
        closeOnCancel: false,
        showCancelButton: false,
        showConfirmButton: false
    });
}

function showSuccessDialog(text) {
    swal("Success", text, "success");
}

function successDialog(text, onConfirmClick) {
    swal({
        title: "Success",
        text: text,
        type: "success",
    }, onConfirmClick);
}

function showErrorDialog(text) {
    swal({type: 'error', title: 'Error', text: text})
}

function showWarningDialog(text) {
    swal({type: 'warning', title: 'Warning', text: text})
}

function warningDialog(title, text, confirmButtonText, onConfirmClick) {
    swal({
        title: title,
        text: text,
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: confirmButtonText,
        closeOnConfirm: false,
        cancelButtonText: "Cancel"
    }, onConfirmClick);
}

function confirmDialog(text, confirmButtonText, onConfirmClick) {
    swal({
        title: text,
        type: "info",
        confirmButtonColor: "#DD6B55",
        confirmButtonText: confirmButtonText,
        closeOnConfirm: true
    }, onConfirmClick);
}

function successResponse(response, func) {
    let statusCode = response["status_code"];
    if (statusCode == null || statusCode == 200) {
        func();
        stopDialog();
    } else {
        if (statusCode != 200 && statusCode != 208) {
            showErrorDialog(response["message"])
        }
    }
}

function errorResponse(response) {
    showErrorDialog(response["message"]);
}


function downloadZipFile(data, fileNameSuffix) {
    // transfer unicode data to characters
    let newContent = "";
    for (let i = 0; i < data.length; i++) {
        newContent += String.fromCharCode(data.charCodeAt(i) & 0xFF);
    }
    let bytes = new Uint8Array(newContent.length);
    for (let i = 0; i < newContent.length; i++) {
        bytes[i] = newContent.charCodeAt(i);
    }

    // use blob to download files
    let blob = new Blob([bytes], {type: "application/zip"});
    let element = document.createElement('a');
    let fileNamePrefix = getFileNameCurrentDataTime();
    element.href = URL.createObjectURL(blob);
    element.download = fileNamePrefix + "_" + fileNameSuffix + ".zip";
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

function leadingZero(value) {
    if (value < 10) {
        return "0" + value.toString();
    }
    return value.toString();
}

function getCurrentDataTime() {
    var today = new Date();
    var date = today.getFullYear() + '/' + leadingZero((today.getMonth() + 1)) + '/' + leadingZero(today.getDate());
    var time = leadingZero(today.getHours()) + ":" + leadingZero(today.getMinutes()) + ":" + leadingZero(today.getSeconds());
    return date + " " + time;
}

function getFileNameCurrentDataTime() {
    var today = new Date();
    var date = today.getFullYear() + "" + leadingZero((today.getMonth() + 1)) + "" + leadingZero(today.getDate());
    var time = leadingZero(today.getHours()) + "" + leadingZero(today.getMinutes()) + "" + leadingZero(today.getSeconds());
    return date + "_" + time;
}

function arrayContains(string, array) {
    return (array.indexOf(string) > -1);
}

function hide(item) {
    if (item == null)
        return;
    item.style.display = "none";
}

function showFlex(item) {
    if (item == null)
        return;
    item.style.display = "flex";
}

function showBlock(item) {
    if (item == null)
        return;
    item.style.display = "block";
}

function split_str(name, index) {
    let tagSplitArray = (name).split("_");
    return tagSplitArray[index];
}

function split_str_array(name) {
    let tagSplitArray = (name).split("_");
    return tagSplitArray;
}

function openNewPageWithHTML(url, html) {
    var newWindows = window.open(url);
    newWindows.document.write(html);
}

function arrayRemove(arr, value) {
    return arr.filter(function (ele) {
        return ele != value;
    });
}

function refreshPartialHTML(id, html) {
    $('#' + id).html(html);
}

function resetDropdown(id) {
    $("#" + id + ":first-child").text(DROPDOWN_OPTION_SELECT);
    $("#" + id + ":first-child").val("");
}

function setDropdown(id, value, text) {
    $("#" + id + ":first-child").text(text);
    $("#" + id + ":first-child").val(value);
}

openNewPage = function (url) {
    showWaitingDialog();
    doGET(url, function (response) {
        let statusCode = response["status_code"];
        if (statusCode == null) {
            stopDialog();
            window.open(url);
        } else {
            if (statusCode == 500)
                showErrorDialog(response["message"])
        }
    }, function (response) {
        showErrorDialog(response);
    });
};

function removeWithAnimate(obj, time) {
    // obj.style.opacity = '0';
    window.setTimeout(
        function removeThis() {
            obj.style.display = 'none';
        }, time);
}