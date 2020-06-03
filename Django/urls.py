"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from photoalbum.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete-user/', DeleteUser.as_view(), name='delete-user'),
    path('edit-user/', EditUserView.as_view(), name='edit-user'),
    path('show-user/', ShowUserView.as_view(), name='show-user'),
    path('password/', PasswordView.as_view(), name='password'),
    path('password-changed/', PasswordChangedView.as_view(), name='password-changed'),
    path('add-user/', AddUser.as_view(), name='signup'),

    path('add-photo/', AddPhotoView.as_view(), name='add-photo'),
    path('', AddPhotoView.as_view(), name='add-ph'),
    path('user-photos/', UserPhotoView.as_view(), name='user-photos'),
    path('photo-details/<int:id>/', DetailsView.as_view(), name='photo-details'),
    path('user/<int:id>/', UserIdShowView.as_view(), name='user-id'),
    path('show-user/', ShowUserView.as_view(), name='show-user'),
    path('all-users/', AllUserView.as_view(), name='all-users'),




]
