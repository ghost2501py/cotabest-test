from django.urls import include, path

app_name = 'api_v1'

urlpatterns = [
    path('', include('products.api.v1.urls', namespace='products')),
    path('', include('carts.api.v1.urls', namespace='carts')),
]
