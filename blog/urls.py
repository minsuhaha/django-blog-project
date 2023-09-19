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
   
   path('image-upload/', views.image_upload.as_view(), name='image_upload'),

   path('board_detail/<int:post_id>/', views.board_detail, name= 'board_detail'),
   # 답변 url 추가 (9/17 수정완료)
   path('comment/create/<int:post_id>/', views.comment_create, name='comment_create'),
   path('<int:post_id>/comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
   path('comment/update/<int:comment_id>/', views.comment_update, name='comment_update'),


   path('autocomplete/', views.autocomplete, name='autocomplete'),
]