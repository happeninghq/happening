$ ->
  $('.event_preset').click ->
    $('form')[0].reset()
    preset = $(this).data('preset')
    for k, v of preset
      if Array.isArray(v)
        v = JSON.stringify(v)
      $('[name="' + k + '"]').val(v)

    $('.properties-widget').each ->
      $(this).data('reload-properties')()
    false