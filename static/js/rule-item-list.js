rulesetDetailPage = function (url) {
    doGET(url, function () {
        window.open(url)
    }, function (response) {
        showErrorDialog(response);
    });
};