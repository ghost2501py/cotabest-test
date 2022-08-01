from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('', include('products.api_v1.urls')),
]
