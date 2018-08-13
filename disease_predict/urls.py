"""disease_predict URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from symptoms import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='home'),
    path('signup/', accounts_views.signup, name='signup'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardListView.as_view(), name='dashboard'),
    path('dashboard/<int:pk>/', views.EachDiseaseListView.as_view(), name='eachdisease'),
    path('dashboard/<int:pk>/disease/<int:disease_pk>/', views.SingleDiseaseListView.as_view(), name='singledisease'),
    path('dashboard/search/', views.search, name='search'),
    path('disease/', views.DiseaseListView.as_view(), name='view_disease'),
    path('doctor/', accounts_views.DoctorListView.as_view(), name='doctor'),
    path('doctor/search/', accounts_views.doctor_search, name='doctor_search'),
    path('settings/account/', accounts_views.update_profile, name='my_account'),
    path('settings/password/',
         auth_views.PasswordChangeView.as_view(
             template_name='password_change.html'
         ),
         name='password_change'),
    path('settings/password/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='password_change_done.html'
         ),
         name='password_change_done'),

    path('map/', views.MapListView.as_view(), name='map'),

    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
