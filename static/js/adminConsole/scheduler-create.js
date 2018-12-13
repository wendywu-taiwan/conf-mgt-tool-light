$(function () {
    $('.clockpicker').clockpicker();
    $(".tagsinput").tagsinput();

    $("#base_env_select_list li").click(function () {
        console.log('select:', $(this).text());
        $("#select_base_env_btn:first-child").text($(this).text());
        $("#select_base_env_btn:first-child").val($(this).val());
    });

    $("#compare_env_select_list li").click(function () {
        console.log('select:', $(this).text());
        $("#select_compare_env_btn:first-child").text($(this).text());
        $("#select_compare_env_btn:first-child").val($(this).val());
    });
});


let baseEnvId, compareEnvId, moduleId, interval_hour, start_date_time;
let country_list = [];
let mail_list = [];

createTask = function (url, module_id, task_list_url) {
    showWaitingDialog();
    console.log("url" + url);
    let validData = checkInputValid(module_id);
    if (!validData)
        return;

    let post_body = {
        "base_environment_id": baseEnvId,
        "compare_environment_id": compareEnvId,
        "module_id": moduleId,
        "country_list": country_list,
        "mail_list": mail_list,
        "interval_hour": interval_hour,
        "start_date_time": start_date_time
    }

    doPOST(url, post_body, function (response) {
        showSuccessDialog("create task success");
        window.location = task_list_url;
    }, function (response) {
        showErrorDialog("create task fail")
    });
};

updateTask = function (url, module_id, task_id) {
    showWaitingDialog();
    console.log("url" + url);
    let validData = checkInputValid(module_id);
    if (!validData)
        return;

    let post_body = {
        "id": task_id,
        "base_environment_id": baseEnvId,
        "compare_environment_id": compareEnvId,
        "module_id": moduleId,
        "country_list": country_list,
        "mail_list": mail_list,
        "interval_hour": interval_hour,
        "start_date_time": start_date_time
    }

    doPOST(url, post_body, function (response) {
        showSuccessDialog("update task success")
    }, function (response) {
        showErrorDialog("update task fail")
    });
}

checkInputValid = function (module_id) {
    baseEnvId = $("#select_base_env_btn:first-child").val();
    compareEnvId = $("#select_compare_env_btn:first-child").val();
    moduleId = module_id;
    interval_hour = $("#hour_input").val();
    start_date_time = getStartDateTime();
    mail_list = $("#mail_receiver_input").tagsinput('items');
    console.log("interval_hour:" + interval_hour);

    if (!baseEnvId || !compareEnvId) {
        showEWarningDialog("please select environment");
        return false;
    }
    if (baseEnvId === compareEnvId) {
        showEWarningDialog("please select different environment");
        return false;
    }

    if (country_list.length == 0) {
        showEWarningDialog("please select country");
        return false;
    }

    if (!interval_hour) {
        showEWarningDialog("please enter hour interval");
        return false;
    } else if (Number(interval_hour) % 1 != 0) {
        showEWarningDialog("please enter integer hour interval");
        return false;
    }

    if (!start_date_time) {
        showEWarningDialog("please enter daily start time");
        return false;
    }

    if (mail_list.length == 0) {
        showEWarningDialog("please enter receiver");
        return false;
    }
    return true;
};

checkboxOnClick = function (country_id) {
    country_list.push(country_id);
};

getStartDateTime = function () {
    let start_time = $("#clock_picker_input").val();
    let today = new Date();
    let yy = today.getFullYear();
    let mm = today.getMonth() + 1;
    let dd = today.getDate();
    start_time = yy + "/" + mm + "/" + dd + " " + start_time + ":00";
    return start_time
};