$(function () {
    flatpickr("#date_picker", {
        minDate: "today",
        defaultDate: "today",
        dateFormat: "Y/m/d"
    });
});

getProceedDate = function () {
    return $("#date_picker").val();
};

setProceedDate = function (nextProceedDate) {
    flatpickr("#date_picker", {
        minDate: "today",
        defaultDate: nextProceedDate,
        dateFormat: "Y/m/d"
    });
    $("#date_picker").val(nextProceedDate);
};