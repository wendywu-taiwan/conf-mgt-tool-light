let getRulesetUrl, downloadRulesetUrl, applyUrl;
let rulesetName, backupKey, backupFolder, sourceEnvId, targetEnvId, countryId;
let EnvTypeSource = "source";
let EnvTypeTarget = "target";

initData = function (name, key, source_env_id, target_env_id, country_id) {
    rulesetName = name;
    backupKey = key;
    sourceEnvId = source_env_id;
    targetEnvId = target_env_id;
    countryId = country_id;
};

initUrl = function (getRuleset, download, apply) {
    getRulesetUrl = getRuleset;
    downloadRulesetUrl = download;
    applyUrl = apply;
};


getRuleset = function (environment_version) {
    showDialog("Loading...");
    backupFolder = environment_version;
    let post_body = {
        "ruleset_name": rulesetName,
        "backup_key": backupKey,
        "environment_version": environment_version
    };

    doPOST(getRulesetUrl, post_body, function (response) {
        let hideDetailDiv;
        let rsDetailDiv = document.getElementById('ruleset_detail_div_' + environment_version);
        let rsContentDiv = document.getElementById('ruleset_content_div_' + environment_version);

        if (environment_version == EnvTypeSource)
            hideDetailDiv = document.getElementById('ruleset_detail_div_' + EnvTypeTarget);
        else
            hideDetailDiv = document.getElementById('ruleset_detail_div_' + EnvTypeSource);

        rsContentDiv.innerHTML = response;
        rsDetailDiv.style.display = "block";
        hideDetailDiv.style.display = "none";
        stopDialog();
    }, function (response) {
        showErrorDialog(response);
    });
};

function downloadRuleset() {
    showWaitingDialog();
    let postEnvId;
    if (backupFolder == "source") {
        postEnvId = sourceEnvId;
    } else {
        postEnvId = targetEnvId;
    }

    let post_body = {
        "backup_key": backupKey,
        "backup_folder": backupFolder,
        "ruleset_name": rulesetName,
        "environment_id": postEnvId,
        "country_id": countryId
    };

    jQuery.ajax({
        url: downloadRulesetUrl,
        method: 'POST',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data: JSON.stringify(post_body),
        mimeType: 'text/plain; charset=x-user-defined',
        responseType: 'arraybuffer',
    }).then(function success(data) {
        stopDialog();
        downloadZipFile(data, "rulesets");
    })
}


function applyToServer() {
    showWaitingDialog();

    let post_body = {
        "backup_key": backupKey,
        "backup_folder": backupFolder,
        "ruleset_name": rulesetName,
        "environment_id": targetEnvId,
        "country_id": countryId
    };

    doPOST(applyUrl, post_body, function (response) {
            let statusCode = response["status_code"];
            let message = response["message"];

            if (response == null || statusCode != 200) {
                showErrorDialog(message);
                return;
            }

            successDialog("Apply to server Success");
        }, function (response) {
            console.log("response:" + String(response));
            showErrorDialog("Apply to server Fail")
        }
    );
}

openNewPage = function (url) {
    showWaitingDialog();
    doGET(url, function (response) {
        let statusCode = response["status_code"];
        if (statusCode == null) {
            stopDialog();
            window.open(url);
        } else {
            showErrorDialog(response["message"])
        }
    }, function (response) {
        showErrorDialog(response);
    });
};

openDiffResultPage = function (url) {
    showWaitingDialog();
    doGET(url, function (response) {
        let statusCode = response["status_code"];
        if (statusCode == null) {
            stopDialog();
            window.open(url);
        } else {
            if (statusCode == 233)
                showSuccessDialog("Ruleset is no difference.");
            else
                showErrorDialog(response["message"])
        }
    }, function (response) {
        showErrorDialog(response);
    });
};