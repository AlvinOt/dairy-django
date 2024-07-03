from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'mashamba'

urlpatterns = [
        
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('', views.home_view, name='home'),
    path('all_farms/', views.all_farms_view, name='all_farms'),
    #path('<slug:slug>/dashboard/', views.dashboard_view, name='dashboard'),
    path('farm-subscription/', views.subscribe_farm, name='farm_subscribe'),
    path('user_farms/', views.farm_list_view, name='farm_list'),
    path('<slug:slug>/pay-to-activate/', views.pay_to_activate_view, name='pay_to_activate'),
    path('<slug:slug>/', views.farm_detail_view, name='farm_detail'),
    path('<slug:slug>/cows/', views.cow_list_view, name='cow_list'),
    path('<slug:slug>/cows/add-cow/', views.add_cow_view, name='add_cow'),
    path('<slug:slug>/cows/<int:cow_id>/', views.cow_detail_view, name='cow_detail'),
    path('<slug:slug>/cows/<int:cow_id>/milking-sessions/', views.milking_sessions_view, name='milking_sessions'),
    path('<slug:slug>/cows/<int:cow_id>/milking-sessions/add-milking-session/', views.add_milking_session_view, name='add_milking_session'),
    path('<slug:slug>/all_cows_milk/', views.all_cows_milk_view, name='all_cows_milk'),
    ]

