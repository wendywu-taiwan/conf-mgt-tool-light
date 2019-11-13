// Http methods
let contentType = "application/json; charset=utf-8";
let dataType = "json";
let csrftoken;


function setToken(token) {
    csrftoken = token;
}

const doGET = function (api_path, success_handler, error_handler) {
    jQuery.ajax({
        cache: false,
        url: api_path,
        type: "GET",
        success: success_handler,
        error: error_handler
    })
};

const doPOST = function (api_path, req, success_handler, error_handler) {
    jQuery.ajax(
        {
            cache: false,
            url: api_path,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            type: "POST",
            data: JSON.stringify(req),
            contentType: contentType,
            success: success_handler,
            error: error_handler
        })
};

const doPUT = function (api_path, req, success_handler, error_handler) {
    let json_req = JSON.stringify(req);
    json_req['csrfmiddlewaretoken'] = csrftoken;
    jQuery.ajax({
        cache: false,
        url: api_path,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        type: "PUT",
        data: json_req,
        dataType: dataType,
        contentType: contentType,
        success: success_handler,
        error: error_handler
    })
};

const doDELETE = function (api_path, success_handler, error_handler) {
    jQuery.ajax({
        cache: false,
        url: api_path,
        type: "DELETE",
        success: success_handler,
        error: error_handler
    })
};
