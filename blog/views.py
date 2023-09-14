from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .forms import BlogForm
from .models import Post
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

    template = 'board_write.html'
    context = {'form': form, 'post': post, 'edit_mode': post_id is not None, 'MEDIA_URL': settings.MEDIA_URL,} #edit_mode: 글 수정 모드여부

    return render(request, template, context)


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
        posts = Post.objects.filter(topic=topic, publish='Y').order_by('-views')
    else:
        posts = Post.objects.filter(publish='Y').order_by('-views') 
    
    title_post = Post.objects.all().order_by('-view').first()
    return render(request, 'board.html', {'posts': posts ,'title_post':title_post})


# 상세 페이지 - board detail page
def board_detail(request, post_id):
    post_detail = Post.objects.get(id = post_id)
    # 포스트 id로 게시물 가져옴
    if request.method == 'POST': 
        
        # 요청에 삭제가 포함된경우
        if 'delete-button' in request.POST:
            post_detail.delete()
            return redirect('board_detail.html')

    # 조회수 증가 및 db에 저장
    post_detail.views += 1 
    post_detail.save() 

    # 이전/다음 게시물 가져옴
    previous_post = Post.objects.filter(id__lt=post_detail.id, storage='Y').order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post_detail.id, storage='Y').order_by('id').first()

    # 같은 주제인 게시물들 중 랜덤으로 가져옴
    recommended_posts = Post.objects.filter(topic=post_detail.topic, storage='Y').exclude(id=post_detail.id).order_by('?')

    # 랜덤으로 2개의 게시물 가져오기 (또는 원하는 개수로 조절)
    recommended_posts = random.sample(list(recommended_posts), 2)

    for recommended_post in recommended_posts:
        soup = BeautifulSoup(recommended_post.content, 'html.parser')
        image_tag = soup.find('img')
        recommended_post.image_tag = str(image_tag) if image_tag else ''
    
    context = {
        'post': post_detail,
        'previous_post': previous_post,
        'next_post': next_post,
        'recommended_posts': recommended_posts,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'board_detail.html', context)

