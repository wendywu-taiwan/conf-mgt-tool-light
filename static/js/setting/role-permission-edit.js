let listUrl = "", updateRolePermissionUrl = "";

function init(update_role_permission_url, list_url) {
    updateRolePermissionUrl = update_role_permission_url;
    listUrl = list_url;
}


function getFunctionPermissionData() {
    console.log("getFunctionPermissionData");
    let functionPermissionArray = [];
    let functionDict = {};
    let permissionArray = [];
    let lastFunctionId = null;
    $('.visible_checkbox').each(function () {
        let dict = {};
        let id = this.id;
        let functionId = split_str(id, 2);
        let roleTypeId = split_str(id, 3);
        let editableCheckbox = document.getElementById("editable_checkbox_" + functionId + "_" + roleTypeId);
        let visible = this.checked;
        let editable = editableCheckbox.checked;

        if (lastFunctionId == null) {
            lastFunctionId = functionId;
        }

        if (lastFunctionId != functionId) {
            functionDict["function_id"] = lastFunctionId;
            functionDict["permissions"] = permissionArray;
            functionPermissionArray.push(functionDict);
            functionDict = {};
            permissionArray = [];
            lastFunctionId = functionId;
            console.log("functionPermissionArray:"+JSON.stringify(functionPermissionArray));
        }


        dict["role_type_id"] = roleTypeId;
        dict["visible"] = visible ? 1 : 0;
        dict["editable"] = editable ? 1 : 0;
        console.log("dict:"+JSON.stringify(dict));

        permissionArray.push(dict);
    });
    return functionPermissionArray;
}

updateRolePermission = function (environmentId) {

    showWaitingDialog();

    let post_body = {
        "environment_id": environmentId,
        "function_permissions": getFunctionPermissionData()
    };

    doPOST(updateRolePermissionUrl, post_body, function (response) {
            console.log("response:" + JSON.stringify(response));
            let statusCode = response["status_code"];
            let message = response["message"];

            if (response == null || statusCode != 200) {
                showErrorDialog(message);
            } else {
                successDialog("update user role success", function () {
                    console.log(response);
                    window.location = listUrl;
                });
            }
        }, function (response) {
            console.log(response);
            showErrorDialog("update user role fail")
        }
    )
    ;
};