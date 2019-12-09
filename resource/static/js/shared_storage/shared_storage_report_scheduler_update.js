function setLeftDataCenter(id, name) {
    leftRegionId = id;
    setDropdown('left_select_region_btn', id, name);
}

function setRightDataCenter(id, name) {
    rightRegionId = id;
    setDropdown('right_select_region_btn', id, name);
}

function setLeftEnvironment(id, name) {
    leftEnvId = id;
    setDropdown("left_select_environment_btn", id, name);
}

function setRightEnvironment(id, name) {
    setDropdown("right_select_environment_btn", id, name);
    rightEnvId = id;
}

function setLeftFolder(name) {
    setDropdown("left_select_folder_btn", name, name);
    leftFolder = name;
}

function setRightFolder(name) {
    setDropdown("right_select_folder_btn", name, name);
    rightFolder = name;
}


let receivers = [];

function addReceivers(receiver) {
    receivers.push(receiver)
}

function setReceivers() {
    for (var i = 0; i < receivers.length; i++) {
        var receiver = receivers[i];
        $('#mail_receiver_input').tagsinput('add', "");
        $('#mail_receiver_input').tagsinput('add', receiver);
    }
}

setDefaultEnvironmentDropDown = function (side, regionId, envId, envName) {
    filterEnvironmentsWithHandler(side, regionId, function (response) {
        let statusCode = response["status_code"];
        if (statusCode == null || statusCode == 200) {
            let environmentDropDownDiv = document.getElementById(side + '_environment_dropdown_div');
            environmentDropDownDiv.innerHTML = response;
            initEnvironmentDropDownComponent();
            setDropdown(side + "_select_environment_btn", envId, envName);
        }
    }, function (response) {
        errorResponse(response);
    });
};

setDefaultFolderDropDown = function (side, folder) {
    filterFoldersWithHandler(side, function (response) {
        let statusCode = response["status_code"];
        if (statusCode == null || statusCode == 200) {
            let folderDropDownDiv = document.getElementById(side + '_folder_dropdown_div');
            folderDropDownDiv.innerHTML = response;
            initFolderDropDownComponent();
            setDropdown(side + "_select_folder_btn", folder, folder);
            stopDialog();
        } else {
            if (statusCode != 200 && statusCode != 208) {
                showErrorDialog(response["message"])
            }
        }
    }, function (response) {
        errorResponse(response);
    });
};