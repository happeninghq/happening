Payment
==============

Some functionality in Happening will require/allow payment from members. Currently this is only the :ref:`membership` plugin but in future will include ticket purchases, etc.

The payment details is abstracted away so that Happening functionality which requires payment can make a request and be informed that payment has been received. There is no need for more involved interaction with payments.

To take a payment, first create a Payment object, and redirect to make_payment::

    from payments.models import Payment

    payment = Payment(
        user=request.user,
        description="Membership",
        amount=1000,
        extra={"member": member.pk},
        success_url_name="membership_payment_success",
        failure_url_name="membership_payment_failure"
    )
    payment.save()
    return redirect("make_payment", payment.pk)

The description will be shown on the member's bank statement. The amount is in pennies. Extra can take any information you want to refer back to later. It will be shown in the payment log and will be available in your success/failure callbacks.

The success_url_name and failure_url_name configure the view which will be redirected to once payment is complete. These should be decorated with the ``payment_successful`` and ``payment_failed`` decorators.


An example of callbacks are::
    
    @login_required
    @payment_successful
    def membership_payment_success(request, payment):
        """Membership payment successful."""
        member = get_object_or_404(get_user_model(), pk=payment.extra["member"])

        # Do something with the member since they've paid

        messages.success(request, "Your payment has been made " +
                                  "successfully. Thank you very much!")

        n = MembershipPaymentSuccessfulNotification(
            request.user, amount=payment.amount / 100)
        n.send()

        return redirect("membership", member.pk)

    @login_required
    @payment_failed
    def membership_payment_failure(request, payment):
        """Membership payment failed."""
        messages.error(request, payment.error)
        return redirect("membership", payment.extra["member"])
