$ ->
  check_id_amount = () ->
    if $('#id_amount').val() == "other"
      $('#other_amount').show()
    else
      $('#other_amount').hide()

  $('#id_amount').change(check_id_amount)
  check_id_amount()