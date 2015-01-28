$ ->
  $('.vote-form').each () ->
    $this = $(this)
    $this.find('.language-list').sortable(
      connectWith: '.connected'
    )

    $this.find('.add-language').keypress (e) ->
      if(e.which == 13)
        $this.find('.other-languages').append(
          $("<li>" + $('.add-language').val() + "</li>"))
        $this.find('.add-language').val("")
        $this.find('.other-languages').sortable(
          connectWith: '.connected'
        )
        false

    $this.submit () ->
      v = []
      $('.preferences').find("li").each () ->
        v.push($(this).text())
      $('[name="languages"]').val(JSON.stringify(v))