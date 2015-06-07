$ ->
    $('.load-ajax-into-input').click () ->
        $this = $(this)
        $.getJSON $this.data('ajax-url'), (data) ->
            $("#" + $this.data('input-id')).val(data.value)
        false

    csrftoken = $.cookie('csrftoken');
    csrfSafeMethod = (method) ->
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))

    $.ajaxSetup
        beforeSend: (xhr, settings) ->
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) 
                xhr.setRequestHeader("X-CSRFToken", csrftoken)