import random
# views.py
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views import View
from .forms import BlogForm
from .models import Post
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.files.storage import default_storage
from bs4 import BeautifulSoup
import random


# 포스트 업로드, 업데이트, 삭제
def create_or_update_post(request, post_id=None):
    # 글수정 페이지의 경우
    if post_id:
        post = get_object_or_404(Post, id=post_id)
    
    # 글쓰기 페이지의 경우, 임시저장한 글이 있는지 검색 
    else:
        post = Post.objects.filter(writer_id=request.user, storage ='N').order_by('-create_date').first()

    # 업로드/수정 버튼 눌렀을 떄
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=post) # 폼 초기화
        if form.is_valid():
            post = form.save(commit=False)

            # 게시물 삭제
            if 'delete-button' in request.POST:
                post.delete() 
                return redirect('board') 

            if not form.cleaned_data.get('topic'):
                post.topic = '여행'
            
            # 임시저장 여부 설정
            if 'temp-save-button' in request.POST:
                post.storage = 'N'
            else:
                post.storage = 'Y'

            # 글쓴이 설정
            post.writer = request.user

            post.save()
            return redirect('board_detail', post_id=post.id) # 업로드/수정한 페이지로 리다이렉트
    
    # 수정할 게시물 정보를 가지고 있는 객체를 사용해 폼을 초기화함
    else:
        form = BlogForm(instance=post)
    context = {'form': form}
    return render(request, 'board_write.html', context)

# 게시물 삭제 - board detail page
@login_required(login_url='board_login')
def board_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.writer:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('board_detail', post_id=post.id)
    post.delete()
    return redirect('board')


# 로그인 - login page
def board_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('board')  # 로그인 성공 시 리디렉션할 페이지
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 로그아웃 - logout page
def board_logout(request):
    logout(request)
    return redirect('board')



# 메인 게시판 - board page
def board(request, topic=None):
    if topic:
        posts = Post.objects.filter(topic=topic, storage='Y').order_by('-view')
    else:
        posts = Post.objects.filter(storage='Y').order_by('-view') 
    
    title_post = Post.objects.all().order_by('-view').first()
    return render(request, 'board.html', {'posts': posts ,'title_post':title_post})



# 상세 페이지 - board detail page
def board_detail(request,id):
    post_detail = Post.objects.filter('id' == id)
    return render(request, 'board_detail.html')
