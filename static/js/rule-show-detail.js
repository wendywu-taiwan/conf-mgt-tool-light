let compareKey, countryId, environmentId, rulesetName;

function setData(compare_key, country_id, environment_id, ruleset_name) {
    compareKey = compare_key;
    countryId = country_id;
    environmentId = environment_id;
    rulesetName = ruleset_name;
}

function downloadRulesFromServer(url) {
    showWaitingDialog();

    let post_body = {
        "compare_hash_key": compareKey,
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
        downloadZipFile(data);
    })
}