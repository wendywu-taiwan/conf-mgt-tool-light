let leftRegionId, rightRegionId, filterEnvUrl;

$(function () {
    $("#left_select_region_list li").click(function () {
        if (leftRegionId === $(this).val())
            return;

        $("#left_select_region_btn:first-child").text($(this).text());
        $("#left_select_region_btn:first-child").val($(this).val());
        $("#left_region_id").val($(this).val());
        leftRegionId = $(this).val();
        filterEnvironments("left", leftRegionId);
    });

    $("#right_select_region_list li").click(function () {
        if (rightRegionId === $(this).val())
            return;

        $("#right_select_region_btn:first-child").text($(this).text());
        $("#right_select_region_btn:first-child").val($(this).val());
        $("#right_region_id").val($(this).val());
        rightRegionId = $(this).val();
        filterEnvironments("right", rightRegionId);
    });
});

resetRegionDropDownComponent = function () {
    $("#left_select_region_btn:first-child").text("Select");
    $("#left_select_region_btn:first-child").val(null);
    $("#left_region_id").val(null);
    leftRegionId = null;

    $("#right_select_region_btn:first-child").text($(this).text());
    $("#right_select_region_btn:first-child").val(null);
    $("#right_region_id").val(null);
    rightRegionId = null;
    resetEnvironmentDropDownComponent(true);
    resetFolderDropDownComponent(true);
};

setFilterEnvironmentUrl = function (url) {
    filterEnvUrl = url;
};

filterEnvironments = function (side, regionId) {
    filterEnvironmentsWithHandler(side, regionId, function (response) {
        successResponse(response, function () {
            let environmentDropDownDiv = document.getElementById(side + '_environment_dropdown_div');
            environmentDropDownDiv.innerHTML = response;
            initEnvironmentDropDownComponent();
            resetEnvironmentDropDownComponent(side, false);
            resetFolderDropDownComponent(side, true);
        });
    }, function (response) {
        resetEnvironmentDropDownComponent(side, true);
        resetFolderDropDownComponent(side, true);
        errorResponse(response);
    });
};

filterEnvironmentsWithHandler = function (side, regionId, success, failure) {
    showWaitingDialog();
    let post_body = {
        "side": side,
        "region_id": regionId
    };

    doPOST(filterEnvUrl, post_body, success, failure);
};
