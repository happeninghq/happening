"""Payment decorators."""
from payments.models import Payment
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.core.urlresolvers import resolve


def payment_decorator(status):
    """Ensure that the method is only called once for a payment.

    Also ensure that it is only called on payments which have
    been attempted, and only called for the correct user.

    This will only mark a payment as "complete" if the return value
    has a status of 200, 201, or 302.

    If you status does not match these - you should update the payment
    manually by setting "complete" to True and saving.
    """
    def inner_1(func):
        def inner(request, pk):
            payment = get_object_or_404(Payment, pk=pk)
            if not payment.user == request.user:
                return HttpResponseForbidden()
            if payment.complete:
                return HttpResponseForbidden()
            if not payment.status == status:
                return HttpResponseForbidden()
            current_url = resolve(request.path_info).url_name
            if current_url not in [payment.success_url_name,
                                   payment.failure_url_name]:
                return HttpResponseForbidden()
            response = func(request, payment)
            if response.status_code in [200, 201, 302]:
                payment.complete = True
                payment.save()
            return response
        return inner
    return inner_1


payment_successful = payment_decorator("PAID")
payment_failed = payment_decorator("FAILED")
