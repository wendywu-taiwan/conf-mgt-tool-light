let regionId, environmentId, countryFolder, moduleFolder, latestVersionFolder, onlyLatestVersion;
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

    $('#only_latest_version_switch').on('switchChange.bootstrapSwitch', function (event, state) {
        let latestVersionDropdown = document.getElementById("latest_version_select_div");
        if ($("#only_latest_version_switch").is(':checked')) {
            removeWithAnimate(latestVersionDropdown, 300);
        } else {
            latestVersionDropdown.style.display = 'flex';
        }
    });
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
        countryFolder = $(this).text();
        onFolderSelected();
    });
};

initModuleFolderDropDownComponent = function () {
    $("#module_select_dropdown_list li").click(function () {
        $("#module_select_dropdown_btn:first-child").text($(this).text());
        $("#module_select_dropdown_btn:first-child").val($(this).val());
        moduleFolder = $(this).text();
        onModuleSelected();
    });
};

initLatestVersionFolderDropDownComponent = function () {
    $("#latest_version_select_dropdown_list li").click(function () {
        $("#latest_version_select_dropdown_btn:first-child").text($(this).text());
        $("#latest_version_select_dropdown_btn:first-child").val($(this).val());
        latestVersionFolder = $(this).text();
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
        "environment_id": environmentId,
        "region_id": regionId,
        "folder_name": countryFolder,
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


filterLatestVersionFolders = function (postUrl) {
    showWaitingDialog();
    let post_body = {
        "environment_id": environmentId,
        "region_id": regionId,
        "country_folder": countryFolder,
        "module_folder": moduleFolder
    };

    doPOST(postUrl, post_body, function (response) {
            refreshPartialHTML("latest_version_select_dropdown_div", response);
            initLatestVersionFolderDropDownComponent();
            stopDialog();
        }, function (response) {
            console.log(response);
        }
    );
};

onClickSearchButton = function (filterFilesUrl, fileListUrl) {
    showWaitingDialog();
    let validData = checkFilterValid();
    if (!validData)
        return;

    let postBody = {
        "region_id": regionId,
        "environment_id": environmentId,
        "country_folder": countryFolder,
        "module_folder": moduleFolder,
        "latest_version_folder": latestVersionFolder,
        "filter_keys": filterKeyList,
        "only_latest_version": onlyLatestVersion
    };

    if (filterKeyList.length == 0) {
        getFilesList(fileListUrl, postBody);
    } else {
        filterFiles(filterFilesUrl, postBody);
    }
};

filterFiles = function (postUrl, postBody) {
    doPOST(postUrl, postBody, function (response) {
            successDialog("filter success", function () {
                let fileListDiv = document.getElementById('file_list_div');
                let filterResultDiv = document.getElementById('filter_result_div');
                let selectAllBtn = document.getElementById('filter_result_select_all_btn_div');
                $('#filter_result_row_data_div').html(response);

                if (response.includes("No matching result")) {
                    selectAllBtn.style.display = 'none';
                } else {
                    selectAllBtn.style.display = 'block';
                }
                fileListDiv.style.display = 'none';
                filterResultDiv.style.display = 'block';
            });
        }, function (response) {
            console.log(response);
            showErrorDialog("filter error")
        }
    )
    ;
};

getFilesList = function (postUrl, postBody) {

    doPOST(postUrl, postBody, function (response) {
            successDialog("filter success", function () {
                let filterResultDiv = document.getElementById('filter_result_div');
                let fileListDiv = document.getElementById('file_list_div');
                let selectAllBtn = document.getElementById('file_list_select_all_btn_div');
                $('#file_list_row_list_div').html(response);

                if (response.includes("No matching result")) {
                    selectAllBtn.style.display = 'none';
                } else {
                    selectAllBtn.style.display = 'block';
                }
                filterResultDiv.style.display = 'none';
                fileListDiv.style.display = 'block';
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
    countryFolder = $("#folder_select_dropdown_btn:first-child").text();
    moduleFolder = $("#module_select_dropdown_btn:first-child").text();
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
    if (!countryFolder) {
        showWarningDialog("please select folder");
        return false;
    }

    if (!moduleFolder) {
        showWarningDialog("please select module");
        return false;
    }
    return true;
};

