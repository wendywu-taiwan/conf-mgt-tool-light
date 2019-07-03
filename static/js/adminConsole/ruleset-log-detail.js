let getRulesetUrl, prettyUrl, downloadRulesetUrl, diffServerUrl, diffOtherVersionUrl, applyUrl;
let rulesetName, backupKey;

initData = function (name, key) {
    rulesetName = name;
    backupKey = key;
};

initUrl = function (getRuleset, pretty, download, diffServer, diffOther, apply) {
    console.log("initUrl,getRuleset :"+getRuleset);
    getRulesetUrl = getRuleset;
    prettyUrl = pretty;
    downloadRulesetUrl = download;
    diffServerUrl = diffServer;
    diffOtherVersionUrl = diffOther;
    applyUrl = apply;
};


getRuleset = function (environment_version) {
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