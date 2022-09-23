from atexit import register
from django.contrib import admin
from .models import Paymentt, Shopcartt

# Register your models here.

@admin.register(Shopcartt)
class Shopcarttadmin(admin.ModelAdmin):
    list_display = ['user', 'dish', 'c_name','c_item','c_date', 'quantity', 'c_price', 'amount', 'cart_code', 'paid']
    readonly_fields = ['user','dish','c_name', 'quantity', 'c_price', 'amount', 'cart_code', 'paid']


@admin.register(Paymentt)
class Paymentt(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name','phone','address','city', 'total', 'cart_code', 'pay_code','paid','pay_date', 'admin_note', 'admin_update']
    readonly_fields = ['user', 'first_name', 'last_name','address','city', 'total', 'cart_code', 'pay_code','paid','pay_date']