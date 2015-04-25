$ ->
    $('.searchable').each ->
        $this = $(this)
        input = $($this.data('search-input'))

        filter = () ->
            query = input.val().toLowerCase()
            if (query == "")
                # Show everything
                $this.find('tr').show()
            else
                $this.find('tr').hide().each ->
                    $tr = $(this)
                    if (!$tr.data('searchable')) || ($tr.data('searchable').toLowerCase().match(".*" + query + ".*"))
                        $tr.show()

        input.keyup filter
        filter()