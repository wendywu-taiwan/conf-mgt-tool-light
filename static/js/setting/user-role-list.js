openEditUserRolePage = function (url) {
    showWaitingDialog();

    doGET(url, function (response) {
        let statusCode = response["status_code"];
        if (statusCode == null) {
            stopDialog();
            window.open(url);
        } else {
            if (statusCode == 500)
                showErrorDialog(response["message"])
        }
    }, function (response) {
        showErrorDialog(response);
    });
};