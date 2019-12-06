$(function () {
    $(".tagsinput").tagsinput();
});


let baseEnvId, compareEnvId, interval, startDateTime, frequencyType;
let countryList = [];
let mailList = [];
let mailContentTypeList = [];
let moduleId, postUrl, taskListUrl;

function init(post_url, list_url) {
    postUrl = post_url;
    taskListUrl = list_url;
}

createTask = function () {
    showWaitingDialog();
    let validData = checkInputValid();
    if (!validData)
        return;

    let post_body = {
        "left_data_center_id": leftRegionId,
        "right_data_center_id": rightRegionId,
        "left_environment_id":leftEnvId,
        "right_environment_id":rightEnvId,
        "left_folder":leftFolder,
        "right_folder":rightFolder,
        "mail_list": mailList,
        "frequency_type": frequencyType,
        "interval": interval,
        "start_date_time": startDateTime
    };

    doPOST(postUrl, post_body, function (response) {
        let statusCode = response["status_code"];
        let message = response["message"];

        if (response == null || statusCode != 200) {
            showErrorDialog(message);
        } else {
            successDialog("create task success", function () {
                console.log(response);
                window.location = taskListUrl;
            });
        }
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
        "mail_content_type_list": mailContentTypeList,
        "mail_list": mailList,
        "frequency_type": frequencyType,
        "interval": interval,
        "start_date_time": startDateTime
    };

    doPOST(postUrl, post_body, function (response) {
        let statusCode = response["status_code"];
        let message = response["message"];

        if (response == null || statusCode != 200) {
            showErrorDialog(message);
        } else {
            successDialog("update task success", function () {
                console.log(response);
                window.location = taskListUrl;
            });
        }
    }, function (response) {
        console.log(response);
        showErrorDialog("update task fail")
    });
}

checkInputValid = function () {
    frequencyType = getFrequencyDropdownVal();
    interval = getInterval();
    startDateTime = getNextProceedTime();
    console.log("getNextProceedTime:" + startDateTime);
    mailList = $("#mail_receiver_input").tagsinput('items');

    if (!leftRegionId || !rightRegionId) {
        showWarningDialog("please select data center");
        return false;
    }
    if (!leftEnvId || !rightEnvId) {
        showWarningDialog("please select environment");
        return false;
    }
    if (!leftFolder || !rightFolder) {
        showWarningDialog("please select folder");
        return false;
    }

    if (leftRegionId === rightRegionId && leftEnvId === rightEnvId && leftFolder === rightFolder) {
        showWarningDialog("please select different value");
        return false;
    }


    if (!interval) {
        showWarningDialog("please enter interval");
        return false;
    } else if (Number(interval) % 1 != 0) {
        showWarningDialog("please enter integer hour interval");
        return false;
    }

    if (!getProceedDate()) {
        showWarningDialog("please select next proceed date");
        return false;
    }

    if (!getProceedTime()) {
        showWarningDialog("please select next proceed time");
        return false;
    }

    if (mailList.length == 0) {
        showWarningDialog("please enter receiver");
        return false;
    }
    return true;
};