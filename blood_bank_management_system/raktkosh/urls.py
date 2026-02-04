from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView,LoginView
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('about', views.About, name='about'),
    path('contact', views.contact, name='contact'),
    path('gallery', views.Gallery, name='gallery'),
    path('login/', views.Login_User, name='login'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('signup', views.Signup_User, name='signup'),
    path('logout/', views.Logout, name='logout'),
    path('change_password', views.Change_Password, name='change_password'),
    path('request_blood', views.request_blood,name='request_blood'),
    path('update-approve-status/<int:pk>', views.update_approve_status_view,name='update-approve-status'),
    path('update-reject-status/<int:pk>', views.update_reject_status_view,name='update-reject-status'),
    path('donator_blood', views.donator_blood,name='donator_blood'),
    path('approve_donation/<int:pk>/', views.approve_donation, name='approve_donation'),
    path('reject_donation/<int:pk>/', views.reject_donation, name='reject_donation'),
    path('admin_donation', views.admin_donation_view,name='admin_donation'),
    path('history', views.history,name='history'),
    path('view_user', views.view_user, name='view_user'),
    path('delete_user/<int:pid>', views.delete_user, name='delete_user'),
    path('profile', views.profile, name='profile'),
    path('edit_profile/<int:pid>', views.edit_profile, name='edit_profile'),
    path('request_history', views.request_history,name='request_history'),
    path('donation_history', views.donation_history,name='donation_history'),
    path('donate_blood', views.donate_blood_view,name='donate_blood'),
    path('make_request', views.make_request,name='make_request'),
    path('admin_blood', views.admin_blood,name='admin_blood'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)