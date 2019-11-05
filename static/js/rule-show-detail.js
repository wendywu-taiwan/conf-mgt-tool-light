let compareKey, backupKey, backupFolder, countryId, environmentId, rulesetName;

function initData(compare_key, backup_key, backup_folder, country_id, environment_id, ruleset_name) {
    compareKey = compare_key;
    backupKey = backup_key;
    backupFolder = backup_folder;
    countryId = country_id;
    environmentId = environment_id;
    rulesetName = ruleset_name;
}

function downloadRulesFromServer(url) {
    showWaitingDialog();
    let post_body = {
        "compare_hash_key": compareKey,
        "backup_key": backupKey,
        "backup_folder": backupFolder,
        "ruleset_name": rulesetName,
        "environment_id": environmentId,
        "country_id": countryId
    };

    jQuery.ajax({
        url: url,
        method: 'POST',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data: JSON.stringify(post_body),
        mimeType: 'text/plain; charset=x-user-defined',
        responseType: 'arraybuffer',
    }).then(function success(data) {
        stopDialog();
        downloadZipFile(data,"rulesets");
    })
}