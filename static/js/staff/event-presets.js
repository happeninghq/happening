$(function() {
    $('.event-preset').click(function() {
        $('form')[0].reset();
        var preset = $(this).data('preset');
        for (k in preset) {
            if (preset.hasOwnProperty(k)) {
                var v = preset[k];

                if (Array.isArray(v)) {
                    v = JSON.stringify(v)
                }

                $('[name="' + k + '"]').val(v);

                $('.widget').each(function() {
                    if ($(this).data('reload')) {
                        $(this).data('reload')();
                    }
                });
                false
            }
        }
    })
})