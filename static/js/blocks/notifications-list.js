$(function() {

    // Mark as read when clicking overall link
    $('.notifications-list-link').click(function() {
        $.post("/notifications/mark-read");
        $('.notification-button__unread').removeClass('notification-button__unread--unread');

        if ($(this).hasClass('notification-button__unread')) {
            $('.notifications-list-link:first').click();
            return false;
        }
    });

    // Make links work on notifications
    $('.notifications-list__notification').click(function() {
        window.location = $(this).data('url');
        return false;
    });
});