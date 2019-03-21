$(function () {
    $('.clockpicker').clockpicker();
    $(".tagsinput").tagsinput();

    $("#base_env_select_list li").click(function () {
        $("#select_base_env_btn:first-child").text($(this).text());
        $("#select_base_env_btn:first-child").val($(this).val());
    });

    $("#compare_env_select_list li").click(function () {
        $("#select_compare_env_btn:first-child").text($(this).text());
        $("#select_compare_env_btn:first-child").val($(this).val());
    });

});

function setBaseEnvSelected(id, name) {
    $("#select_base_env_btn:first-child").text(name);
    $("#select_base_env_btn:first-child").val(id);
};

function setCompareEnvSelected(id, name) {
    $("#select_compare_env_btn:first-child").text(name);
    $("#select_compare_env_btn:first-child").val(id);
};

function setCountryChecked(country_id) {
    countryCheckboxOnClick(country_id);
    $("#checkbox_input_" + country_id).prop("checked", true);
};

function setMailContentTypeChecked(mail_content_type_id) {
    mailContentTypeCheckboxOnClick(mail_content_type_id);
    $("#checkbox_input_" + mail_content_type_id).prop("checked", true);
};

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

let receivers = [];

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

function leadingZero(value) {
    if (value < 10) {
        return "0" + value.toString();
    }
    return value.toString();
}