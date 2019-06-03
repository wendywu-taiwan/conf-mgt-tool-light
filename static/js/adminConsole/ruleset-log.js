$(function () {
    $('.btn').on('click', function () {
        $('.btn').removeClass('selected');
        $(this).addClass('selected');
    });
});