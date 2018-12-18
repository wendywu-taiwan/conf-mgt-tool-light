function showWaitingDialog() {
    swal({
        title: "Please Wait..",
        imageUrl: "../../../../static/icons/loading.gif",
        closeOnConfirm: false,
        closeOnCancel: false,
        showCancelButton:false,
        showConfirmButton:false
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