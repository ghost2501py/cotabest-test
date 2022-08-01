from django.urls import path

from .views import (
    add_product, CartDetail, change_quantity, create_cart, finish,
    remove_product,
)

app_name = 'carts'

urlpatterns = [
    path('carts/create-cart/', create_cart, name='cart-create'),
    path('carts/<int:pk>/', CartDetail.as_view(), name='cart-detail'),
    path('carts/<int:pk>/add-product/', add_product, name='add-product'),
    path('carts/<int:pk>/change-quantity/', change_quantity, name='change-quantity'),
    path('carts/<int:pk>/remove-product/<int:product_pk>/', remove_product, name='remove-product'),
    path('carts/<int:pk>/finish/', finish, name='finish'),
]
