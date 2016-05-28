/* global Stripe:false */
import $ from 'jquery';

// Stripe will be included in the page
// this is because they often update the code

export const init = () => {
  $('.stripe-form').each(function initStripe() {
    const $form = $(this);
    $form.submit(() => {
      $form.find('button').prop('disabled', true);
      Stripe.card.createToken($form, (status, response) => {
        if (response.error) {
          $form.find('.payment-errors').text(response.error.message);
          $form.find('button').prop('disabled', false);
        } else {
          const $paymentForm = $($form.data('payment-form'));
          const token = response.id;
          $paymentForm.find('#id_stripe_token').val(token);
          $paymentForm.submit();
        }
      });
      return false;
    });
  });
};
