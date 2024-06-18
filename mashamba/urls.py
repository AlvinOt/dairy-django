from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.farm_detail_view, name='farm_detail'),
    path('<slug:slug>/cows/', views.cow_list_view, name='cow_list'),
    path('<slug:slug>/cows/<int:cow_id>/', views.cow_detail_view, name='cow_detail'),
    path('<slug:slug>/cows/<int:cow_id>/milking-sessions/', views.milking_sessions_view, name='milking_sessions'),
    path('<slug:slug>/all_cows_milk/', views.all_cows_milk_view, name='all_cows_milk'),
    ]

