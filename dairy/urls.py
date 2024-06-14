from django.urls import path
from . import views

app_name = 'dairy'

urlpatterns = [
    # farm views
    path('', views.farm_list, name='farm_list'),
    path('<int:id>/', views.farm_detail, name='farm_detail'),
]
