$(function () {
    $(".tagsinput").tagsinput();

    $("#select-country-list li").click(function () {
        $("#select-country-btn:first-child").text($(this).text());
        $("#select-country-btn:first-child").val($(this).val());
    });

    $("#select-env-list li").click(function () {
        $("#select-env-btn:first-child").text($(this).text());
        $("#select-env-btn:first-child").val($(this).val());
    });
});

let envId, countryId;
let filterKeyList = [];

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


function downloadSelectedRules(url) {
    downloadRulesFromBRE(url, getSelectedRules());
}

function downloadAllRules(url) {
    downloadRulesFromBRE(url, getAllRules());
}

function downloadRulesFromBRE(url, ruleNameList) {
    showWaitingDialog();

    if (!countryId) {
        showWarningDialog("please select country");
        return;
    } else if (!envId) {
        showWarningDialog("please select environment");
        return;
    } else if (ruleNameList == null || ruleNameList.length == 0) {
        showWarningDialog("please select ruleset to download");
        return;
    }

    let post_body = {
        "environment_id": envId,
        "country_id": countryId,
        "ruleset_name_list": ruleNameList
    };

    jQuery.ajax({
        url: url,
        method: 'POST',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data: JSON.stringify(post_body),
        mimeType: 'text/plain; charset=x-user-defined',
        responseType: 'arraybuffer',
    }).then(function success(data) {
        stopDialog();
        downloadZipFile(data, "rulesets");
    })
}

function getAllRules() {
    let allRuleNames = [];
    $('#row_checkbox_div input').each(function () {
        allRuleNames.push($(this).attr('name'));
    });
    return allRuleNames;
}

function getSelectedRules() {
    let selectedRuleNames = [];
    $('#row_checkbox_div input:checked').each(function () {
        selectedRuleNames.push($(this).attr('name'));
    });
    return selectedRuleNames;
}

function onCheckboxSelected() {
    let selectedCount = 0;
    $('#row_checkbox_div input:checked').each(function () {
        selectedCount++;
    });
    let button = document.getElementById('download_selected_btn');
    button.firstChild.data = "Download(" + selectedCount + ")";
    button.style.visibility = (selectedCount > 0) ? 'visible' : 'hidden';
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
