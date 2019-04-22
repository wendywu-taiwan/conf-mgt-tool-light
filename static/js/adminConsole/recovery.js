$(function () {
    $(".tagsinput").tagsinput();

    $("#select-env-list li").click(function () {
        $("#select-env-btn:first-child").text($(this).text());
        $("#select-env-btn:first-child").val($(this).val());
        onEnvironmentSelected($(this).val());
    });

    initCountryDropDown();
});

let envId, countryId, backupFolderName;
let filterKeyList = [];
let rulesetsMap = {};

initCountryDropDown = function () {
    $("#select-country-list li").click(function () {
        $("#select-country-btn:first-child").text($(this).text());
        $("#select-country-btn:first-child").val($(this).val());
    });
}

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


filterRules = function (postUrl) {
    showWaitingDialog();
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
                let downloadAllBtn = document.getElementById('download_all_btn_div');
                let ruleNameTableDiv = document.getElementById('download_data_div');
                let ruleNameTableContentDiv = document.getElementById('show_rule_name_list_div');

                ruleNameTableDiv.style.display = 'block';
                ruleNameTableContentDiv.innerHTML = response;
                if (response.includes("No matching result")) {
                    downloadAllBtn.style.display = 'none';
                } else {
                    downloadAllBtn.style.display = 'block';
                }
                // refresh download selected btn status
                onCheckboxSelected();
            });
        }, function (response) {
            console.log(response);
            showErrorDialog("filter error")
        }
    )
    ;
};


applyRulesetsRecover = function (postUrl) {
    let ruleset, rulesetAction;
    let createdRulesets = [];
    let updatedRulesets = [];
    let deletedRulesets = [];

    for (ruleset in rulesetsMap) {
        rulesetAction = rulesetsMap[ruleset];
        if (rulesetAction == "created") {
            createdRulesets.push(ruleset);
        } else if (rulesetAction == "updated") {
            updatedRulesets.push(ruleset);
        } else {
            deletedRulesets.push(ruleset);
        }
    }

    let post_body = {
        "environment_id": envId,
        "country_id": countryId,
        "select_folder_name": backupFolderName,
        "created_rulesets": createdRulesets,
        "updated_rulesets": updatedRulesets,
        "deleted_rulesets": deletedRulesets
    };

    doPOST(postUrl, post_body, function (response) {
            successDialog("recover success", function () {
            });
        }, function (response) {
            console.log(response);
            showErrorDialog("recover error")
        }
    )
    ;
};

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

    for (var a in rulesetsMap) {
        console.log(a);
        console.log(rulesetsMap[a]);
    }
}

function getSelectedRules() {
    let selectedRuleNames = [];
    $('#row_checkbox_div input:checked').each(function () {
        selectedRuleNames.push($(this).attr('name'));
    });
    console.log("selectedRuleNames:" + selectedRuleNames);
    return selectedRuleNames;
}

onClickBackupFolderRow = function (selectedItem) {
    removeWithAnimate(document.getElementById('filter_env_country_div'));
    var rowElements = document.getElementsByClassName('content_row_div');
    var selectedItemId = selectedItem.id;
    var i, rowElement, rowElementId, rowElementRulesetDiv;
    for (i = 0; i < rowElements.length; i++) {
        rowElement = rowElements[i];
        rowElementId = rowElement.id;
        rowElementRulesetDiv = document.getElementById(rowElementId + "_rulesets_div");
        if (rowElementId == selectedItemId) {
            backupFolderName = rowElementId;
            rowElementRulesetDiv.style.display = 'block';
            rowElement.style.backgroundColor = '#edf9f6';
        } else {
            rowElementRulesetDiv.style.display = 'none';
            rowElement.style.backgroundColor = 'white';
        }
    }
};

function removeWithAnimate(obj) {
    obj.style.opacity = '0';
    window.setTimeout(
        function removeThis() {
            obj.style.display = 'none';
        }, 500);
}
