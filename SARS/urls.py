"""
URL configuration for demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from covid_app import views
from covid_app.views import signup_view, login_view, dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    # path('predict/',views.predict,name='predict'),
    path('add/', views.predict, name='add_patient'),
    path('predict/', views.predict, name='predict'),

    path('update/<int:patient_id>/', views.update_contact, name='update_contact'),
    path('delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('add/<int:patient_id>/', views.add_patient, name='add_patient'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

