"""
URL configuration for qnd41app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from usuarios.views import dashboard_view
from .sites import custom_admin_site

# Change the parentheses to square brackets for a list
urlpatterns = [
    path("admin2/", custom_admin_site.urls),
    path("admin/", dashboard_view),
    path('analytics/', admin.site.urls),
    path('appointment/', include('appointment.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('rosetta/', include('rosetta.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('MEDDES/', include('usuarios.urls', namespace='usuarios')),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #path('calendario/', self.admin_site.admin_view(self.calendar_view), name='citas_calendar'),
    # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# Add static URLs to the urlpatterns if in debug mode
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
