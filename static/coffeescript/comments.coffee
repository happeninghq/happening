$ ->
  $('.comment-form').each ->
    $this = $(this)
    $this.find('.show-button').click ->
      $this.find('.show-button').hide()
      $this.find('form').show()
      setup_markdown_editor($this.find('textarea'))