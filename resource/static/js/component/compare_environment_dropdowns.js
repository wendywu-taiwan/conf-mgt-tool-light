let leftEnvId, rightEnvId, filterFolderUrl;

$(function () {
    initEnvironmentDropDownComponent();
});

resetEnvironmentDropDownComponent = function (side, removeOption) {
    if (side == "left")
        resetLeftEnvironmentDropDownComponent(removeOption);
    else
        resetRightEnvironmentDropDownComponent(removeOption);
};


resetLeftEnvironmentDropDownComponent = function (removeOption) {
    $("#left_select_environment_btn:first-child").text("Select");
    $("#left_select_environment_btn:first-child").val(null);
    $("#left_environment_id").val(null);
    leftEnvId = null;
    if (removeOption) {
        let list = document.getElementById('left_select_environment_list');
        list.innerHTML = '';
    }
};

resetRightEnvironmentDropDownComponent = function (removeOption) {
    $("#right_select_environment_btn:first-child").text("Select");
    $("#right_select_environment_btn:first-child").val(null);
    $("#right_environment_id").val(null);
    rightEnvId = null;
    if (removeOption) {
        let list = document.getElementById('right_select_environment_list');
        list.innerHTML = '';
    }
};

initEnvironmentDropDownComponent = function () {
    $("#left_select_environment_list li").click(function () {
        if ($(this).val() === leftEnvId)
            return;

        leftFolder = null;
        $("#left_select_environment_btn:first-child").text($(this).text());
        $("#left_select_environment_btn:first-child").val($(this).val());
        $("#left_environment_id").val($(this).val());
        leftEnvId = $(this).val();
        filterFolders("left");
    });

    $("#right_select_environment_list li").click(function () {
        if ($(this).val() === rightEnvId)
            return;

        rightFolder = null;
        $("#right_select_environment_btn:first-child").text($(this).text());
        $("#right_select_environment_btn:first-child").val($(this).val());
        $("#right_environment_id").val($(this).val());
        rightEnvId = $(this).val();
        filterFolders("right");
    });
};

setFilterFolderUrl = function (url) {
    filterFolderUrl = url;
};

filterFolders = function (side) {
    filterFoldersWithHandler(side, function (response) {
        successResponse(response, function () {
            let folderDropDownDiv = document.getElementById(side + '_folder_dropdown_div');
            folderDropDownDiv.innerHTML = response;
            initFolderDropDownComponent();
            resetFolderDropDownComponent(side, false);
        });
    }, function (response) {
        resetFolderDropDownComponent(side, true);
        errorResponse(response);
    });
};

filterFoldersWithHandler = function (side, success, failure) {
    showWaitingDialog();
    let post_body;
    if (side == "left") {
        post_body = {
            "side": side,
            "environment_id": leftEnvId,
            "region_id": leftRegionId
        };
    } else {
        post_body = {
            "side": side,
            "environment_id": rightEnvId,
            "region_id": rightRegionId
        };
    }

    doPOST(filterFolderUrl, post_body, success, failure);
};