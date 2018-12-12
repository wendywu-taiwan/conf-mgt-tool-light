// Http methods
let contentType = "application/json; charset=utf-8";
let dataType = "json";

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
            type: "POST",
            data: JSON.stringify(req),
            dataType: dataType,
            contentType: contentType,
            success: success_handler,
            error: error_handler
        })
};

const doPUT = function (api_path, req, success_handler, error_handler) {
    jQuery.ajax({
        cache: false,
        url: api_path,
        type: "PUT",
        data: JSON.stringify(req),
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
