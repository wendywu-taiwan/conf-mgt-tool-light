let leftFolder, rightFolder;

$(function () {
    initFolderDropDownComponent();
});

resetFolderDropDownComponent = function (side, removeOption) {
    if (side == "left")
        resetLeftFolderDropDownComponent(removeOption);
    else
        resetRightFolderDropDownComponent(removeOption);
};

resetLeftFolderDropDownComponent = function (removeOption) {
    $("#left_select_folder_btn:first-child").text("Select");
    $("#left_select_folder_btn:first-child").val(null);
    $("#left_folder").val(null);
    leftFolder = null;
    if (removeOption) {
        let list = document.getElementById('left_select_folder_list');
        list.innerHTML = '';
    }
};

resetRightFolderDropDownComponent = function (removeOption) {
    $("#right_select_folder_btn:first-child").text("Select");
    $("#right_select_folder_btn:first-child").val(null);
    $("#right_folder").val(null);
    rightFolder = null;
    if (removeOption) {
        let list = document.getElementById('right_select_folder_list');
        list.innerHTML = '';
    }
};


initFolderDropDownComponent = function () {
    $("#left_select_folder_list li").click(function () {
        $("#left_select_folder_btn:first-child").text($(this).text());
        $("#left_select_folder_btn:first-child").val($(this).val());
        $("#left_folder").val($(this).text());
        leftFolder = $(this).text();
    });

    $("#right_select_folder_list li").click(function () {
        $("#right_select_folder_btn:first-child").text($(this).text());
        $("#right_select_folder_btn:first-child").val($(this).val());
        $("#right_folder").val($(this).text());
        rightFolder = $(this).text();
    });
};
