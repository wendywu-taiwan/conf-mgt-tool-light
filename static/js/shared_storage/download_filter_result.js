function filteredFilesSelectAll() {
    let inputs = document.getElementsByClassName('filter_result_file_checkbox');
    let selectAllButtonText = $('#filter_result_select_all_btn').text();
    let inputCounts = inputs.length;
    let i, input, inputId, checkedStatus;

    if (selectAllButtonText == "Deselect All") {
        checkedStatus = false;
        changeFilterResultDownloadBtnVisibility(false, 0);
        $('#filter_result_select_all_btn').text("Select All");
    } else {
        checkedStatus = true;
        changeFilterResultDownloadBtnVisibility(true, inputCounts);
        $('#filter_result_select_all_btn').text("Deselect All");
    }

    for (i = 0; i < inputCounts; i++) {
        input = inputs[i];
        input.checked = checkedStatus;
        inputId = input.id;
    }
}

function onClickCheckbox(inputItem, filePath) {
    if (inputItem.checked) {
        selectFilePathArray.push(filePath);
    } else {
        selectFilePathArray = arrayRemove(selectFilePathArray, filePath);
    }
    checkFilterResultDownloadBtnVisibility();
    checkFilterResultSelectAllBtnStatus();
}


function checkFilterResultDownloadBtnVisibility() {
    let checkCount = $('.filter_result_file_checkbox').filter(':checked').length;
    if (checkCount == 0) {
        changeFilterResultDownloadBtnVisibility(false, 0);
    } else {
        changeFilterResultDownloadBtnVisibility(true, checkCount);
    }
}

function checkFilterResultSelectAllBtnStatus() {
    let inputCount = $('.filter_result_file_checkbox').length;
    let checkedCount = $('.filter_result_file_checkbox').filter(':checked').length;
    if (checkedCount == 0) {
        $('#filter_result_select_all_btn').text("Select All");
    } else if (checkedCount == inputCount) {
        $('#filter_result_select_all_btn').text("Deselect All");
    }
}

function changeFilterResultDownloadBtnVisibility(visible, checkCount) {
    console.log("changeFilterResultDownloadBtnVisibility, visible:" + visible + ", checkCount:" + checkCount);
    let downloadBtnDiv = document.getElementById('filter_result_download_selected_btn_div');
    let downloadBtn = document.getElementById('filter_result_download_selected_btn');
    if (visible) {
        downloadBtnDiv.style.display = 'block';
        downloadBtn.innerText = "Download(" + checkCount + ")";
    } else {
        downloadBtnDiv.style.display = 'none';
    }
}

function downloadFilterFiles() {
    showWaitingDialog();
    let inputs = $('.filter_result_file_checkbox').filter(':checked');
    downloadFiles(inputs);
}