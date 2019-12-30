$(function () {
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


let baseEnvId, compareEnvId, interval, startDateTime, frequencyType, displayName;
let countryList = [];
let mailList = [];
let mailContentTypeList = [];
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
        "mail_content_type_list": mailContentTypeList,
        "mail_list": mailList,
        "frequency_type": frequencyType,
        "interval": interval,
        "start_date_time": startDateTime,
        "display_name": displayName,
        "skip_rulesets": generateSkipRulesetData()

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
        "start_date_time": startDateTime,
        "display_name": displayName,
        "skip_rulesets": generateSkipRulesetData()
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
};

checkInputValid = function () {
    displayName = $("#display_name_input").val();
    baseEnvId = $("#select_base_env_btn:first-child").val();
    compareEnvId = $("#select_compare_env_btn:first-child").val();
    frequencyType = getFrequencyDropdownVal();
    interval = getInterval();
    startDateTime = getNextProceedTime();
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

    if (mailContentTypeList.length == 0) {
        showWarningDialog("please select mail content");
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
countryCheckboxOnClick = function (countryId) {
    let addSkipRulesetDiv = document.getElementById(countryId + "_add_skip_ruleset_list_div");
    showFlex(addSkipRulesetDiv);
    countryList.push(countryId);
};

mailContentTypeCheckboxOnClick = function (mailContentId) {
    mailContentTypeList.push(mailContentId);
};

countryCheckboxOnChange = function (checkboxItem) {
    let countryId = checkboxItem.value;
    let addSkipRulesetDiv = document.getElementById(countryId + "_add_skip_ruleset_list_div");
    let skipRulesetInputDiv = document.getElementById(countryId + "_skip_ruleset_list_input_div");

    if (checkboxItem.checked && !countryList.includes(countryId)) {
        countryCheckboxOnClick(countryId);
    } else {
        clearTagsInput(countryId + "_skip_ruleset_list_input");
        hide(addSkipRulesetDiv);
        hide(skipRulesetInputDiv);
        countryList = countryList.filter(function (item) {
            return item !== countryId;
        })
    }
};

addSkipRulesetOnClick = function (divItem) {
    let divId = divItem.id;
    let countryId = split_str(divId, 0);
    showSkipRulesetDiv(countryId);
};

mailContentTypeCheckboxOnChange = function (checkboxItem) {
    let mailContentId = checkboxItem.value;
    if (checkboxItem.checked && !mailContentTypeList.includes(mailContentId)) {
        mailContentTypeCheckboxOnClick(mailContentId)
    } else {
        mailContentTypeList = mailContentTypeList.filter(function (item) {
            return item !== mailContentId;
        })
    }
};
showSkipRulesetDiv = function (countryId) {
    let addSkipRulesetInputDiv = document.getElementById(countryId + "_add_skip_ruleset_list_div");
    let skipRulesetInputDiv = document.getElementById(countryId + "_skip_ruleset_list_input_div");
    hide(addSkipRulesetInputDiv);
    showFlex(skipRulesetInputDiv);
};

generateSkipRulesetData = function () {
    let skipRulesetsList = [];
    for (let index in countryList) {
        countryId = countryList[index];
        let tagsInputId = countryId + "_skip_ruleset_list_input";
        let skipRulesets = getValueTagsInput(tagsInputId);

        let skipRulesetObject = {
            "country_id": countryId,
            "ruleset_list": skipRulesets
        };
        skipRulesetsList.push(skipRulesetObject)
    }
    return skipRulesetsList;
};