from django.shortcuts import render
from Apps.Settings.models import GeneralSettings, Banner, CategoryImage
from Apps.Shop.models import Category, Product,Order

# from Product.models import Product, News


def header(request, *args, **kwargs):
    general_settings = GeneralSettings.objects.first()
    categories = Category.get_root_nodes().filter(is_active=True)
    context = {
        "title": "عنوان جدید",
        "categories": categories,
        "general_settings": general_settings,
    }
    open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    if open_order is not None:
        context['order'] = open_order
        context['cart_details'] = open_order.orderdetail_set.all()
    return render(request, "Layout/_header.html", context)


def footer(request, *args, **kwargs):
    general_settings = GeneralSettings.objects.first()
    context = {"general_settings": general_settings}
    return render(request, "Layout/_footer.html", context)


def index(request):
    context = {
        "sliders": Banner.objects.filter(position="S").all(),
        "top_banner_1": Banner.objects.filter(position="1").last(),
        "top_banner_2": Banner.objects.filter(position="2").last(),
        "mid_banner_1": Banner.objects.filter(position="3").last(),
        "mid_banner_2": Banner.objects.filter(position="4").last(),
        "special_products": Product.objects.filter(is_special=True).all(),
        "newest_products": Product.objects.order_by("-created_at").all(),
        "top_sale_products": Product.objects.filter(is_suggested=True).all(),
        "categories_images": CategoryImage.objects.all(),
    }
    return render(request, "index.html", context)


def terms(request):
    general_settings = GeneralSettings.objects.first()
    context = {
        "description": general_settings.terms_and_conditions,
    }
    return render(request, "rules-and-terms.html", context)

def about(request):
    general_settings = GeneralSettings.objects.first()
    context = {
        "description": general_settings.about,
    }
    return render(request, "about.html", context)

def contact(request):
    context = {}
    return render(request, "contact.html", context)


def faq(request):
    context = {}
    return render(request, "faq.html", context)

def how_to_buy(request):
    general_settings = GeneralSettings.objects.first()
    context = {
        "description": general_settings.how_to_buy,
    }
    return render(request, "how-to-buy.html", context)
