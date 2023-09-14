# urls.py
from django.urls import path
from . import views

urlpatterns = [
   path('login/', views.board_login, name='board_login'), 
   path('logout/', views.board_logout, name='board_logout'), 
   
   path('', views.board, name='board'),
   path('topic/<int:topic>/', views.board, name='board_topic'),

   path('write/', views.create_or_update_post, name='board_write'),
   path('edit_post/<int:post_id>/', views.create_or_update_post, name='board_write'),
   
   path('board_detail/<int:post_id>/', views.board_detail, name= 'board_detail'),
]