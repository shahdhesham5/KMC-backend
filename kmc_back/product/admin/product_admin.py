# Register your models here.
# from django.contrib import admin
from django.utils.translation import gettext as _

from kmc_back.generic_admin import *
from product.forms.product_forms import AtLeastOneRequiredInlineFormSet
from product.models.product_models import *


class ProductImageInline(TranslatableInline):
    formset = AtLeastOneRequiredInlineFormSet
    model = ProductImage


class ProductVideoUrlInline(TranslatableInline):
    model = ProductVideoUrl


class ProductItemInline(TranslatableInline):
    model = ProductItem
    extra = 1
    inlines = [TranslationInline]


class ProductItemAdmin(TranslatableAdmin):
    inlines = [TranslationInline]


class SubBranchInline(TranslatableInline):
    model = SubBranch
    extra = 1
    inlines = [TranslationInline]


class BranchInline(TranslatableInline):
    model = Branch
    extra = 1
    inlines = [TranslationInline, SubBranchInline]


class SubBranchAdmin(TranslatableAdmin):
    ordering = ["id"]
    list_display = ["name"]
    search_fields = ("name",)
    list_filter = ("branch__name",)
    inlines = [TranslationInline]


class BrandAdmin(TranslatableAdmin):
    ordering = ["id"]
    list_display = ["name"]
    search_fields = ("name",)
    inlines = [TranslationInline]


class ProductAdmin(TranslatableAdmin):
    ordering = ["id"]
    list_display = ["title", "branch", "sub_branch", "type", "price", "sale_price", "sale_percentage", "is_on_sale", "stock"]
    
    # Add fieldsets if needed
    fieldsets = (
        (
            _("Related tables"),
            {
                "fields": (
                    ("type", "brand", "is_archived"),
                    ("branch", "sub_branch"),
                )
            },
        ),
        (
            _("Info"),
            {
                "fields": (
                    "title",
                    "product_item_title",
                    "description",
                    "weight",
                    "number_of_boxes",
                )
            },
        ),
        (
            _("Price"),
            {
                "fields": (
                    ("price", "sale_price", "sale_percentage"),
                )
            },
        ),
        (
            _("Availability"),
            {"fields": ("stock",)},
        ),
        (
            _("Ratings"),
            {"fields": ("rate",)},
        ),
    )

    search_fields = ("title",)
    list_filter = ("brand__name", "branch__name", "sub_branch__name", "type__name")
    
    inlines = [
        TranslationInline,
        ProductImageInline,
        ProductVideoUrlInline,
        ProductItemInline,
    ]


    def is_on_sale(self, obj):
    # Ensure the product is marked as on sale only if there is a sale percentage or a sale price
        if obj.sale_percentage and obj.sale_percentage > 0:
            return True
        elif obj.sale_price and obj.sale_price < obj.price:
            return True
        return False

    is_on_sale.boolean = True
    is_on_sale.short_description = 'On Sale'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Filter products on sale
        queryset = queryset.filter(sale_percentage__gt=0) | queryset.filter(sale_price__isnull=False)
        return queryset


class BranchAdmin(TranslatableAdmin):
    ordering = ["id"]
    list_display = ["name", "type"]
    search_fields = ("name",)
    list_filter = ("type__name",)
    inlines = [TranslationInline, SubBranchInline]


class TypeAdmin(TranslatableAdmin):
    ordering = ["id"]
    list_display = ["name"]
    search_fields = ("name",)
    inlines = [TranslationInline, BranchInline]


admin.site.register(Type, TypeAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(SubBranch, SubBranchAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(ProductVideoUrl)
# admin.site.register(Review)
admin.site.register(WishList)
