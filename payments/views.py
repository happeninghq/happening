"""Payment views."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Payment, PaymentHandler
from pages.configuration import SiteTitle
from copy import copy
from django.http import HttpResponseForbidden
from .forms import PaymentForm
import stripe


@login_required
def make_payment(request, pk):
    """Accept payment."""
    payment = get_object_or_404(Payment, pk=pk)
    if not payment.user == request.user:
        return HttpResponseForbidden()

    if not payment.status == "PENDING":
        return HttpResponseForbidden()

    handler = PaymentHandler.objects.active()
    if not handler:
        payment.status = "FAILED"
        payment.error = "This website is not configured for payment"
        payment.save()
        return redirect(payment.failure_url_name, payment.pk)

    if request.method == "POST":
        form = PaymentForm(request.POST)

        stripe.api_key = handler.secret_key

        description = "%s: %s" % (SiteTitle().get(), payment.description)
        metadata = copy(payment.metadata)
        metadata["paid_by_id"] = request.user.pk

        if form.is_valid():
            try:
                charge = stripe.Charge.create(
                    # We work in pennies, not pounds
                    amount=payment.amount,
                    currency="gbp",  # TODO: Allow other currencies
                    card=form.cleaned_data['stripe_token'],
                    description=description,
                    metadata=metadata,
                    statement_descriptor=description[:22],
                    receipt_email=request.user.email
                )

                payment.status = "PAID"
                payment.reciept_id = charge.id
                payment.save()
                return redirect(payment.success_url_name, payment.pk)

            except stripe.CardError as e:
                payment.status = "FAILED"
                payment.error = e
                payment.save()
                return redirect(payment.failure_url_name, payment.pk)
    else:
        form = PaymentForm(initial={"amount": payment.amount / 100})

    return render(request, "payments/payment.html",
                  {"amount": payment.amount / 100,
                   "stripe_key": handler.public_key,
                   "payment_form": form,
                   "payment": payment
                   }
                  )
