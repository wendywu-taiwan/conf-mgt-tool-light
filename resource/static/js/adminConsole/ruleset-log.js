$(function () {
    $('.btn').on('click', function () {
        $('.btn').removeClass('selected');
        $(this).addClass('selected');
    });

    $('#filter_tags_input').on('itemAdded', function (event) {
        filterKeys = $("#filter_tags_input").tagsinput('items');
        filterLogList();
    });

    $('#filter_tags_input').on('itemRemoved', function (event) {
        filterKeys = $("#filter_tags_input").tagsinput('items');
        filterLogList();
    });

});

let filterUrl = "";
let pageChangeUrl = "";
let orderDescend = "descend";
let orderAscend = "ascend";
let filterUserIds = [];
let filterEnvironmentIds = [];
let filterCountryIds = [];
let filterKeys = [];
let order = orderDescend;
let page = 1;
let limit = 10;

initFilterUrl = function (filter, page) {
    filterUrl = filter;
    pageChangeUrl = page;
};

changePage = function (newPage) {
    page = newPage;
    pageChangeLogList();
};

addFilterUserId = function (id) {
    if (!filterUserIds.includes(id))
        filterUserIds.push(id);
};

removeFilterUserId = function (id) {
    if (filterUserIds.includes(id))
        filterUserIds = arrayRemove(filterUserIds, id);
};

addFilterEnvironmentsId = function (id) {
    if (!filterEnvironmentIds.includes(id))
        filterEnvironmentIds.push(id);
};

removeFilterEnvironmentsId = function (id) {
    if (filterEnvironmentIds.includes(id))
        filterEnvironmentIds = arrayRemove(filterEnvironmentIds, id);
};

addFilterCountriesId = function (id) {
    if (!filterCountryIds.includes(id))
        filterCountryIds.push(id);
};

removeFilterCountriesId = function (id) {
    if (filterCountryIds.includes(id))
        filterCountryIds = arrayRemove(filterCountryIds, id);
};

setOrder = function (orderStr) {
    order = orderStr;
    filterLogList();
};

filterLogList = function () {
    refreshLogList(filterUrl);
};

pageChangeLogList = function () {
    refreshLogList(pageChangeUrl);
};

refreshLogList = function (url) {
    let post_body = {
        "filter_user_ids": filterUserIds,
        "filter_environment_ids": filterEnvironmentIds,
        "filter_countries_ids": filterCountryIds,
        "filter_keys": filterKeys,
        "order": order,
        "page": page,
        "limit": limit
    };

    doPOST(url, post_body, function (response) {
        let rsLogListDiv = document.getElementById('ruleset_log_list_div');
        rsLogListDiv.innerHTML = response;
    }, function (response) {
        showErrorDialog(response);
    });
};

directToDetail = function (detailUrl) {
    window.open(detailUrl);
};