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


showWaitingDialog = function () {
    swal({
        title: "Please Wait..",
        imageUrl: "../../../../static/icons/loading.gif",
        closeOnConfirm: false,
        closeOnCancel: false
    });
};

showSuccessDialog = function (text) {
    swal("Success", text, "success");
};

showErrorDialog = function (text) {
    swal({ type: 'error', title: 'Error', text: text})
};

showEWarningDialog = function (text) {
    swal({ type: 'warning', title: 'Warning', text: text})
};