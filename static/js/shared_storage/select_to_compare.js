let leftEnvId, rightEnvId, leftRegionId, rightRegionId, leftFolder, rightFolder;


$(function () {
    $("#left_select_region_list li").click(function () {
        $("#left_select_region_btn:first-child").text($(this).text());
        $("#left_select_region_btn:first-child").val($(this).val());
        $("#left_region_id").val($(this).val());
        leftRegionId = $(this).val();
        onRegionSelected("left", $(this).val());
    });

    $("#right_select_region_list li").click(function () {
        $("#right_select_region_btn:first-child").text($(this).text());
        $("#right_select_region_btn:first-child").val($(this).val());
        $("#right_region_id").val($(this).val());
        rightRegionId = $(this).val();
        onRegionSelected("right", $(this).val());
    });

    initEnvironmentDropDownComponent();
    initFolderDropDownComponent();

    $("#compare_submit_button").click(function () {
        showWaitingDialog();
    });
});

initEnvironmentDropDownComponent = function () {
    $("#left_select_environment_list li").click(function () {
        $("#left_select_environment_btn:first-child").text($(this).text());
        $("#left_select_environment_btn:first-child").val($(this).val());
        $("#left_environment_id").val($(this).val());
        leftEnvId = $(this).val();
        onEnvironmentSelected("left");
    });

    $("#right_select_environment_list li").click(function () {

        $("#right_select_environment_btn:first-child").text($(this).text());
        $("#right_select_environment_btn:first-child").val($(this).val());
        $("#right_environment_id").val($(this).val());
        rightEnvId = $(this).val();
        onEnvironmentSelected("right");
    });
};

initFolderDropDownComponent = function () {
    $("#left_select_folder_list li").click(function () {
        $("#left_select_folder_btn:first-child").text($(this).text());
        $("#left_select_folder_btn:first-child").val($(this).val());
        $("#left_folder").val($(this).val());
        leftFolder = $(this).text();
    });

    $("#right_select_folder_list li").click(function () {

        $("#right_select_folder_btn:first-child").text($(this).text());
        $("#right_select_folder_btn:first-child").val($(this).val());
        $("#right_folder").val($(this).val());
        rightFolder = $(this).text();
    });

};

filterEnvironments = function (side, regionId, postUrl) {
    let post_body = {
        "side": side,
        "region_id": regionId
    };

    doPOST(postUrl, post_body, function (response) {
            let environmentDropDownDiv = document.getElementById(side + '_environment_dropdown_div');
            environmentDropDownDiv.innerHTML = response;
            initEnvironmentDropDownComponent();
        }, function (response) {
            console.log(response);
        }
    );
};

filterFolders = function (side, postUrl) {
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

    doPOST(postUrl, post_body, function (response) {
            let folderDropDownDiv = document.getElementById(side + '_folder_dropdown_div');
            folderDropDownDiv.innerHTML = response;
            initFolderDropDownComponent();
            stopDialog();
        }, function (response) {
            console.log(response);
        }
    );
};
