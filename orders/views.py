# Create your views here.
from datetime import datetime, timedelta
from django.db import transaction
import uuid
from shop.models import Product
from shop.models import DiscountCode
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from shop.models import DiscountUsage
from .forms import VerifyPhoneForm , OrderCreateForm
from django.contrib.auth import login
from account.models import ShopUser, WalletTransaction
from .models import OrderItem, Order, SuccessfulTransaction, ReturnRequest
import random
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from django.conf import settings
import arabic_reshaper
from bidi.algorithm import get_display


def verify_phone(request):
    if request.user.is_authenticated:
        return redirect('orders:order_create')

    if request.method == 'POST':
        form = VerifyPhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            tokens = {'token':''.join(random.choices('0123456789',k=6))}
            request.session['verification_code'] = tokens['token']
            request.session['verification_code_time'] = timezone.now().isoformat()
            request.session['phone'] = phone
            # send sms (tokens)
            print("token:",tokens['token'])
            messages.success(request,'Verification code sent successfully')
            return redirect('orders:verify_code')
    else:
        form = VerifyPhoneForm()
    context = {
        'form':form
    }
    return render(request, 'verify_phone.html',context)


def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            verification_code = request.session['verification_code']
            phone = request.session['phone']
            code_time = datetime.fromisoformat(request.session['verification_code_time'])
            expire_time = code_time + timedelta(minutes=1)
            if timezone.now() > expire_time:
                del request.session['verification_code']
                del request.session['verification_code_time']
                del request.session['phone']
                messages.error(request,'کد منقضی شده هست لطفا دوباره شماره رو وارد کنید')
                return redirect('orders:verify_phone')

            if code == verification_code:
                user = ShopUser.objects.create_user(phone=phone, password='123456')
                print(user)
                login(request, user)
                # send sms (password)
                del request.session['verification_code']
                del request.session['verification_code_time']
                del request.session['phone']
                return redirect('orders:order_create')

            else:
                messages.error(request,'Invalid verification code')

    return render(request,'verify_code.html')

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.buyer = request.user
                order.save()
                for product_id, item in cart.cart.items():
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item["quantity"],
                        price=product.new_price,
                        weight=product.weight
                    )
                request.session['order_id'] = order.id
        return redirect('orders:payment')

    else:
        form = OrderCreateForm(initial={
            'first_name' : request.user.first_name,
            'last_name' : request.user.last_name,
            'phone' : request.user.phone,
        })


    context = {
        'form':form,
        'cart':cart,
        'user':request.user
    }
    return render(request, 'order_create.html',context)





# @login_required
# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.buyer = request.user
#             order.save()
#             for item in cart:
#                 OrderItem.objects.create(order=order,product=item["product"], quantity=item["quantity"], price=item["price"], weight=item["weight"])
#             request.session['order_id'] = order.id
#             SuccessfulTransaction.objects.create(order=order,amount=cart.get_final_price(),transaction_id='10104523')
#             discount_code = request.session.get('discount_code')
#             discount = DiscountCode.objects.filter(code=discount_code).first()
#             if discount:
#                 DiscountUsage.objects.create(order=order,discount=discount,user=request.user)
#                 request.session.pop('discount_code',None)
#             for item in order.items.all():
#                 item.product.inventory -= item.quantity
#                 item.product.save()
#             cart.clear()
#             order.save()
#             return redirect('shop:product_list')
#     else:
#         form = OrderCreateForm(initial={
#             'first_name' : request.user.first_name,
#             'last_name' : request.user.last_name,
#             'phone' : request.user.phone,
#         })
#
#
#     context = {
#         'form':form,
#         'cart':cart,
#         'user':request.user
#     }
#     return render(request, 'order_create.html',context)
#--------------------------------------------------------------------------
#
# from django.conf import settings
# import requests
# import json
# from django.http import HttpResponse
#
# # ? sandbox merchant
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'
#
# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
#
#
# # Important: need to edit for realy server.
# CallbackURL = 'http://127.0.0.1:8000/orders/verify/'
#
#
# def send_request(request):
#     order = Order.objects.get(id=request.session['order_id'])
#
#     description = ""
#
#     for item in order.items.all():
#         description += item.product.name + ','
#
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": order.get_final_cost(),
#         "Description": description,
#         "Phone": request.user.phone,
#         "CallbackURL": CallbackURL,
#     }
#
#     data = json.dumps(data)
#
#     headers = {
#         'content-type': 'application/json',
#         'content-length': str(len(data))
#     }
#
#     try:
#         response = requests.post(
#             ZP_API_REQUEST,
#             data=data,
#             headers=headers,
#             timeout=10
#         )
#
#         if response.status_code == 200:
#             response = response.json()
#
#             if response['Status'] == 100:
#                 for item in order.items.all():
#                     item.product.inventory -= item.quantity
#                     item.product.save()
#                 order.paid = True
#                 order.save()
#                 return {'status': True,'url': ZP_API_STARTPAY + str(response['Authority']),'authority': response['Authority']}
#
#             return {'status': False,'code': str(response['Status'])}
#
#         return {'status': False,'code': response.status_code}
#
#     except requests.exceptions.Timeout:
#         return {'status': False,'code': 'timeout'}
#
#     except requests.exceptions.ConnectionError:
#         return {'status': False,'code': 'connection error'}
#
#
# def verify(request):
#     order = Order.objects.get(id=request.session['order_id'])
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount":order.get_final_cost(),
#         "Authority": request.GET.get('Authority'),
#     }
#
#     data = json.dumps(data)
#
#     headers = {
#         'content-type': 'application/json',
#         'content-length': str(len(data))
#     }
#
#     try:
#         response = requests.post(
#             ZP_API_VERIFY,
#             data=data,
#             headers=headers,
#             timeout=10
#         )
#
#         if response.status_code == 200:
#             response = response.json()
#
#             if response['Status'] == 100:
#                 return {'status': True,'RefID': response['RefID']}
#
#             del request.session['order_id']
#
#             return {
#                 'status': False,
#                 'code': str(response['Status'])
#             }
#
#         return {
#             'status': False,
#             'code': response.status_code
#         }
#
#     except requests.exceptions.Timeout:
#         return {
#             'status': False,
#             'code': 'timeout'
#         }
#
#     except requests.exceptions.ConnectionError:
#         return {
#             'status': False,
#             'code': 'connection error'
#         }
#----------------------------------------------------------------------


def list_orders(request):
    user = request.user
    orders = Order.objects.filter(buyer=user)
    return render(request,'list_orders.html',{'orders':orders})

@login_required
def order_detail(request,order_id):
    user = request.user
    order = Order.objects.get(id=order_id )
    status_request = ReturnRequest.objects.filter(order_id=order_id).first()
    if order.buyer == user:
        context = {
            'order':order,
            'status_request':status_request
        }
        return render(request,'order_detail.html',context)
    else:
        return HttpResponse("You are not allowed to see this order")



pdfmetrics.registerFont(
    TTFont("Vazirmatn",os.path.join(settings.BASE_DIR,"orders","static","fonts","Vazirmatn-Regular.ttf"))
)

def persian_text(text):
    text = arabic_reshaper.reshape(str(text))
    return get_display(text)


def transaction_pdf(request,order_id):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    order = Order.objects.get(id=order_id)

    p.setFont("Vazirmatn", 12)
    p.drawString(50, 570, persian_text(f"نام و نام خانواگی:{order.first_name} {order.last_name}"))
    p.drawString(50, 750, persian_text(f"خریدار: {order.buyer}"))
    p.drawString(50, 690, persian_text(f"آدرس: {order.address}"))
    p.drawString(50, 670, persian_text(f"کد پستی: {order.postal_code}"))
    p.drawString(50, 650, persian_text(f"شهر: {order.city}"))
    p.drawString(50, 630, persian_text(f"استان: {order.province}"))
    p.drawString(50, 590, persian_text(f"وضعیت: {order.status}"))
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="transaction.pdf")


def order_return(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.delivery_time:
        return_period = order.delivery_time + timedelta(days=7)
        if return_period < timezone.now():
            messages.error(request,"مهلت مرجوعی این سفارش به پایان رسیده است")
        else:
            if not ReturnRequest.objects.filter(order_id=order.id).exists():
                ReturnRequest.objects.create(order_id=order_id)
                messages.success(request,"درخواست شما با موفقیت ثبت شد")
            else:
                messages.error(request,"شما قبلا این درخواست رو ثبت کرده اید")
    else:
        messages.error(request,"این سفارش هنوز تحویل داده نشده")

    return redirect('orders:order_detail',order_id=order_id)


def payment(request):
    return render(request,'payment.html')


@login_required
@require_POST
def payment_wallet(request):
    order_id = request.session.get('order_id')

    if not order_id:
        return redirect('orders:list_orders')

    with transaction.atomic():
        order = get_object_or_404(
            Order.objects.select_for_update(),
            id=order_id,
            buyer=request.user,
        )

        if order.paid:
            return redirect('orders:successful_payment')

        wallet = request.user.wallet.__class__.objects.select_for_update().get(
            pk=request.user.wallet.pk
        )

        price_total = order.get_final_cost()

        if wallet.balance < price_total:
            return redirect('orders:payment_failed')

        wallet.balance -= price_total
        wallet.save(update_fields=['balance'])

        for item in order.items.all():
            item.product.inventory -= item.quantity
            item.product.save(update_fields=['inventory'])


        order.paid = True
        order.save(update_fields=['paid'])
        SuccessfulTransaction.objects.create(order_id=order.id,amount=price_total,transaction_id=uuid.uuid4().hex)
        discount_code = request.session.get('discount_code')

        if discount_code:
            discount = DiscountCode.objects.filter(
                code=discount_code
            ).first()

            if discount:
                DiscountUsage.objects.create(
                    order=order,
                    discount=discount,
                    user=request.user
                )
        WalletTransaction.objects.create(wallet=wallet,amount=price_total,type='purchase')

        request.session.pop('order_id',None)
        request.session.pop('cart',None)
        request.session.pop('discount_code',None)



    return redirect('orders:successful_payment')



@login_required
@require_POST
def payment_bank(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('orders:list_orders')
    with transaction.atomic():
        order = get_object_or_404(Order.objects.select_for_update(), id=order_id, buyer=request.user)

        if order.paid:
            return redirect('orders:successful_payment')

        price_total = order.get_final_cost()
        items = list(order.items.select_related('product'))

        for item in items:
            if item.product.inventory < item.quantity:
                return redirect('orders:payment_failed')

        for item in items:
                item.product.inventory -= item.quantity
                item.product.save(update_fields=['inventory'])

        order.paid = True
        order.save(update_fields=['paid'])
        SuccessfulTransaction.objects.create(order=order,amount=price_total,transaction_id=uuid.uuid4().hex)
        discount_code = request.session.get('discount_code')

        if discount_code:
            discount = DiscountCode.objects.filter(
                code=discount_code
            ).first()

            if discount:
                DiscountUsage.objects.create(
                    order=order,
                    discount=discount,
                    user=request.user
                )

        request.session.pop('order_id', None)
        request.session.pop('cart', None)
        request.session.pop('discount_code', None)

    return redirect('orders:successful_payment')

def successful_payment(request):
    return render(request,'successful_payment.html')

def payment_failed(request):
    return render(request,'payment_failed.html')