$(function() {
    // Address widgets will reload properly
    // but there is no hidden input - so instead we add a data-val method
    $('.address-widget').each(function() {
        var $this = $(this);

        $this.data('val', function(v) {
            for (var k in v) {
                $this.find('[name="' + $this.data('name') + '_' + k +'"]').val(v[k]);
            }
        });
    });
});