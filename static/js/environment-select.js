$(function () {
    $("#select-country-list li").click(function () {
        console.log('select:', $(this).text());
        $("#select-country-btn:first-child").text($(this).text());
        $("#select-country-btn:first-child").val($(this).val());
        $("#country_selected").val($(this).val());
    });

    $("#select-env-1-list li").click(function () {

        $("#select-env-1-btn:first-child").text($(this).text());
        $("#select-env-1-btn:first-child").val($(this).val());
        $("#environment_1_selected").val($(this).val());
    });

    $("#select-env-2-list li").click(function () {

        $("#select-env-2-btn:first-child").text($(this).text());
        $("#select-env-2-btn:first-child").val($(this).val());
        $("#environment_2_selected").val($(this).val());
    });

     $("#compare_submit_button").click(function () {
         showWaitingDialog();
     });
});
