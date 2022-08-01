from django.urls import path

from .views import add_product, CartDetail, change_quantity, create_cart, remove_product

urlpatterns = [
    path('carts/create-cart/', create_cart),
    path('carts/<int:pk>/', CartDetail.as_view()),
    path('carts/<int:pk>/add-product/', add_product),
    path('carts/<int:pk>/change-quantity/', change_quantity),
    path('carts/<int:pk>/remove-product/<int:product_pk>/', remove_product),
]
