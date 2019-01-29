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
                let ruleNameTableDiv = document.getElementById('download_data_div');
                let ruleNameTableContentDiv = document.getElementById('show_rule_name_list_div');

                if (response.length > 0) {
                    ruleNameTableDiv.style.display = 'block';
                    ruleNameTableContentDiv.innerHTML = response;
                } else {
                    ruleNameTableDiv.style.display = 'none';
                }
                console.log(response);
            });
        }, function (response) {
            console.log(response);
            showErrorDialog("filter error")
        }
    )
    ;
};


function downloadSelectedRules(url) {
    let test = getSelectedRules();
    console.log("downloadSelectedRules:" + test);
    downloadPackedRules(url, getSelectedRules());
}

function downloadAllRules(url) {
    let test = getAllRules();
    console.log("downloadSelectedRules:" + test);
    downloadPackedRules(url, getAllRules());
}

function downloadPackedRules(url, ruleNameList) {
    showWaitingDialog();

    console.log("downloadPackedRules:" + ruleNameList);
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
        // transfer unicode data to characters
        let newContent = "";
        for (let i = 0; i < data.length; i++) {
            newContent += String.fromCharCode(data.charCodeAt(i) & 0xFF);
        }
        let bytes = new Uint8Array(newContent.length);
        for (let i = 0; i < newContent.length; i++) {
            bytes[i] = newContent.charCodeAt(i);
        }

        // use blob to download files
        let blob = new Blob([bytes], {type: "application/zip"});
        let element = document.createElement('a');
        element.href = URL.createObjectURL(blob);
        element.download = "ruleset.zip";
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    })
}

function getAllRules() {
    let allRuleNames = [];
    $('#check_box_rule_name_div input').each(function () {
        allRuleNames.push($(this).attr('name'));
    });
    return allRuleNames;
}

function getSelectedRules() {
    let selectedRuleNames = [];
    $('#check_box_rule_name_div input:checked').each(function () {
        selectedRuleNames.push($(this).attr('name'));
    });
    return selectedRuleNames;
}

function onCheckboxSelected() {
    let selectedCount = 0;
    $('#check_box_rule_name_div input:checked').each(function () {
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
