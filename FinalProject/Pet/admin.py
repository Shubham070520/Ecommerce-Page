from django.contrib import admin
from Pet.models import Pet
from Pet.models import Cart

# Register your models here.
class PetAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'type', 'breed', 'gender', 'description', 'price', 'age']
    list_filter = ['type', 'breed', 'gender','price', 'age']
    search_fields = ['name', 'type', 'breed', 'gender', 'description', 'price', 'age']

admin.site.register(Pet, PetAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','pid', 'uid', 'quantity']
    list_filter = ['uid']

admin.site.register(Cart, CartAdmin)