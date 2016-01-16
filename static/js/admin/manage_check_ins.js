$(function() {
    $('.btn.check-in').click(function() {
        var $this = $(this);
        $.getJSON($(this).attr('href'), function(r) {
            if ($this.text() == "Check In") {
                $this.attr('href', $this.data('cancel-check-in-url'));
                $this.text('Cancel Check In');
            } else {
                $this.attr('href', $this.data('check-in-url'));
                $this.text('Check In');
            }

            $this.closest('tr').find('.checked-in').html(r['checked-in']);

            $('#attendees-list').data('refresh-datatable')();
        });
        return false;
    });
});