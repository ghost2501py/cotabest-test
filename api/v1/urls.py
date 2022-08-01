from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('', include('products.api.v1.urls')),
    path('', include('carts.api.v1.urls')),
]
