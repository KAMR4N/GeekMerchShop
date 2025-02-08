from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import *

# Register your models here.


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)
    list_display = ("title", "is_active")
    list_editable = ("is_active",)


class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute
    extra = 2


class AttributeCountFilter(admin.SimpleListFilter):
    title = "Attribute Count"
    parameter_name = "attr_count"

    def lookups(self, request, model_admin):
        return [
            ("more_5", "More Than 5"),
            ("lower_5", "lower Than 5"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "more_5":
            return queryset.annotate(attr_count=Count("attributes")).filter(
                attr_count__gt=5
            )
        if self.value() == "lower_5":
            return queryset.annotate(attr_count=Count("attributes")).filter(
                attr_count__lte=5
            )


@admin.register(ProductClass)
class ProductClassAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "require_shipping",
        "track_stock",
        "attribute_count",
    )
    list_filter = ("require_shipping", "track_stock", AttributeCountFilter)
    inlines = [ProductAttributeInline]
    actions = ["enable_track_stock"]
    prepopulated_fields = {"slug": ("title",)}

    def attribute_count(self, obj):
        return obj.attributes.count()

    def enable_track_stock(self, request, queryset):
        queryset.update(track_stock=True)


class ProductCategoryInline(admin.StackedInline):
    model = Product.categories.through
    extra = 2


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


# class ProductVariantInline(admin.TabularInline):
#     model = Product
#     fields = ("sku", "price", "quantity", "attributes")
#     extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "created_at",
    )
    inlines = [
        ProductAttributeValueInline,
        ProductImageInline,
        # ProductVariantInline,
    ]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Option)
admin.site.register(OptionGroup)
admin.site.register(OptionGroupValue)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(Order)
admin.site.register(OrderDetail)
