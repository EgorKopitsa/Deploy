from django.contrib import admin
from django.forms import ModelChoiceField

from .models import *


class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug']


class Design(admin.ModelAdmin):

    list_display = ['title', 'price', 'dimensions', 'available']
    list_filter = ['available']
    list_editable = ['price']
    prepopulated_fields = {'slug': ('title',)}


class TopImageAdmin(admin.StackedInline):
    model = ImageTop


class TopAdmin(Design):

    inlines = [TopImageAdmin]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='top'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Meta:
        model = Top

# class ButtonAdmin(Design):
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == 'category':
#             return ModelChoiceField(Category.objects.filter(slug='button'))
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
#
#
# class ShoesAdmin(Design):
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == 'category':
#             return ModelChoiceField(Category.objects.filter(slug='shoes'))
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'status', 'track_number', 'cart', 'delivery_price', 'created_at']
    list_editable = ['status', 'track_number']


class CartProductAdmin(admin.ModelAdmin):
    list_display = ['cart', 'user', 'content_object', 'size', 'qty', 'final_price']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'final_price']


class CarouselAdmin(admin.ModelAdmin):
    list_display = ['id']


class DeliveryAdmiin(admin.ModelAdmin):
    list_display = ['where']


admin.site.register(Category, CategoryAdmin)
# admin.site.register(Button, ButtonAdmin)
# admin.site.register(Shoes, ShoesAdmin)
admin.site.register(Top, TopAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Delivery, DeliveryAdmiin)
