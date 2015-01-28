$ ->
    $('.load-ajax-into-input').click () ->
        $this = $(this)
        $.getJSON $this.data('ajax-url'), (data) ->
            $("#" + $this.data('input-id')).val(data.value)
        false