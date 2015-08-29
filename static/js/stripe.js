$(function() {
    $('.stripe-form').each(function() {
        var $form = $(this);
        $form.submit(function(event) {
            $form.find('button').prop('disabled', true)
            Stripe.card.createToken($form, function(status, response) {
                if (response.error) {
                    $form.find('.payment-errors').text(response.error.message);
                    $form.find('button').prop('disabled', false);
                } else {
                    var $payment_form = $($form.data('payment-form'));
                    var token = response.id;
                    $payment_form.find('#id_stripe_token').val(token);
                    $payment_form.submit();
                }
            });
            return false;
        });
    });
});