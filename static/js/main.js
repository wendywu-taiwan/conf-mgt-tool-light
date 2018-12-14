$(function () {
    $("#select-country-list li").click(function () {
        console.log('select:', $(this).text());
        $("#select-country-btn:first-child").text($(this).text());
        $("#select-country-btn:first-child").val($(this).text());
        $("#country_selected").val($(this).val());

    });

    $("#select-env-1-list li").click(function () {

        $("#select-env-1-btn:first-child").text($(this).text());
        $("#select-env-1-btn:first-child").val($(this).text());
        $("#environment_1_selected").val($(this).val());

    });

    $("#select-env-2-list li").click(function () {

        $("#select-env-2-btn:first-child").text($(this).text());
        $("#select-env-2-btn:first-child").val($(this).text());
        $("#environment_2_selected").val($(this).val());
    });
});


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