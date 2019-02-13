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


let baseEnvId, compareEnvId, intervalHour, startDateTime;
let countryList = [];
let mailList = [];
let moduleId, postUrl, taskListUrl;

function init(module_id, post_url, list_url) {
    moduleId = module_id;
    postUrl = post_url;
    taskListUrl = list_url;
}

createTask = function () {
    showWaitingDialog();
    let validData = checkInputValid();
    if (!validData)
        return;

    let post_body = {
        "base_environment_id": baseEnvId,
        "compare_environment_id": compareEnvId,
        "module_id": moduleId,
        "country_list": countryList,
        "mail_list": mailList,
        "interval_hour": intervalHour,
        "start_date_time": startDateTime
    }

    doPOST(postUrl, post_body, function (response) {
        successDialog("create task success", function () {
            console.log(response);
            window.location = taskListUrl;
        });
    }, function (response) {
        console.log(response);
        showErrorDialog("create task fail")
    });
};

updateTask = function (task_id) {
    showWaitingDialog();
    let validData = checkInputValid();
    if (!validData)
        return;

    let post_body = {
        "id": task_id,
        "base_environment_id": baseEnvId,
        "compare_environment_id": compareEnvId,
        "module_id": moduleId,
        "country_list": countryList,
        "mail_list": mailList,
        "interval_hour": intervalHour,
        "start_date_time": startDateTime
    };

    doPOST(postUrl, post_body, function (response) {
        successDialog("update task success", function () {
            console.log(response);
            window.location = taskListUrl;
        });
    }, function (response) {
        console.log(response);
        showErrorDialog("update task fail")
    });
}

checkInputValid = function () {
    baseEnvId = $("#select_base_env_btn:first-child").val();
    compareEnvId = $("#select_compare_env_btn:first-child").val();
    intervalHour = $("#hour_input").val();
    startDateTime = getStartDateTime();
    mailList = $("#mail_receiver_input").tagsinput('items');

    if (!baseEnvId || !compareEnvId) {
        showWarningDialog("please select environment");
        return false;
    }
    if (baseEnvId === compareEnvId) {
        showWarningDialog("please select different environment");
        return false;
    }

    if (countryList.length == 0) {
        showWarningDialog("please select country");
        return false;
    }

    if (!intervalHour) {
        showWarningDialog("please enter hour interval");
        return false;
    } else if (Number(intervalHour) % 1 != 0) {
        showWarningDialog("please enter integer hour interval");
        return false;
    }

    if (!startDateTime) {
        showWarningDialog("please enter daily start time");
        return false;
    }

    if (mailList.length == 0) {
        showWarningDialog("please enter receiver");
        return false;
    }
    return true;
};
checkboxOnClick = function (countryId) {
    countryList.push(countryId);
};

checkboxOnChange = function (checkboxItem) {
    let countryId = checkboxItem.value;
    if(checkboxItem.checked && !countryList.includes(countryId)){
        checkboxOnClick(countryId)
    }else{
        countryList = countryList.filter(function (item) {
            return item !== countryId;
        })
    }
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