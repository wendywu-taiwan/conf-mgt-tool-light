function clearTagsInput(id) {
    $("#" + id).tagsinput('removeAll');
}

function getValueTagsInput(id) {
    return $("#" + id).tagsinput('items');
}

function addValueTagsInput(id, tag) {
    $("#" + id).tagsinput('add', tag);

}