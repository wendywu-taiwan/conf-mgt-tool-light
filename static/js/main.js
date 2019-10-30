$(function () {
    let csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    setToken(csrftoken);
});

function stopDialog() {
    swal.close();
}

function showWaitingDialog() {
    showDialog("Please Wait..");
}

function showDialog(title) {
    swal({
        title: title,
        imageUrl: "/static/icons/loading.gif",
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


function downloadZipFile(data) {
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
    element.href = URL.createObjectURL(blob);
    element.download = "ruleset.zip";
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
    var date = today.getFullYear() + '/' + (today.getMonth() + 1) + '/' + today.getDate();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    return date + " " + time;
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