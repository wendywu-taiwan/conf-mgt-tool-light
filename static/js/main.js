$(function () {
    let csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
    setToken(csrftoken);
});

function stopDialog() {
    swal.close();
}

function showWaitingDialog() {
    swal({
        title: "Please Wait..",
        imageUrl: "../../../../static/icons/loading.gif",
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