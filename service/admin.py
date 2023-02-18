from django.contrib import admin

# Register your models here.
from .models import Users

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id' , 'nickname' , 'user_id' , 'subscription_date' , 'total_amount' , 'last_visit' , 'created_at')
    list_display_links  = ('id' , 'nickname')
    search_fields = ('id','nickname')
    list_editable = ('subscription_date',)
    ordering = ['total_amount']

