from django.urls import path
from . import views

urlpatterns = [
   
   path('write/', views.board_write, name='board_write'),
   path('login/', views.board_login, name='board_login'), 
]
