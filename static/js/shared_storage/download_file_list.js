$(function () {
    $('.collapse').on('hide.bs.collapse', function (e) {
        e.preventDefault();
    })
});

function checkButtonStatus() {
    let fileCount = $('.file_checkbox').length;
    let fileCheckedCount = $('.file_checkbox').filter(':checked').length;
    if (fileCheckedCount == 0) {
        $('#file_list_select_all_btn').text("Select All");
        changeDownloadBtnVisibility(false, 0);
    } else if (fileCount == fileCheckedCount) {
        $('#file_list_select_all_btn').text("Deselect All");
        changeDownloadBtnVisibility(true, fileCheckedCount);
    } else {
        changeDownloadBtnVisibility(true, fileCheckedCount);
    }
}

function checkFolderCheckboxStatus() {
    let inputs = document.getElementsByClassName("file_list_file_checkbox");
    let inputCounts = inputs.length;
    let i, input, inputId;

    for (i = 0; i < inputCounts; i++) {
        input = inputs[i];
        inputId = input.id;

        if (input.classList.contains("file_checkbox"))
            continue;

        let childFoldersClassName = getChildFolderClassNameFromCheckboxId(input.id);
        let childFilesClassName = getChildFileClassNameFromCheckboxId(input.id);

        let childFolderCount = $('.' + childFoldersClassName).length;
        let childFileCount = $('.' + childFilesClassName).length;
        let childFolderCheckCount = $('.' + childFoldersClassName).filter(':checked').length;
        let childFileCheckCount = $('.' + childFilesClassName).filter(':checked').length;

        let inputCurrentStatus = input.checked;
        let inputNewStatus;
        if ((childFolderCount + childFileCount) == (childFolderCheckCount + childFileCheckCount)) {
            inputNewStatus = true;
        } else {
            inputNewStatus = false;
        }
        if (inputCurrentStatus != inputNewStatus) {
            input.checked = inputNewStatus;
            checkFolderCheckboxStatus();

        }
    }
}

function checkboxOnClick(item) {
    let checked = item.checked;
    let childFoldersClassName = getChildFolderClassNameFromCheckboxId(item.id);
    let childFilesClassName = getChildFileClassNameFromCheckboxId(item.id);

    checkedLoopChildInputByClassName(childFoldersClassName, checked);
    checkedLoopChildInputByClassName(childFilesClassName, checked);
    checkButtonStatus();
    checkFolderCheckboxStatus();
}

function checkedLoopChildInputByClassName(className, checked) {
    let inputs = document.getElementsByClassName(className);
    let inputCounts = inputs.length;
    let i, input;

    for (i = 0; i < inputCounts; i++) {
        input = inputs[i];
        input.checked = checked;

        let childFoldersClassName = getChildFolderClassNameFromCheckboxId(input.id);
        let childFilesClassName = getChildFileClassNameFromCheckboxId(input.id);

        checkedLoopChildInputByClassName(childFoldersClassName, checked);
        checkedLoopChildInputByClassName(childFilesClassName, checked);
    }
}

function checkedChildInputByClassName(className, checked) {
    let inputs = document.getElementsByClassName(className);
    let inputCounts = inputs.length;
    let i, input, inputId;

    for (i = 0; i < inputCounts; i++) {
        input = inputs[i];
        input.checked = checked;
        inputId = input.id;
    }
}

function fileListSelectAll() {

    let selectAllButton = $('#file_list_select_all_btn');
    let checkCount = $('.file_checkbox').length;
    let checkedStatus;


    if (selectAllButton.text() == "Deselect All") {
        checkedStatus = false;
        changeDownloadBtnVisibility(false, 0);
        selectAllButton.text("Select All");
    } else {
        checkedStatus = true;
        changeDownloadBtnVisibility(true, checkCount);
        selectAllButton.text("Deselect All");
    }
    checkedChildInputByClassName("file_list_file_checkbox", checkedStatus);
}

function changeDownloadBtnVisibility(visible, checkCount) {
    let downloadBtnDiv = document.getElementById('file_list_download_selected_btn_div');
    let downloadBtn = document.getElementById('file_list_download_selected_btn');
    if (visible) {
        downloadBtnDiv.style.display = 'block';
        downloadBtn.innerText = "Download(" + checkCount + ")";
    } else {
        downloadBtnDiv.style.display = 'none';
    }
}

function getChildFolderClassNameFromCheckboxId(id) {
    let compare_hash_key = split_str(id, 0);
    return "child_checkbox_folder_" + compare_hash_key;
}

function getChildFileClassNameFromCheckboxId(id) {
    let compare_hash_key = split_str(id, 0);
    return "child_checkbox_file_" + compare_hash_key;
}

function downloadListFiles() {
    showWaitingDialog();
    let inputs = $('.file_checkbox').filter(':checked');
    downloadFiles(inputs);
}