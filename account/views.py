from django.db.models import F
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from account.forms import Register, ChangePassword, WalletRecharge
from .models import Wallet, WalletTransaction
from django.db import transaction
# Create your views here.

def log_out(request):
    logout(request)
    return render(request,'account/registration/logout.html')


def register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            phone = form.cleaned_data.get('phone')
            user = form.save(commit=False)
            user.phone = phone
            user.set_password(password)
            with transaction.atomic():
                user.save()
                Wallet.objects.create(user=user)
            return render(request,'account/registration/register_done.html')
    else:
        form = Register()

    context = {
        'form':form
    }
    return render(request,'account/registration/register.html',context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePassword(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user = request.user
            user.set_password(new_password)
            user.save()
            return render(request,'account/registration/change_password_done.html')
    else:
        form = ChangePassword()

    context = {
        'form':form
    }
    return render(request,'account/registration/change_password.html',context)

@login_required
def wallet(request):
    user = request.user
    context = {
        'user':user,
    }
    return render(request,'account/wallet/wallet.html',context)

@login_required
def wallet_recharge(request):
    if request.method == 'POST':
        form = WalletRecharge(request.POST)
        if form.is_valid():
            user = request.user
            amount = form.cleaned_data.get('amount')
            wallet = user.wallet
            with transaction.atomic():
                Wallet.objects.filter(pk=wallet.pk).update(
                    balance=F('balance') + amount
                )
                WalletTransaction.objects.create(wallet=user.wallet, type='deposit', amount=amount)

            return redirect('account:wallet')

    else:
        form = WalletRecharge()
    context = {
        'form':form
    }
    return render(request,'account/wallet/wallet_recharge.html',context)

@login_required
def wallet_transaction(request):
    wallet = request.user.wallet
    transactions = WalletTransaction.objects.filter(wallet=wallet).order_by('-created')
    context = {
        'transactions':transactions,
        'wallet':wallet
    }
    return render(request,'account/wallet/wallet_transaction.html',context)
