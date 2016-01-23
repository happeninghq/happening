"""Finance views."""
from django.shortcuts import render, redirect
from forms import AccountForm, TransactionForm
from models import Account, Transaction
from django.core.urlresolvers import reverse
from django.db.models import Sum


def account(request):
    """List transactions against an account."""
    accounts = Account.objects.all()

    total_amount = Transaction.objects.all().aggregate(
        Sum('amount'))["amount__sum"]
    if not total_amount:
        total_amount = 0
    else:
        total_amount = total_amount

    transactions = Transaction.objects.order_by('-date')
    return render(request, "finances/staff/account.html",
                  {"accounts": accounts, "account": account,
                   "transactions": transactions,
                   "total_amount": total_amount})


def create_account(request):
    """Create an account."""
    form = AccountForm()
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            return redirect("finances", account.pk)
    return render(request, "finances/staff/create_account.html",
                  {"form": form})


def create_transaction(request):
    """Create a transaction."""
    form = TransactionForm()

    v_next = request.GET.get("next")

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            if form.cleaned_data.get("inflow"):
                transaction.amount = form.cleaned_data['inflow']
            else:
                transaction.amount = 0 - form.cleaned_data['outflow']
            transaction.save()

            if not v_next:
                return redirect("finances", transaction.account.pk)
            return redirect(v_next)
    return render(request, "finances/staff/create_transaction.html",
                  {"form": form, "next": v_next if v_next else reverse(
                   "finances", 0)})
