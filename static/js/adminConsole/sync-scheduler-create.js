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


let sourceEnvId, targetEnvId, intervalHour, startDateTime;
let backup = false;
let countryList = [];
let mailList = [];
let actionList = [];
let moduleId, postUrl, taskListUrl;

function init(module_id, post_url, list_url) {
    moduleId = module_id;
    postUrl = post_url;
    taskListUrl = list_url;
}

runTask = function (postUrl) {
    showWaitingDialog();
    let validData = checkInputValid(true);
    if (!validData)
        return;

    let post_body = {
        "source_environment_id": sourceEnvId,
        "target_environment_id": targetEnvId,
        "module_id": moduleId,
        "country_list": countryList,
        "action_list": actionList,
        "receiver_list": mailList,
        "interval_hour": 0,
        "next_proceed_time": getCurrentDataTime(),
        "backup": backup
    };

    doPOST(postUrl, post_body, function (response) {
        if (response == null || response["status_code"] != 200) {
            showErrorDialog(response["message"])
        } else {
            successDialog("run task success", function () {
                console.log(response);
            });
        }
    }, function (response) {
        console.log(response);
        showErrorDialog(response["message"])
    });
};

createTask = function () {
    showWaitingDialog();
    let validData = checkInputValid(false);
    if (!validData)
        return;

    let post_body = {
        "source_environment_id": sourceEnvId,
        "target_environment_id": targetEnvId,
        "module_id": moduleId,
        "country_list": countryList,
        "action_list": actionList,
        "receiver_list": mailList,
        "interval_hour": intervalHour,
        "next_proceed_time": startDateTime,
        "backup": backup
    };

    doPOST(postUrl, post_body, function (response) {
        if (response == null || response["status_code"] != 200) {
            showErrorDialog(response["message"])
        } else {
            successDialog("create task success", function () {
                console.log(response);
                window.location = taskListUrl;
            });
        }
    }, function (response) {
        showErrorDialog(response["message"]);
    });
};

updateTask = function (task_id) {
    showWaitingDialog();
    let validData = checkInputValid(false);
    if (!validData)
        return;

    let post_body = {
        "task_id": task_id,
        "source_environment_id": sourceEnvId,
        "target_environment_id": targetEnvId,
        "country_list": countryList,
        "action_list": actionList,
        "receiver_list": mailList,
        "interval_hour": intervalHour,
        "next_proceed_time": startDateTime,
        "backup": backup
    };

    doPOST(postUrl, post_body, function (response) {
        if (response == null || response["status_code"] != 200) {
            showErrorDialog(response["message"])
        } else {
            successDialog("update task success", function () {
                console.log(response);
                window.location = taskListUrl;
            });
        }
    }, function (response) {
        showErrorDialog(response["message"])
    });
};

checkInputValid = function (runNow) {
    sourceEnvId = $("#select_source_env_btn:first-child").val();
    targetEnvId = $("#select_target_env_btn:first-child").val();
    intervalHour = $("#hour_input").val();
    startDateTime = getStartDateTime();
    mailList = $("#mail_receiver_input").tagsinput('items');

    if (!sourceEnvId || !targetEnvId) {
        showWarningDialog("please select environment");
        return false;
    }
    if (sourceEnvId === targetEnvId) {
        showWarningDialog("please select different environment");
        return false;
    }

    if (countryList.length == 0) {
        showWarningDialog("please select country");
        return false;
    }

    if (actionList.length == 0) {
        showWarningDialog("please select action");
        return false;
    }

    if (!runNow && !intervalHour) {
        showWarningDialog("please enter hour interval");
        return false;
    } else if (Number(intervalHour) % 1 != 0) {
        showWarningDialog("please enter integer hour interval");
        return false;
    }

    if (!runNow && !startDateTime) {
        showWarningDialog("please enter daily start time");
        return false;
    }

    if (mailList.length == 0) {
        showWarningDialog("please enter receiver");
        return false;
    }
    return true;
};

function setSourceEnvSelected(id, name) {
    $("#select_source_env_btn:first-child").text(name);
    $("#select_source_env_btn:first-child").val(id);
};

function setTargetEnvSelected(id, name) {
    $("#select_target_env_btn:first-child").text(name);
    $("#select_target_env_btn:first-child").val(id);
};

countryCheckboxOnChange = function (checkboxItem) {
    let countryId = checkboxItem.value;
    if (checkboxItem.checked && !countryList.includes(countryId)) {
        countryCheckboxOnClick(countryId)
    } else {
        countryList = countryList.filter(function (item) {
            return item !== countryId;
        })
    }
};

countryCheckboxOnClick = function (countryId) {
    countryList.push(countryId);
};


actionCheckboxOnChanged = function (checkboxItem) {
    let action = checkboxItem.value;
    if (checkboxItem.checked && !actionList.includes(action)) {
        actionList.push(action);
    } else {
        actionList = actionList.filter(function (item) {
            return item !== action;
        })
    }
};

backupOnChecked = function (checkboxItem) {
    if (checkboxItem.checked) {
        backup = true;
    } else {
        backup = false;
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