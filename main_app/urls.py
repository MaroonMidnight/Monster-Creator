from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('monsters', views.monster_index, name='monster-index'),
    path('monsters/<int:monster_id>/', views.monster_detail, name='monster-detail'),
    path('monster/create/', views.MonsterCreate.as_view(), name='monster-create'),
]
