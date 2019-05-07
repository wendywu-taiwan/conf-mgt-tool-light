$(function () {
    $('.clockpicker').clockpicker();
    $(".tagsinput").tagsinput();

    $("#source_env_select_list li").click(function () {
        $("#select_source_env_btn:first-child").text($(this).text());
        $("#select_source_env_btn:first-child").val($(this).val());
    });

    $("#target_env_select_list li").click(function () {
        $("#select_target_env_btn:first-child").text($(this).text());
        $("#select_target_env_btn:first-child").val($(this).val());
    });
});

let receivers = [];


function setCountryChecked(country_id) {
    countryCheckboxOnClick(country_id);
    $("#checkbox_input_" + country_id).prop("checked", true);
};

function setActionChecked(action) {
    actionList.push(action);
    $("#action_" + action).prop("checked", true);
}

function setDailyProceedTime(start_time) {
    var start_time_date = new Date(start_time);
    var hours = leadingZero(start_time_date.getHours());
    var minute = leadingZero(start_time_date.getMinutes());
    var start_time_hour_minute = hours + ":" + minute;
    $("#clock_picker_input").text(start_time_hour_minute);
    $("#clock_picker_input").val(start_time_hour_minute);
}

function setIntervalHour(interval_hour) {
    $("#hour_input").text(interval_hour);
    $("#hour_input").val(interval_hour);
}

function addReceivers(receiver) {
    receivers.push(receiver)
}

function setReceivers() {
    for (var i = 0; i < receivers.length; i++) {
        var receiver = receivers[i];
        $('#mail_receiver_input').tagsinput('add', "");
        $('#mail_receiver_input').tagsinput('add', receiver);
    }
}

function setBackupCheck(rulesetBackup) {
    if (rulesetBackup == "True") {
        backup = true;
        $("#backup_yes_input").prop("checked", true);
    } else {
        backup = false;
        $("#backup_yes_input").prop("checked", false);
    }
}