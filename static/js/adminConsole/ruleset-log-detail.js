let getRulesetUrl, downloadRulesetUrl, diffServerUrl, diffOtherVersionUrl, applyUrl;
let rulesetName, backupKey;
let backupFolder;

initData = function (name, key) {
    rulesetName = name;
    backupKey = key;
};

initUrl = function (getRuleset, download, diffServer, diffOther, apply) {
    getRulesetUrl = getRuleset;
    downloadRulesetUrl = download;
    diffServerUrl = diffServer;
    diffOtherVersionUrl = diffOther;
    applyUrl = apply;
};


getRuleset = function (environment_version) {
    backupFolder = environment_version;
    let post_body = {
        "ruleset_name": rulesetName,
        "backup_key": backupKey,
        "environment_version": environment_version
    };

    doPOST(getRulesetUrl, post_body, function (response) {
        let rsDetailDiv = document.getElementById('ruleset_detail_div');
        let rsContentDiv = document.getElementById('ruleset_content_div');
        rsContentDiv.innerHTML = response;
        rsDetailDiv.style.display = "block";
    }, function (response) {
        showErrorDialog(response);
    });
};

rulesetDetailBackupPage = function (url) {
    doGET(url, function () {
        window.open(url);
    }, function (response) {
        showErrorDialog(response);
    });
}