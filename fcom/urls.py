"""fcom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views

from django.urls import path, include
from dashboard.index.forms import LoginForm, admin_login, logout_dashboard_user, forget_password, partner_login
from home.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #dashboard pages urls
    path('admin/', include("dashboard.index.urls")),
    path('login/', admin_login, name='login'),
    path('partner/', partner_login, name='partner_login'),
    path('forget-password/', forget_password, name='forget_password'),
    path('logut/', logout_dashboard_user, name='logout_dashboard_user'),
    
    # path('login/', auth_views.LoginView.as_view(template_name="dashboard/login.html"),
    #      {'next_page': '/admin/dashboard', 'template_name': 'login.html', 'authentication_form': login_form}, name='login'),
    path('master/', include("dashboard.master.urls")),
    path('services/', include("dashboard.services.urls")),
    path('orders/', include("dashboard.orders.urls")),
    path('seo/', include("dashboard.seo.urls")),
    path('bookings/', include("bookings.urls")),

    #User pages urls 
    path('', home, name="HomePage"),
    path('', include("home.urls")),    
    path('helpdesk/', include("chat.urls")),    
    
  
    
    path('api/v1/user/', include("api.urls")),    
  #  path('api/v1/bookings/', include("bookings.urls")),    
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)  + static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
