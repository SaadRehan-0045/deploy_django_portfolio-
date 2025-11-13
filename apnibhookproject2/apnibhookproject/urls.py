# apnibhookproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_portfolio(request):
    return redirect('portfolio_home')

urlpatterns = [
    # path('admin/', admin.site.urls),  # Django admin
    path('', include('core.urls')),   # Your portfolio app
    path('django-admin/', admin.site.urls),  # Alternative Django admin URL
]