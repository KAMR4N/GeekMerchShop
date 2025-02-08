from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import *


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)
    list_display = ("title", "is_active")
    list_editable = ("is_active",)


class ProductCategoryInline(admin.StackedInline):
    model = Product.categories.through
    extra = 2


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "created_at",
    )
    inlines = [
        ProductImageInline,
        # ProductVariantInline,
    ]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Order)
admin.site.register(OrderDetail)
