let userId = "";
let listUrl = "";
let updateUserRoleUrl = "";
let checkedList = [];

$(function () {


});


function init(update_user_role_url, list_url) {
    updateUserRoleUrl = update_user_role_url;
    listUrl = list_url;
}

function getCheckedData() {

    $('.user_role_option input:checked').each(function () {
        let dict = {};
        let id = this.id;

        dict["environment_id"] = split_str(id, 1);
        dict["role_type_id"] = split_str(id, 2);
        checkedList.push(dict);
    });
}

updateUserRole = function (userId) {

    showWaitingDialog();
    getCheckedData();

    let post_body = {
        "user_id": userId,
        "checked_list": checkedList
    };

    doPOST(updateUserRoleUrl, post_body, function (response) {
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
