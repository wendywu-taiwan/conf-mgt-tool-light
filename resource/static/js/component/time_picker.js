$(function () {
    $('.clockpicker').clockpicker();
});

getProceedTime = function () {
    let start_time = $("#clock_picker_input").val();
    start_time = start_time + ":00";
    return start_time
};

setProceedTime = function (nextProceedTime) {
    $("#clock_picker_input").val(nextProceedTime);
};