$ ->
  stripeResponseHandler = (status, response) ->
    $form = $('#stripe-form')
    if response.error
      $form.find('.payment-errors').text(response.error.message)
      $form.find('button').prop('disabled', false)
    else
      token = response.id
      $('#id_stripe_token').val(token)
      $('#payment-form').submit()

  $('#stripe-form').submit (event) ->
    $form = $(this)

    $form.find('button').prop('disabled', true)

    Stripe.card.createToken($form, stripeResponseHandler)

    false