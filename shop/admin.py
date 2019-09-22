from django.contrib import admin
from django import forms
from django.http import HttpResponseRedirect
from mptt.admin import MPTTModelAdmin
from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.models import Gallery as PhotoLogeGallery
from .models import Category, Product, Gallery, Cart, CartItem, Order
from import_export.admin import ImportExportModelAdmin
from django.contrib import messages
from django.db import DatabaseError, IntegrityError

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug': ('name', )}

class CategoryMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    prepopulated_fields = {'slug': ('name', )}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'quantity', 'availability', 'created']
    list_filter = ['availability', 'created']
    list_editable = ['price', 'quantity', 'availability']
    prepopulated_fields = {'slug': ('name', )}

class CartItemAdmin(admin.ModelAdmin):
    """Товары в корзине"""
    list_display = ("cart", "product", "quantity")


class GalleryAdminForm(forms.ModelForm):
    """Users never need to enter a description on a gallery."""

    class Meta:
        model = PhotoLogeGallery
        exclude = ['description']


class GalleryAdmin(GalleryAdminDefault):
    form = GalleryAdminForm


class CartAdmin(admin.ModelAdmin):
    """Корзины"""
    list_display = ("id", "user", "accepted", )
    list_display_links = ("user", )
    # readonly_fields = ("cartitem",)
    actions = ['delete_model']

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions

    def check_cart_user(self, obj):
        return Cart.objects.filter(user=obj.user).count()

    def delete_model(self, request, obj):
        try:
            for i in obj.all():
                if self.check_cart_user(i) > 1:
                    i.delete()
        except:
            if self.check_cart_user(obj) > 1:
                obj.delete()

        self.message_user(request, "You cannot delete the last recycle bin")
        messages.success(request, "You cannot delete the last recycle bin")
        
    delete_model.short_description = 'Delete Cart'

# else:
#     self.message_user(request, 'LLALLALALA')

# def message_user(self, request, message, level=messages.INFO, extra_tags='',
#                  fail_silently=False):
#     message = 'LALALLALAL'
#     return message
#
#     messages.add_message(request, messages.ERROR, 'You can not delete the last cart')
#     messages.add_message(request, messages.INFO, 'You can not delete the last cart')
    # messages.error(request, 'You can not delete the last cart')
    # messages.info(request, 'You can not delete the last cart')
    # messages.warning(request, 'You can not delete the last cart')
    # messages.success(request, 'You can not delete the last cart')



class OrderAdmin(ImportExportModelAdmin):
    list_display = ('cart', 'accepted', 'date', )
    list_filter = ['date', 'accepted']
    search_fields = ('id', 'cart__user__username')
    readonly_fields = ('products_list', 'get_user')
    exclude = ('cart', 'product')



# @admin.register(OrderAdmin)
# class OrderAdmins(ImportExportModelAdmin):
#     pass


admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.unregister(PhotoLogeGallery)
admin.site.register(PhotoLogeGallery, GalleryAdmin)
admin.site.register(Cart, CartAdmin)
# admin.site.disable_action('delete_selected')
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
