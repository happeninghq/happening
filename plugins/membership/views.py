"""Membership views."""
from django.http import HttpResponseForbidden
from payments.decorators import payment_successful, payment_failed
from payments.models import Payment
from forms import PaymentForm
from django.contrib import messages
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from models import Membership
from notifications import MembershipPaymentSuccessfulNotification
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from members.decorators import require_editing_own_profile
from django.contrib.auth import get_user_model


@login_required
def my_membership(request):
    """Redirect to our own membership page."""
    return redirect("membership", request.user.pk)


@require_editing_own_profile
def membership(request, pk):
    """Show our activate memberships."""
    member = get_object_or_404(get_user_model(), pk=pk)

    # TODO: Decide what the initial amount should actually be
    initial_amount = "50"

    form = PaymentForm(initial={"amount": initial_amount})

    if request.method == "POST":
        form = PaymentForm(request.POST, initial={"amount": initial_amount})
        if form.is_valid():
            payment = Payment(
                user=request.user,
                description="Membership",
                amount=form.selected_amount * 100,
                extra={"member": member.pk},
                success_url_name="membership_payment_success",
                failure_url_name="membership_payment_failure"
            )
            payment.save()
            return redirect("make_payment", payment.pk)

    memberships = member.memberships.order_by('-start_time')

    return render(request, "membership/membership.html",
                  {"member": member, "form": form, "memberships": memberships})


@login_required
@payment_successful
def membership_payment_success(request, payment):
    """Membership payment successful."""
    member = get_object_or_404(get_user_model(), pk=payment.extra["member"])
    if not payment.user == request.user:
        return HttpResponseForbidden()

    membership = Membership(user=member,
                            start_time=timezone.now(),
                            end_time=timezone.now() +
                            relativedelta(years=1),
                            amount=payment.amount / 100,
                            payment_id=payment.id)
    membership.save()

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
