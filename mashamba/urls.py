from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.farm_detail_view, name='farm_detail'),
    # Other paths specific to your app can be defined here
]

