let gitPathIds = [];
let editPathUrl;

function onClickButton(item) {
    if (item.text == "Edit") {
        onClickEdit(item);
    } else {
        onClickSave(item);
    }
}

function onClickEdit(item) {
    let index, id;
    for (index in gitPathIds) {
        id = gitPathIds[index];
        dataDisplayMode(id, showBlock, hide);
    }
    item.text = "Save";
}

function onClickSave(item) {
    showWaitingDialog();
    checkInputValid();

    doPOST(editPathUrl, getUpdatePathJson(), function (response) {
        let statusCode = response["status_code"];

        if (response == null || statusCode != 200) {
            showErrorDialog("update path fail");
        } else {
            updateContentDivAndShow();
            successDialog("update path success", function () {
                console.log(response);
            });
            item.text = "Edit";
        }
    }, function (response) {
        console.log(response);
        showErrorDialog("update path fail");
    });
}

function checkInputValid() {
    let index, id;
    for (index in gitPathIds) {
        id = gitPathIds[index];
        if (getRepoInputValue(id) == "" && getRepoInputPlaceHolder(id) == "") {
            showWarningDialog("please make sure each repo path is not empty");
        }

        if (getFolderInputValue(id) == "" && getFolderInputPlaceHolder(id) == "") {
            showWarningDialog("please make sure each folder path is not empty");
        }
    }
}

function updateContentDivAndShow() {
    let index, id;
    for (index in gitPathIds) {
        id = gitPathIds[index];
        let repoContentDiv, folderContentDiv;
        repoContentDiv = document.getElementById(id + "_repo_path_content_div");
        folderContentDiv = document.getElementById(id + "_folder_content_div");
        repoContentDiv.innerHTML = getRepoInputValue(id);
        folderContentDiv.innerHTML = getFolderInputValue(id);
        dataDisplayMode(id, hide, showBlock);
    }
}

function getUpdatePathJson() {
    let pathList = [];
    let id, index, repoPath, folder;
    for (index in gitPathIds) {
        id = gitPathIds[index];
        repoPath = getRepoInputValue(id) == "" ? getRepoInputPlaceHolder(id) : getRepoInputValue(id);
        folder = getFolderInputValue(id) == "" ? getFolderInputPlaceHolder(id) : getFolderInputValue(id);

        let pathObj = {
            "id": id,
            "repo_path": repoPath,
            "folder": folder
        };
        pathList.push(pathObj);
    }

    return pathList;
}

function getRepoInputValue(id) {
    let input = document.getElementById(id + "_repo_path_input");
    return input.value;
}

function getRepoInputPlaceHolder(id) {
    let input = document.getElementById(id + "_repo_path_input");
    return input.placeholder;
}

function getFolderInputValue(id) {
    let input = document.getElementById(id + "_folder_input");
    return input.value;
}

function getFolderInputPlaceHolder(id) {
    let input = document.getElementById(id + "_folder_input");
    return input.placeholder;
}


function dataDisplayMode(id, inputDivDisplayFunc, contentDivDisplayFunc) {
    let repoInputDiv, folderInputDiv, repoContentDiv, folderContentDiv;
    repoInputDiv = document.getElementById(id + "_repo_path_input_div");
    folderInputDiv = document.getElementById(id + "_folder_input_div");
    repoContentDiv = document.getElementById(id + "_repo_path_content_div");
    folderContentDiv = document.getElementById(id + "_folder_content_div");

    inputDivDisplayFunc(repoInputDiv);
    inputDivDisplayFunc(folderInputDiv);
    contentDivDisplayFunc(repoContentDiv);
    contentDivDisplayFunc(folderContentDiv);
}