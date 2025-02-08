from django.urls import path
from .views import product_detail, products_archive, add_user_order, remove_item_order, user_open_order,remove_all_order

urlpatterns = [
    path("shop/", products_archive, name="shop"),
    path("shop/category/<slug>", products_archive, name="shop"),
    path("shop/product/<slug>", product_detail),
    
    path("add-user-order", add_user_order),
    path('cart', user_open_order, name='user_cart'),
    path('cart/remove-item-order/<detail_id>', remove_item_order, name='remove-item-order'),
    path('cart/remove-all-order/', remove_all_order, name='remove-all-order'),
    path('cart/checkout/', remove_all_order, name='checkout'),
    
    # path('products/', ProductList.as_view(), name='products'),
    # path('products/<category_name>', ProductCategoryList.as_view()),
    # path('products/<pk>/<title>', product_detail),
    # path('products/search', ProductSearchList.as_view()),
    # path('products_categories_partial', products_categories_partial, name='products_categories'),
]
