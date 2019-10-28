let regionId, environmentId, folderName, moduleName, onlyLatestVersion;
let filterKeyList = [];

$(function () {
    $(".tagsinput").tagsinput();

    $("#region_select_dropdown_list li").click(function () {
        $("#region_select_dropdown_btn:first-child").text($(this).text());
        $("#region_select_dropdown_btn:first-child").val($(this).val());
        regionId = $(this).val();
        onRegionSelected($(this).val());
    });

    initEnvironmentDropDownComponent();
    initFolderDropDownComponent();
});

initEnvironmentDropDownComponent = function () {
    $("#environment_select_dropdown_list li").click(function () {
        $("#environment_select_dropdown_btn:first-child").text($(this).text());
        $("#environment_select_dropdown_btn:first-child").val($(this).val());
        environmentId = $(this).val();
        onEnvironmentSelected();
    });
};

initFolderDropDownComponent = function () {
    $("#folder_select_dropdown_list li").click(function () {
        $("#folder_select_dropdown_btn:first-child").text($(this).text());
        $("#folder_select_dropdown_btn:first-child").val($(this).val());
        folderName = $(this).text();
        onFolderSelected();
    });
};

initModuleFolderDropDownComponent = function () {
    $("#module_select_dropdown_list li").click(function () {
        $("#module_select_dropdown_btn:first-child").text($(this).text());
        $("#module_select_dropdown_btn:first-child").val($(this).val());
        moduleName = $(this).text();
    });
};

filterEnvironments = function (regionId, postUrl) {
    let post_body = {
        "side": "left",
        "region_id": regionId
    };

    doPOST(postUrl, post_body, function (response) {
            let environmentDropDownDiv = document.getElementById('environment_select_dropdown_div');
            environmentDropDownDiv.innerHTML = response;
            initEnvironmentDropDownComponent();
        }, function (response) {
            console.log(response);
        }
    );
};

filterFolders = function (postUrl) {
    showWaitingDialog();
    let post_body = {
        "side": "left",
        "environment_id": environmentId,
        "region_id": regionId,
    };

    doPOST(postUrl, post_body, function (response) {
            let folderDropDownDiv = document.getElementById('folder_select_dropdown_div');
            folderDropDownDiv.innerHTML = response;
            initFolderDropDownComponent();
            stopDialog();
        }, function (response) {
            console.log(response);
        }
    );
};

filterModuleFolders = function (postUrl) {
    showWaitingDialog();
    let post_body = {
        "folder_name": folderName,
    };

    doPOST(postUrl, post_body, function (response) {
            let folderDropDownDiv = document.getElementById('module_select_dropdown_div');
            folderDropDownDiv.innerHTML = response;
            initModuleFolderDropDownComponent();
            stopDialog();
        }, function (response) {
            console.log(response);
        }
    );
};

filterFiles = function (postUrl) {
    showWaitingDialog();
    let validData = checkFilterValid();
    if (!validData)
        return;

    let post_body = {
        "region_id": regionId,
        "environment_id": environmentId,
        "folder_name": folderName,
        "module_name": moduleName,
        "filter_keys": filterKeyList,
        "only_latest_version": onlyLatestVersion
    };

    doPOST(postUrl, post_body, function (response) {
            successDialog("filter success", function () {
                let filterResultDiv = document.getElementById('filter_result_div');
                let selectAllBtn = document.getElementById('filter_result_select_all_btn_div');
                $('#filter_result_row_data_div').html(response);

                if (response.includes("No matching result")) {
                    selectAllBtn.style.display = 'none';
                } else {
                    selectAllBtn.style.display = 'block';
                }
                filterResultDiv.style.display = 'block';
            });
        }, function (response) {
            console.log(response);
            showErrorDialog("filter error")
        }
    )
    ;
};

checkFilterValid = function () {
    regionId = $("#region_select_dropdown_btn:first-child").val();
    environmentId = $("#environment_select_dropdown_btn:first-child").val();
    folderName = $("#folder_select_dropdown_btn:first-child").text();
    moduleName = $("#module_select_dropdown_btn:first-child").text();
    filterKeyList = $("#filter_tags_input").tagsinput('items');
    onlyLatestVersion = $('#only_latest_version_switch').bootstrapSwitch('state');

    if (!regionId) {
        showWarningDialog("please select data center");
        return false;
    }
    if (!environmentId) {
        showWarningDialog("please select environment");
        return false;
    }
    if (!folderName) {
        showWarningDialog("please select folder");
        return false;
    }

    if (!moduleName) {
        showWarningDialog("please select module");
        return false;
    }
    return true;
};

