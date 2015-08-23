$(function() {
    $('.datetime-widget').each(function() {
        var $this = $(this);
        $this.datetimepicker({"format": $this.data('datetime-format')});
    });
});