from django.urls import path
from .views import (
    product_detail,
    products_archive,
    add_user_order,
    remove_item_order,
    user_open_order,
    remove_all_order,
    payment,
    search_products,
)

urlpatterns = [
    path("shop/", products_archive, name="shop"),
    path("shop/category/<slug>", products_archive, name="shop"),
    path("shop/product/<slug>", product_detail),
    path("shop/search", search_products),
    path("add-user-order", add_user_order),
    path("cart", user_open_order, name="user_cart"),
    path(
        "cart/remove-item-order/<detail_id>",
        remove_item_order,
        name="remove-item-order",
    ),
    path("cart/remove-all-order/", remove_all_order, name="remove-all-order"),
    path("cart/checkout/", remove_all_order, name="checkout"),
    path("cart/payment/", payment, name="payment"),
]
