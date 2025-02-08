from django.http import Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from Apps.Shop.forms import UserNewOrderForm
from .models import Order, OrderDetail, Product, ProductImage
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.


def products_archive(request):
    products_list = Product.objects.order_by("-created_at").all()
    paginator = Paginator(products_list, 1)

    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    context = {"page_obj": page_obj}
    return render(request, "Shop/shop.html", context)


def product_detail(request, *args, **kwargs):
    product_slug = kwargs["slug"]
    product = Product.objects.get_product_by_slug(product_slug)
    product_images = ProductImage.objects.filter(product=product).all()
    related_products = Product.objects.get_related_products_by_product_category(product)
    user_new_order_form = UserNewOrderForm(
        request.POST or None, initial={"product_id": product.pk}
    )
    context = {
        "product": product,
        "product_images": product_images,
        "related_products": related_products,
        "new_order_form": user_new_order_form,
    }
    return render(request, "Shop/product-detail.html", context)


@login_required(
    login_url="/login",
)
def add_user_order(request):
    new_order_form = UserNewOrderForm(request.POST or None)
    if new_order_form.is_valid():
        order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        if order is None:
            order = Order.objects.create(owner_id=request.user.id, is_paid=False)

        product_id = new_order_form.cleaned_data.get("product_id")
        count = new_order_form.cleaned_data.get("count")
        product = Product.objects.get_product_by_id(product_id)

        price = product.price
        if product.is_special:
            price = product.discounted_price

        order.orderdetail_set.create(
            product_id=product_id,
            price=price,
            count=count,
        )
        messages.success(request, "محصول به سبد خرید اضافه شد")
    else:
        messages.error(request, "خطا در افزودن به سبد خرید")

    return redirect(f"/shop/product/{product.slug}")

@login_required(login_url='/login', )
def user_open_order(request):
    context = {
        'order': None,
        'details': None
    }
    open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    if open_order is not None:
        context['order'] = open_order
        context['details'] = open_order.orderdetail_set.all()
    return render(request, 'shop/cart.html', context)


@login_required(login_url='/login', )
def remove_item_order(request, *args, **kwargs):
    detail_id = kwargs.get('detail_id')
    if detail_id is not None:
        order_detail = OrderDetail.objects.get_queryset().get(id=detail_id, order__owner=request.user.id)
        if order_detail is not None:
            order_detail.delete()
        messages.success(request, "محصول از سبد خرید حذف شد")
        return redirect('/cart')
    raise Http404()

@login_required(login_url='/login', )
def remove_all_order(request, *args, **kwargs):
    detail_id = kwargs.get('detail_id')
    if detail_id is not None:
        order_detail = OrderDetail.objects.get_queryset().get(id=detail_id, order__owner=request.user.id)
        if order_detail is not None:
            order_detail.delete()
        messages.success(request, "محصول از سبد خرید حذف شد")
        return redirect('/cart')
    raise Http404()