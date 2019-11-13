let regionId, environmentId, countryFolder, moduleFolder, versionFolder;
let filterKeyList = [];
let downloadFileUrl;
$(function () {
    $(".tagsinput").tagsinput();

    $("#region_select_dropdown_list li").click(function () {
        $("#region_select_dropdown_btn:first-child").text($(this).text());
        $("#region_select_dropdown_btn:first-child").val($(this).val());

        if (regionId == $(this).val()) {
            return;
        }
        regionId = $(this).val();
        resetResultBlock();
        resetEnvironmentDropDown();
        resetFolderDropDown();
        resetModuleDropDown();
        resetLastVersionDropDown();
        onRegionSelected($(this).val());
    });

    initEnvironmentDropDownComponent();
    initFolderDropDownComponent();
});

initDownloadFileUrl = function (url) {
    downloadFileUrl = url;
};

initEnvironmentDropDownComponent = function () {
    $("#environment_select_dropdown_list li").click(function () {
        $("#environment_select_dropdown_btn:first-child").text($(this).text());
        $("#environment_select_dropdown_btn:first-child").val($(this).val());

        if (environmentId == $(this).val()) {
            return;
        }
        environmentId = $(this).val();
        resetResultBlock();
        resetFolderDropDown();
        resetModuleDropDown();
        resetLastVersionDropDown();
        onEnvironmentSelected();
    });
};

initFolderDropDownComponent = function () {
    $("#folder_select_dropdown_list li").click(function () {
        $("#folder_select_dropdown_btn:first-child").text($(this).text());
        $("#folder_select_dropdown_btn:first-child").val($(this).val());
        if (countryFolder == $(this).val()) {
            return;
        }
        countryFolder = $(this).text();
        resetResultBlock();
        resetModuleDropDown();
        resetLastVersionDropDown();
        onFolderSelected();
    });
};

initModuleFolderDropDownComponent = function () {
    $("#module_select_dropdown_list li").click(function () {
        $("#module_select_dropdown_btn:first-child").text($(this).text());
        $("#module_select_dropdown_btn:first-child").val($(this).val());
        if (moduleFolder == $(this).val()) {
            return;
        }
        moduleFolder = $(this).text();
        resetResultBlock();
        resetLastVersionDropDown();
        onModuleSelected();
    });
};

initLatestVersionFolderDropDownComponent = function () {
    $("#latest_version_select_dropdown_list li").click(function () {
        $("#latest_version_select_dropdown_btn:first-child").text($(this).text());
        $("#latest_version_select_dropdown_btn:first-child").val($(this).val());
        if (versionFolder == $(this).val()) {
            return;
        }
        versionFolder = $(this).text();
        resetResultBlock();
    });
};
resetEnvironmentDropDown = function () {
    resetDropdown("environment_select_dropdown_btn");
    environmentId = null;
};

resetFolderDropDown = function () {
    resetDropdown("folder_select_dropdown_btn");
    countryFolder = DROPDOWN_OPTION_SELECT;
};

resetModuleDropDown = function () {
    resetDropdown("module_select_dropdown_btn");
    moduleFolder = DROPDOWN_OPTION_SELECT;
};

resetLastVersionDropDown = function () {
    resetDropdown("latest_version_select_dropdown_btn");
    versionFolder = DROPDOWN_OPTION_SELECT;
};

resetResultBlock = function () {
    $('#filter_result_select_all_btn').text("Select All");
    $('#file_list_select_all_btn').text("Select All");
    changeFilterResultDownloadBtnVisibility(false, 0);
    changeFileListDownloadBtnVisibility(false, 0);

    let filterResultDiv = document.getElementById('filter_result_div');
    let fileListDiv = document.getElementById('file_list_div');

    filterResultDiv.style.display = "none";
    fileListDiv.style.display = "none";
};

filterEnvironments = function (regionId, postUrl) {
    let post_body = {
        "side": "left",
        "region_id": regionId
    };

    doPOST(postUrl, post_body, function (response) {
            successResponse(response, function () {
                let environmentDropDownDiv = document.getElementById('environment_select_dropdown_div');
                environmentDropDownDiv.innerHTML = response;
                initEnvironmentDropDownComponent();
            });
        }, function (response) {
            errorResponse(response);
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
            successResponse(response, function () {
                let folderDropDownDiv = document.getElementById('folder_select_dropdown_div');
                folderDropDownDiv.innerHTML = response;
                initFolderDropDownComponent();
            });
        }, function (response) {
            errorResponse(response);
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
            successResponse(response, function () {
                let folderDropDownDiv = document.getElementById('module_select_dropdown_div');
                folderDropDownDiv.innerHTML = response;
                initModuleFolderDropDownComponent();
            });
        }, function (response) {
            errorResponse(response);
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
            successResponse(response, function () {
                refreshPartialHTML("latest_version_select_dropdown_div", response);
                initLatestVersionFolderDropDownComponent();
            });
        }, function (response) {
            errorResponse(response);
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
        "latest_version_folder": versionFolder,
        "filter_keys": filterKeyList,
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
                    let statusCode = response["status_code"];
                    let fileListDiv = document.getElementById('file_list_div');
                    let filterResultDiv = document.getElementById('filter_result_div');
                    let selectAllBtn = document.getElementById('filter_result_select_all_btn_div');
                    $('#filter_result_row_data_div').html(response);

                    if (statusCode == 208) {
                        selectAllBtn.style.display = 'none';
                    } else {
                        selectAllBtn.style.display = 'block';
                    }
                    fileListDiv.style.display = 'none';
                    filterResultDiv.style.display = 'block';
                    checkFilterResultDownloadBtnVisibility();
                    checkFilterResultSelectAllBtnStatus();
                }
            );
        }, function (response) {
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
    versionFolder = $("#latest_version_select_dropdown_btn:first-child").text();
    console.log("checkFilterValid, versionFolder:" + versionFolder);
    filterKeyList = $("#filter_tags_input").tagsinput('items');

    if (!regionId) {
        showWarningDialog("please select data center");
        return false;
    }
    if (!environmentId) {
        showWarningDialog("please select environment");
        return false;
    }
    if (countryFolder === DROPDOWN_OPTION_SELECT) {
        showWarningDialog("please select country");
        return false;
    }

    if (moduleFolder === DROPDOWN_OPTION_SELECT) {
        showWarningDialog("please select module");
        return false;
    }

    if (versionFolder === DROPDOWN_OPTION_SELECT) {
        showWarningDialog("please select version");
        return false;
    }
    return true;
};

function downloadFiles(inputs) {
    showWaitingDialog();
    let inputCounts = inputs.length;
    let i, input;
    let selectFilePathArray = [];

    for (i = 0; i < inputCounts; i++) {
        input = inputs[i];
        selectFilePathArray.push(input.value);
        console.log("onClickDownloadBtn, add file path:" + input.value)
    }

    let post_body = {
        "region_id": regionId,
        "environment_id": environmentId,
        "file_path_list": selectFilePathArray
    };

    jQuery.ajax({
        url: downloadFileUrl,
        method: 'POST',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data: JSON.stringify(post_body),
        mimeType: 'text/plain; charset=x-user-defined',
        responseType: 'arraybuffer',
    }).then(function success(data) {
        stopDialog();
        downloadZipFile(data, "files");
    })
}

