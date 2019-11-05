$(function () {
    $('.collapse').on('hidden.bs.collapse', function (e) {
        triggerOppositeComponent(e, "hide");
        changeCollapseIconVisibility(e, hide, showBlock);
    });

    $('.collapse').on('shown.bs.collapse', function (e) {
        triggerOppositeComponent(e, "show");
        changeCollapseIconVisibility(e, showBlock, hide);
    });

    let leftSideResultDiv = document.getElementById("left_folder_structure_div");
    let rightSideResultDiv = document.getElementById("right_folder_structure_div");

    leftSideResultDiv.addEventListener('scroll', function () {
        rightSideResultDiv.scrollTop = leftSideResultDiv.scrollTop;
    });

    rightSideResultDiv.addEventListener('scroll', function () {
        leftSideResultDiv.scrollTop = rightSideResultDiv.scrollTop;
    });
});

function showCollapseComponent(side, depth, index, node_hash_key) {
    let collapseShowIcon = getCollapseShowIcon(side, depth, index, node_hash_key);
    let collapseHideIcon = getCollapseHideIcon(side, depth, index, node_hash_key);
    let collapseComponent = getCollapseComponent(side, depth, index, node_hash_key);

    showBlock(collapseShowIcon);
    hide(collapseHideIcon);
    collapseComponent.collapse("show");
}

function hideCollapseComponent(side, depth, index, node_hash_key) {
    let collapseShowIcon = getCollapseShowIcon(side, depth, index, node_hash_key);
    let collapseHideIcon = getCollapseHideIcon(side, depth, index, node_hash_key);
    let collapseComponent = getCollapseComponent(side, depth, index, node_hash_key);

    showBlock(collapseHideIcon);
    hide(collapseShowIcon);
    collapseComponent.collapse("hide");

}

function getCollapseShowIcon(side, depth, index, node_hash_key) {
    return getCollapseIcon(side, depth, index, node_hash_key, "collapse_show")
}

function getCollapseHideIcon(side, depth, index, node_hash_key) {
    return getCollapseIcon(side, depth, index, node_hash_key, "collapse_hide")
}

function getCollapseComponent(side, depth, index, node_hash_key) {
    let collapseComponentId = side + "_folder_" + depth + "_" + index + "_" + node_hash_key + "_child_div";
    return $('#' + collapseComponentId + '');
}

function getCollapseIcon(side, depth, index, node_hash_key, idSuffix) {
    let idPrefix = side + "_" + depth + "_" + index + "_" + node_hash_key;
    let componentId = idPrefix + "_" + idSuffix;
    return document.getElementById(componentId);
}


function triggerOppositeComponent(e, status) {
    let idArray = split_str_array(e.currentTarget.id);
    let oppositeId = "";
    let oppositeComponent = null;


    oppositeId = (idArray[0] == "left") ? "right" : "left";
    delete idArray[0];

    idArray.forEach(function (element) {
        oppositeId = oppositeId + "_" + element;
        oppositeComponent = $('#' + oppositeId + '');
    });

    oppositeComponent.collapse(status);
    e.stopPropagation();
}

function changeCollapseIconVisibility(e, showIconSwitchMethod, hideIconSwitchMethod) {
    let collapseChildComponentId = e.currentTarget.id;
    let idArray = split_str_array(collapseChildComponentId);
    let collapseShowIconId = "";
    let collapseHideIconId = "";
    let collapseShowIcon, collapseHideIcon;

    //folder
    delete idArray[1];
    //child
    delete idArray[5];
    //div
    delete idArray[6];

    idArray.forEach(function (element) {
        collapseShowIconId = collapseShowIconId + element + "_";
        collapseHideIconId = collapseHideIconId + element + "_";
    });

    collapseShowIconId = collapseShowIconId + "collapse_show";
    collapseHideIconId = collapseHideIconId + "collapse_hide";

    collapseShowIcon = document.getElementById(collapseShowIconId);
    collapseHideIcon = document.getElementById(collapseHideIconId);

    showIconSwitchMethod(collapseShowIcon);
    hideIconSwitchMethod(collapseHideIcon);
}

let lastClickedRDataLineId;

function dataLineOnclick(element, type, diffResult, detailUrl, diffUrl) {
    // example id: right_-18446744073139484987_data_line_div
    //remove last select item bg color

    if (diffResult == "remove")
        return;

    if (lastClickedRDataLineId != null) {
        let lastElement = document.getElementById(lastClickedRDataLineId);
        let lastOppositeElement = getOppositeElement(lastClickedRDataLineId);
        lastElement.style.backgroundColor = "#ffffff";
        lastOppositeElement.style.backgroundColor = "#ffffff";
    }

    if (type == "folder") {
        return;
    }

    //add bg color to current select item
    lastClickedRDataLineId = element.id;
    element.style.backgroundColor = "#d8ecffbd";
    let oppositeElement = getOppositeElement(element.id);
    oppositeElement.style.backgroundColor = "#d8ecffbd";

    //open file detail or diff page
    if (diffResult == "different") {
        getFileDiffPage(diffUrl);
    } else {
        getFileDetailPage(detailUrl)
    }
}

function getOppositeElement(id) {
    let idArray = split_str_array(id);
    let side = idArray[0];
    let oppositeElementId = (side == "left") ? "right" : "left";

    delete idArray[0];
    idArray.forEach(function (string) {
        oppositeElementId = oppositeElementId + "_" + string;
    });
    return document.getElementById(oppositeElementId);
}

function getFileDetailPage(url) {
    showWaitingDialog();

    doGET(url, function (response) {
        let statusCode = response["status_code"];
        if (statusCode == null) {
            stopDialog();
            window.open(url);
        } else {
            if (statusCode == 234)
                showSuccessDialog("Preview is not supported for this file");
            else
                showErrorDialog(response["message"])
        }
    }, function (response) {
        showErrorDialog(response);
    });

}

function getFileDiffPage(url) {
    showWaitingDialog();

    doGET(url, function (response) {
        let statusCode = response["status_code"];
        if (statusCode == null) {
            stopDialog();
            window.open(url);
        } else {
            if (statusCode == 234)
                showSuccessDialog("Preview is not supported for this file");
            else
                showErrorDialog(response["message"])
        }
    }, function (response) {
        showErrorDialog(response);
    });

}