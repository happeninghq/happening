"""Finance views."""
from django.shortcuts import render, redirect
from .forms import AccountForm, TransactionForm
from .models import Account, Transaction
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib import messages


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
            form.save()
            messages.success(request, "The account has been created.")
            return redirect("finances")
    return render(request, "finances/staff/create_account.html",
                  {"form": form})


def create_transaction(request):
    """Create a transaction."""
    form = TransactionForm()

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The transaction has been added.")

            return redirect("finances")
    return render(request, "finances/staff/create_transaction.html",
                  {"form": form})


def edit_transaction(request, pk):
    """Edit a transaction."""
    transaction = get_object_or_404(Transaction, pk=pk)
    form = TransactionForm(instance=transaction)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated.")

            return redirect("finances")
    return render(request, "finances/staff/edit_transaction.html",
                  {"transaction": transaction, "form": form})


@require_POST
def delete_transaction(request, pk):
    """Delete a transaction."""
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    messages.success(request, "The transaction has been deleted.")

    return redirect("finances")
