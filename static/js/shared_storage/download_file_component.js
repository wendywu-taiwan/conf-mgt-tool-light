let downloadUrl;

function initDownloadUrl(url) {
    downloadUrl = url;
}

function downloadFiles(regionId, environmentId, root_hash_key, file_path) {
    showWaitingDialog();
    let post_body = {
        "region_id": regionId,
        "environment_id": environmentId,
        "root_hash_key": root_hash_key,
        "file_path": file_path,
    };

    jQuery.ajax({
        url: downloadUrl,
        method: 'POST',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data: JSON.stringify(post_body),
        mimeType: 'text/plain; charset=x-user-defined',
        responseType: 'arraybuffer',
    }).then(function success(data) {
        stopDialog();
        downloadZipFile(data, "files");
    })
}