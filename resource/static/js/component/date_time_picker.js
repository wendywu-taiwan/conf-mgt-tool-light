getNextProceedTime = function () {
    let date = getProceedDate();
    let time = getProceedTime();
    return date + " " + time;
};

function setNextProceedTime(start_time) {
    var start_time_date = new Date(start_time);
    var year = start_time_date.getFullYear();
    var month = leadingZero(start_time_date.getMonth() + 1);
    var date = leadingZero(start_time_date.getDate());
    var hours = leadingZero(start_time_date.getHours());
    var minute = leadingZero(start_time_date.getMinutes());
    var nextProceedDate = year + "/" + month + "/" + date;
    var nextProceedTime = hours + ":" + minute;
    setProceedDate(nextProceedDate);
    setProceedTime(nextProceedTime);
}