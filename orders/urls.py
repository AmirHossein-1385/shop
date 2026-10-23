from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('verify-phone/',views.verify_phone,name='verify_phone'),
    path('verify-code/',views.verify_code,name='verify_code'),
    path('order-create/',views.order_create,name='order_create'),
    # path('request/', views.send_request, name='request'),
    # path('verify/', views.verify , name='verify'),
    path('list-orders/', views.list_orders, name='list_orders'),
    path('order-detail/<int:order_id>/',views.order_detail,name='order_detail'),
    path('transaction-create/<int:order_id>/',views.transaction_pdf,name='transaction_create'),
    path('order-return/<int:order_id>/',views.order_return,name='order_return'),
    path('payment/',views.payment,name='payment'),
    path('payment/wallet/',views.payment_wallet,name='payment_wallet'),
    path('payment/bank/',views.payment_bank,name='payment_bank'),
    path('successful-payment/',views.successful_payment,name='successful_payment'),
    path('payment-failed/',views.payment_failed,name='payment_failed'),
]