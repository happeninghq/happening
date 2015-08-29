$(function() {
    $('.image-widget').each(function() {
        $this = $(this);
        $this.data('initial-src', $this.find('.image-widget__image').attr("src"));
        $this.data('initial-file-name', $this.find('.image-widget__file-name').text());
        $this.data('initial-file-size', $this.find('.image-widget__file-size').text());
        $this.data('initial-dimensions', $this.find('.image-widget__dimensions').text());
        $this.data('initial-value', $this.find('input[type="hidden"]').val());

        $this.find('[type="file"]').fileupload({
            dataType: 'json',
            done: function(e, data) {
                $this.find('.image-widget__image').attr("src", data.result.src)
                $this.find('.image-widget__file-size').text(data.result.filesize)
                $this.find('.image-widget__file-name').text(data.result.filename)
                $this.find('.image-widget__dimensions').text(data.result.dimensions)
                $this.find('input[type="hidden"]').val(data.result.value)
            }
        });
            // # progressall: (e, data) ->
            // #     progress = parseInt(data.loaded / data.total * 100, 10)
            // #     progress_meter.css 'width', progress + '%'
            // # add: (e, data) ->
            // #     progress_meter.css 'width', '0%'
            // #     progress.show
            // #     # $this.find('.file-name').text('')
            // #     # $this.find('.file-size').text('')
            // #     # $this.find('.dimensions').text('')
            // #     data.submit();
            // # done: (e, data) ->
            // #     console.log "DONE"
            // #     progress.hide

        $this.find('.image-widget__reset').click(function() {
            $this.find('.image-widget__image').attr('src', $this.data('initial-src'));
            $this.find('.image-widget__file-name').text($this.data('initial-file-name'));
            $this.find('.image-widget__file-size').text($this.data('initial-file-size'));
            $this.find('.image-widget__dimensions').text($this.data('initial-dimensions'));
            $this.find('input[type="hidden"]').val($this.data('initial-value'));
            return false;
        });

        $this.find('.image-widget__clear').click(function() {
            $this.find('.image-widget__image').attr('src', $this.data('no-image-src'));
            $this.find('.image-widget__file-name').text('');
            $this.find('.image-widget__file-size').text('');
            $this.find('.image-widget__dimensions').text('');
            $this.find('input[type="hidden"]').val('');
            return false;
        });
    });
});