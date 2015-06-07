$('.image-widget').each () ->
    $this = $(this)
    $this.data('initial-src', $this.find('img').attr("src"))
    $this.data('initial-file-name', $this.find('.file-name').text())
    $this.data('initial-file-size', $this.find('.file-size').text())
    $this.data('initial-dimensions', $this.find('.dimensions').text())
    $this.data('initial-value', $this.find('input[type="hidden"]').val())

    progress = $(this).find('.progress')
    progress_meter = $(this).find('.progress .meter')

    $this.find('[type="file"]').fileupload
        dataType: 'json',
        done: (e, data) ->
            $this.find('img').attr("src", data.result.src)
            $this.find('.file-size').text(data.result.filesize)
            $this.find('.file-name').text(data.result.filename)
            $this.find('.dimensions').text(data.result.dimensions)
            $this.find('input[type="hidden"]').val(data.result.value)
        # progressall: (e, data) ->
        #     progress = parseInt(data.loaded / data.total * 100, 10)
        #     progress_meter.css 'width', progress + '%'
        # add: (e, data) ->
        #     progress_meter.css 'width', '0%'
        #     progress.show
        #     # $this.find('.file-name').text('')
        #     # $this.find('.file-size').text('')
        #     # $this.find('.dimensions').text('')
        #     data.submit();
        # done: (e, data) ->
        #     console.log "DONE"
        #     progress.hide

    $this.find('.reset').click () ->
        $this.find('img').attr('src', $this.data('initial-src'))
        $this.find('.file-name').text($this.data('initial-file-name'))
        $this.find('.file-size').text($this.data('initial-file-size'))
        $this.find('.dimensions').text($this.data('initial-dimensions'))
        $this.find('input[type="hidden"]').val($this.data('initial-value'))
        false

    $this.find('.clear').click () ->
        $this.find('img').attr('src', $this.data('no-image-src'))
        $this.find('.file-name').text('')
        $this.find('.file-size').text('')
        $this.find('.dimensions').text('')
        $this.find('input[type="hidden"]').val('')
        false
