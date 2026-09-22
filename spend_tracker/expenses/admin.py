from django.contrib import admin
from .models import Expense
# Register your models here.

admin.site.register(Expense)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'category', 'note', 'date', 'created_at')
    list_filter = ('category', 'date')
    search_fields = ('category', 'note')