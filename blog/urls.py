from django.urls import path
from . import views

urlpatterns = [
   path('', views.board, name='board'),
   path('write/', views.board_write, name='board_write'),
   path('login/', views.board_login, name='board_login'), 
   path('detail/', views.board_detail, name='board_detail')
]
