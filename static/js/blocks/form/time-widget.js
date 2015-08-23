$(function() {
    $('.time-widget').each(function() {
        var $this = $(this);
        $this.datetimepicker({"datepicker": false, "format": $this.data('time-format')});
    });
});