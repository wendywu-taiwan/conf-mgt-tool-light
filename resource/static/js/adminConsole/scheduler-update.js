$(function () {
    $(".tagsinput").tagsinput();

    $("#base_env_select_list li").click(function () {
        $("#select_base_env_btn:first-child").text($(this).text());
        $("#select_base_env_btn:first-child").val($(this).val());
    });

    $("#compare_env_select_list li").click(function () {
        $("#select_compare_env_btn:first-child").text($(this).text());
        $("#select_compare_env_btn:first-child").val($(this).val());
    });

});

function setDisplayName(name) {
    $("#display_name_input").val(name);
    $("#display_name_input").text(name);
}

function setBaseEnvSelected(id, name) {
    $("#select_base_env_btn:first-child").text(name);
    $("#select_base_env_btn:first-child").val(id);
};

function setCompareEnvSelected(id, name) {
    $("#select_compare_env_btn:first-child").text(name);
    $("#select_compare_env_btn:first-child").val(id);
};

function setCountryChecked(country_id) {
    countryCheckboxOnClick(country_id);
    $("#checkbox_input_" + country_id).prop("checked", true);
};

function setMailContentTypeChecked(mail_content_type_id) {
    mailContentTypeCheckboxOnClick(mail_content_type_id);
    $("#mail_content_type_checkbox_input_" + mail_content_type_id).prop("checked", true);
};

function addTagToSkipRulesetInput(countryId, ruleset) {
    addValueTagsInput(countryId + "_skip_ruleset_list_input", ruleset);
}

let receivers = [];

function addReceivers(receiver) {
    receivers.push(receiver)
}

function setReceivers() {
    for (var i = 0; i < receivers.length; i++) {
        var receiver = receivers[i];
        $('#mail_receiver_input').tagsinput('add', "");
        $('#mail_receiver_input').tagsinput('add', receiver);
    }
}