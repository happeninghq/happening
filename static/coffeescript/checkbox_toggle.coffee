$ ->
  $('.checkbox_toggle').change ->
    $this = $(this)
    if $this.is(':checked')
      $($this.data('toggle')).show()
    else
      $($this.data('toggle')).hide()


  $('.checkbox_toggle').change()