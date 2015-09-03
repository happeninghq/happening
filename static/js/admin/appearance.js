$(function() {
    $('input[type="color"]').change($.throttle(1000, function(value) {
        var parameters = [];

        $('input[type="color"]').each(function() {
            var $this = $(this);
            parameters.push($this.attr('name') + "=" + $this.val().substr(1));
        });

        parameters = parameters.join('&');

        $('body').append('<link rel="stylesheet" href="/admin/appearance/css?' + parameters + '" type="text/css"></link>')
    }));
});