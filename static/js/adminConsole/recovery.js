$(function () {
    $(".tagsinput").tagsinput();

    $("#select-env-list li").click(function () {
        $("#select-env-btn:first-child").text($(this).text());
        $("#select-env-btn:first-child").val($(this).val());
        onEnvironmentSelected($(this).val());
    });

    initCountryDropDown();
});

let envId, countryId, backupKey, currentTargetEnvId;
let filterKeyList = [];
let rulesetsMap = {};
let allRulesetMaps = {};
let allRulesetsRecoveredArray = [];
let recoveryUrl, currentRulesetListDiv;

initRecoveryUrl = function (url) {
    recoveryUrl = url;
};

initCountryDropDown = function () {
    $("#select-country-list li").click(function () {
        $("#select-country-btn:first-child").text($(this).text());
        $("#select-country-btn:first-child").val($(this).val());
    });
};

filterCountries = function (environmentId, postUrl) {
    let post_body = {
        "environment_id": environmentId
    };

    doPOST(postUrl, post_body, function (response) {
            let countryDropDownDiv = document.getElementById('select_country_div');
            countryDropDownDiv.innerHTML = response;
            initCountryDropDown();
        }, function (response) {
            console.log(response);
        }
    )
    ;
};

filterBackupRules = function (postUrl) {
    showWaitingDialog();
    checkFilterValid();

    let validData = checkFilterValid();
    if (!validData)
        return;

    let post_body = {
        "environment_id": envId,
        "country_id": countryId,
        "filter_keys": filterKeyList
    };

    doPOST(postUrl, post_body, function (response) {
            successDialog("filter success", function () {
                let backupDataDiv = document.getElementById('back_up_data_div');
                backupDataDiv.style.display = 'block';
                backupDataDiv.innerHTML = response;
            });
        }, function (response) {
            console.log(response);
            showErrorDialog("filter error")
        }
    );
};

applyRulesetsRecover = function () {
    if (Object.keys(rulesetsMap).length == 0) {
        showWarningDialog("please select at least one ruleset to recover");
        return;
    }

    showWaitingDialog();
    let ruleset, rulesetAction;
    let appliedRulesets = [];

    for (ruleset in rulesetsMap) {
        rulesetAction = rulesetsMap[ruleset];
        appliedRulesets.push(ruleset);
    }

    let post_body = {
        "target_environment_id": currentTargetEnvId,
        "country_id": countryId,
        "backup_key": backupKey,
        "applied_rulesets": appliedRulesets,
    };

    doPOST(recoveryUrl, post_body, function (response) {
            let statusCode = response["status_code"];
            let message = response["message"];

            if (response == null || statusCode != 200) {
                showErrorDialog(message);
                return;
            }

            successDialog("recover finish", function () {
                    let failedRulesets = response["data"]["failed_rulesets"];
                    let updateRulesets = response["data"]["updated_rulesets"];
                    let createRulesets = response["data"]["created_rulesets"];
                    let deletedRulesets = response["data"]["deleted_rulesets"];

                    checkAllRecover(failedRulesets, updateRulesets, createRulesets, deletedRulesets);
                    showFailureRulesetRow(failedRulesets);
                    showSuccessRulesetRow(updateRulesets);
                    showSuccessRulesetRow(createRulesets);
                    showSuccessRulesetRow(deletedRulesets);
                }
            );
        }, function (response) {
            console.log("response:" + String(response));
            showErrorDialog("recover error")
        }
    )
    ;
};

openDiffResultPage = function (url) {
    showWaitingDialog();
    doGET(url, function (response) {
        let statusCode = response["status_code"];
        if (statusCode == null) {
            stopDialog();
            window.open(url);
        } else {
            if (statusCode == 233)
                showSuccessDialog("Ruleset is no difference.");
            if (statusCode == 500)
                showErrorDialog(response["message"])
        }
    }, function (response) {
        showErrorDialog(response);
    });
};

function checkAllRecover(failedRulesets, updateRulesets, createRulesets, deletedRulesets) {
    let failedCount = failedRulesets == null ? 0 : failedRulesets.length;
    let createdCount = createRulesets == null ? 0 : createRulesets.length;
    let updatedCount = updateRulesets == null ? 0 : updateRulesets.length;
    let deletedCount = deletedRulesets == null ? 0 : deletedRulesets.length;
    let recoverRulesetCount = failedCount + createdCount + updatedCount + deletedCount;
    if (recoverRulesetCount == Object.keys(allRulesetMaps).length) {
        allRulesetsRecoveredArray.push(backupKey);
        changeButtonStatus(false);
    } else {
        changeButtonStatus(true);
    }
}

function showSuccessRulesetRow(rulesetList) {
    let count = rulesetList.length;
    if (rulesetList == null || count == 0) {
        return;
    }

    for (let i = 0; i < count; i++) {
        let ruleset = rulesetList[i];
        let rulesetName = ruleset["ruleset_name"];

        let normalRulesetRow = document.getElementById(backupKey + "_" + rulesetName + '_checked_row_div');
        let failedRulesetRow = document.getElementById(backupKey + "_" + rulesetName + '_fail_row_div');
        let successRulesetRow = document.getElementById(backupKey + "_" + rulesetName + '_success_row_div');
        normalRulesetRow.style.display = 'none';
        failedRulesetRow.style.display = 'none';
        successRulesetRow.style.display = 'block';
    }
}

function showFailureRulesetRow(rulesetList) {
    let count = rulesetList.length;
    if (rulesetList == null || count == 0) {
        return;
    }

    for (let i = 0; i < count; i++) {
        let ruleset = rulesetList[i];
        let rulesetName = ruleset["ruleset_name"];

        let normalRulesetRow = document.getElementById(backupKey + "_" + rulesetName + '_checked_row_div');
        let failedRulesetRow = document.getElementById(backupKey + "_" + rulesetName + '_fail_row_div');
        let successRulesetRow = document.getElementById(backupKey + "_" + rulesetName + '_success_row_div');
        let exceptionDiv = document.getElementById(backupKey + "_" + rulesetName + '_row_exception_div');

        normalRulesetRow.style.display = 'none';
        failedRulesetRow.style.display = 'block';
        successRulesetRow.style.display = 'none';
        exceptionDiv.innerHTML = ruleset["exception"]
    }
}

function showNormalRulesetRow(rulesetName) {
    let normalRulesetRow = document.getElementById(backupKey + "_" + rulesetName + '_checked_row_div');
    let failedRulesetRow = document.getElementById(backupKey + "_" + rulesetName + '_fail_row_div');
    let successRulesetRow = document.getElementById(backupKey + "_" + rulesetName + '_success_row_div');
    normalRulesetRow.style.display = 'block';
    failedRulesetRow.style.display = 'none';
    successRulesetRow.style.display = 'none';
}

checkFilterValid = function () {
    envId = $("#select-env-btn:first-child").val();
    countryId = $("#select-country-btn:first-child").val();
    filterKeyList = $("#filter_tags_input").tagsinput('items');

    if (!countryId) {
        showWarningDialog("please select country");
        return false;
    }
    if (!envId) {
        showWarningDialog("please select environment");
        return false;
    }
    return true;
};

function onSelectedRules(inputItem, rulesetName, action) {
    rulesetsMap[rulesetName] = action;
    if (inputItem.checked) {
        rulesetsMap[rulesetName] = action;
    } else {
        delete rulesetsMap[rulesetName];
    }
}

function addAllRulesets() {
    let container = currentRulesetListDiv;
    let inputs = container.getElementsByTagName('input');
    for (let index = 0; index < inputs.length; ++index) {
        let input = inputs[index];
        allRulesetMaps[input.name] = input.value;
    }
}

function applyAllRulesets() {
    let container = currentRulesetListDiv;
    let inputs = container.getElementsByTagName('input');
    for (let index = 0; index < inputs.length; ++index) {
        let input = inputs[index];
        input.checked = true;
    }
    rulesetsMap = allRulesetMaps;
}

function clearAllInputSelected() {
    if (currentRulesetListDiv == null) {
        return;
    }

    rulesetsMap = {};
    allRulesetMaps = {};

    let container = currentRulesetListDiv;
    let inputs = container.getElementsByTagName('input');
    for (let index = 0; index < inputs.length; ++index) {
        let input = inputs[index];
        input.checked = false;
    }
}

onClickBackupFolderRow = function (backupId, targetEnvId) {
    console.log("backupId:" + backupId + ", targetEnvId:" + targetEnvId);
    backupKey = backupId;
    currentTargetEnvId = targetEnvId;

    clearAllInputSelected();
    removeWithAnimate(document.getElementById('filter_env_country_div'));
    var rowElements = document.getElementsByClassName('content_row_div');
    var i, rowElement, rowElementId, rowElementRulesetDiv;
    for (i = 0; i < rowElements.length; i++) {
        rowElement = rowElements[i];
        rowElementId = rowElement.id;
        rowElementRulesetDiv = document.getElementById(rowElementId + "_rulesets_div");
        if (rowElementId == backupId) {
            rowElementRulesetDiv.style.display = 'block';
            rowElement.style.backgroundColor = '#edf9f6';
            currentRulesetListDiv = rowElementRulesetDiv;
            addAllRulesets();
        } else {
            rowElementRulesetDiv.style.display = 'none';
            rowElement.style.backgroundColor = 'white';
        }
    }
    // check if all rulesets been recovered
    if (arrayContains(backupKey, allRulesetsRecoveredArray)) {
        changeButtonStatus(false);
    } else {
        changeButtonStatus(true);
    }
};

function changeButtonStatus(status) {
    let button_group_div = document.getElementById(backupKey + "_button_group_div");
    if (status) {
        button_group_div.style.display = 'flex';
    } else {
        button_group_div.style.display = 'none';
    }
}

function removeWithAnimate(obj) {
    obj.style.opacity = '0';
    window.setTimeout(
        function removeThis() {
            obj.style.display = 'none';
        }, 500);
}
