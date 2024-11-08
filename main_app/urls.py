from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('monsters/', views.MonsterList.as_view(), name='monster-index'),
    path('monsters/<int:monster_id>/', views.monster_detail, name='monster-detail'),
    path('monsters/create/', views.MonsterCreate.as_view(), name='monster-create'),
    path('monsters/<int:pk>/update/', views.MonsterUpdate.as_view(), name='monster-update'),
    path('monsters/<int:pk>/delete/', views.MonsterDelete.as_view(), name='monster-delete'),
    path('moves/create/', views.MovesCreate.as_view(), name='moves-create'),
    path('monsters/<int:monster_id>/add-moves/', views.add_moves, name='add-moves'),
    path('moves/<int:pk>/', views.MovesDetail.as_view(), name='moves-detail'),
    path('moves/', views.MovesList.as_view(), name='moves-index'),
    path('moves/<int:pk>/update/', views.MovesUpdate.as_view(), name='moves-update'),
    path('moves/<int:pk>/delete/', views.MovesDelete.as_view(), name='moves-delete'),
    path('monsters/<int:monster_id>/associate-moves/<int:moves_id>/', views.associate_moves, name='associate-moves'),
    path('monsters/<int:monster_id>/remove-moves/<int:moves_id>/', views.remove_moves, name='remove-moves'),
    path('accounts/signup/', views.signup, name='signup'),
]
