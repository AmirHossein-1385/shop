from django.contrib import admin

from shop.models import DiscountUsage
from .models import Order, OrderItem, SuccessfulTransaction, ReturnRequest
import openpyxl
from django.http import HttpResponse
import csv

from .services import approve_return


# Register your models here.


def export_to_excel(modeladmin,request,queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="orders.xlsx"'
    #--------
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Orders"
    #--------
    columns = ['Id','First Name','Last Name','Phone','Address','Postal Code','Province','City','Paid','Created']
    ws.append(columns)
    #--------
    for order in queryset:
        created = order.created.replace(tzinfo=None) if order.created else ''
        ws.append([
            order.id,order.first_name,order.last_name,order.phone,order.address,order.postal_code,order.province,order.city,
            order.paid,created
        ])
    wb.save(response)
    return response

export_to_excel.short_description = 'Export to Excel'


def export_to_csv(modeladmin,request,queryset):
    response = HttpResponse(content_type="text/csv",headers={"content-Disposition":'attachment;filename="orders.csv'})
    writer = csv.writer(response)
    writer.writerow(['Id','First Name','Last Name','Phone','Address','Postal Code','Province','City','Paid','Created'])
    for order in queryset:
        writer.writerow([
            order.id,
            order.first_name,
            order.last_name,
            order.phone,
            order.address,
            order.postal_code,
            order.province,
            order.city,
            order.paid,
            order.created
            ])

    return response

export_to_csv.short_description = 'Export to CSV'


def approve_return(modeladmin, request, queryset):
    for item in queryset:
        approve_return(item.order)
        item.status = 'تایید کردن'
        item.save()


approve_return.short_description = 'Approve return'

def reject_return(modeladmin, request, queryset):
    for item in queryset:
        item.status = 'رد کردن'
        item.save()

reject_return.short_description = 'Reject return'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','buyer','first_name','last_name','phone','address','postal_code','city','province','status','paid','delivery_time','created','updated']
    inlines = [OrderItemInline]
    list_filter = ['paid', 'created', 'updated']
    list_editable = ['status']
    actions = [export_to_excel , export_to_csv]


@admin.register(SuccessfulTransaction)
class SuccessfulTransactionAdmin(admin.ModelAdmin):
    list_display = ['amount','transaction_id','created']

@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ['order_id','order_items','status','created']
    list_editable = ['status']
    actions = [approve_return,reject_return]

    def order_items(self, obj):
        return " ,  ".join(
            f"{item.product.name}×{item.quantity}"
            for item in obj.order.items.all()
        )

    order_items.short_description = "Order items"

@admin.register(DiscountUsage)
class DiscountUsageAdmin(admin.ModelAdmin):
    list_display = ['user','discount','order','used']