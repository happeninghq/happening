$(function() {
    $('.date-widget').each(function() {
        var $this = $(this);
        $this.datetimepicker({"timepicker": false, "format": $this.data('date-format')});
    });
});