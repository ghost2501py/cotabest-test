from django.urls import include, path
from django.views.generic import TemplateView

app_name = 'api_v1'

urlpatterns = [
    path('docs/', TemplateView.as_view(template_name='insomnia.html')),
    path('', include('products.api.v1.urls', namespace='products')),
    path('', include('carts.api.v1.urls', namespace='carts')),
]
