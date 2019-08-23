$(function () {
    $("#frequency_dropdown_ul li").click(function () {
        let selectFrequency = $(this).text();
        setIntervalText(selectFrequency);

        $("#frequency_dropdown_button:first-child").text(selectFrequency);
        $("#frequency_dropdown_button:first-child").val($(this).val());
    });
});

function getFrequencyDropdownVal() {
    return $("#frequency_dropdown_button:first-child").val();
}

function setFrequencyDropdown(id, name) {
    $("#frequency_dropdown_button:first-child").text(name);
    $("#frequency_dropdown_button:first-child").val(id);
    setIntervalText(name);
}

function setIntervalText(selectFrequency) {
    let frequencyText = "";
    if (selectFrequency == "Daily") {
        frequencyText = "Day(s)";
    } else if (selectFrequency == "Weekly") {
        frequencyText = "Week(s)";
    } else {
        frequencyText = "Month(s)";
    }
    $("#frequency_text_div").text(frequencyText);
}

function getInterval() {
    return $("#repeat_input").val();
}

function setInterval(val) {
    $("#repeat_input").val(val);
    $("#repeat_input").text(val);
}