$(function() {
    var csrftoken = Cookies.get('csrftoken');
    $('body').on('click', '.confirm', function() {
        if (confirm($(this).data('confirm'))) {
            if ($(this).attr('href')) {
                $('<form action=' + $(this).attr('href') + ' method="POST"><input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '"></form>').submit();
                return false;
            } else {
                // For forms etc.
                return true;
            }
        } else {
            return false;
        }
    });
});