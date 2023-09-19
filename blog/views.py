# views.py
from django.contrib import messages
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import openai
from .forms import BlogForm, CommentForm
from .models import Post
from bs4 import BeautifulSoup
from django.core.files.storage import default_storage
import random
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Comment
from django.db.models import Q
import json, os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PASSWORD_FILE = os.path.join(BASE_DIR, 'password.json')
secrets = json.load(open(PASSWORD_FILE))


openai.api_key = secrets["openai_api_key"]

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
                post.topic = '전체'
            
            # 임시저장 여부 설정
            if 'temp-save-button' in request.POST:
                post.storage = 'N'
            else:
                post.storage = 'Y'

            # 글쓴이 설정
            post.writer = request.user

            post.save()
            return redirect('board_detail', post_id=post.id) # 업로드/수정한 페이지로 리다이렉트
        print(form.errors)

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
        posts = Post.objects.filter(topic=topic, storage='Y').order_by('-view')
        if  Post.objects.filter(topic=topic, storage='Y'):
            title_post = Post.objects.filter(topic=topic, storage='Y').order_by('-view').first()
        else:
            title_post = None
    else:
        posts = Post.objects.filter(storage='Y').order_by('-view') 
        title_post = Post.objects.all().order_by('-view').first()
    # current_topic 값 추가로 넘겨주기 (9/15 수정완료) : 토픽 별 필터링 표시

    # 검색 기능
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(Q(title__icontains=search_query) | 
                             Q(content__icontains=search_query) |
                             Q(writer__username__icontains = search_query))

    # 페이지네이션
    page = request.GET.get('page')  

    paginator = Paginator(posts, 6)

    try:
        page_obj = paginator.get_page(page)
    
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.get_page(page)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    try:  
        left_index = (int(page) - 2)
        if left_index < 1:
            left_index = 1

        right_index = (int(page) + 2)
        if right_index > paginator.num_pages:
            right_index = paginator.num_pages

        custom_range = range(left_index, right_index+1)

    except TypeError:
        page = 1

        left_index = (int(page) - 2)
        if left_index < 1:
            left_index = 1

        right_index = (int(page) + 2)
        if right_index > paginator.num_pages:
            right_index = paginator.num_pages

        custom_range = range(left_index, right_index+1)

    
    return render(request, 'board.html', {'posts': posts ,'title_post': title_post, 'current_topic': topic, 'page_obj': page_obj, 'paginator': paginator, 'custom_range': custom_range})


# 상세 페이지 - board detail page
def board_detail(request, post_id):
    post_detail = Post.objects.get(id = post_id)
    # 포스트 id로 게시물 가져옴
    if request.method == 'POST': 
        
        # 요청에 삭제가 포함된경우
        if 'delete-button' in request.POST:
            post_detail.delete()
            return redirect('board')

    # 조회수 증가 및 db에 저장
    post_detail.view += 1 
    post_detail.save() 

    # 이전/다음 게시물 가져옴
    previous_post = Post.objects.filter(id__lt=post_detail.id, storage='Y').order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post_detail.id, storage='Y').order_by('id').first()

    # 같은 주제인 게시물들 중 최신 글 가져옴
    recommended_posts = Post.objects.filter(topic=post_detail.topic, storage='Y').exclude(id=post_detail.id).order_by('-create_date')[:2]

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


# 이미지 업로드
class image_upload(View):
    
    # 사용자가 이미지 업로드 하는경우 실행
    def post(self, request):
        
        # file필드 사용해 요청에서 업로드한 파일 가져옴
        file = request.FILES['file']
        
        # 저장 경로 생성
        filepath = 'uploads/' + file.name
        
        # 파일 저장
        filename = default_storage.save(filepath, file)
        
        # 파일 URL 생성
        file_url = settings.MEDIA_URL + filename
        
        # 이미지 업로드 완료시 JSON 응답으로 이미지 파일의 url 반환
        return JsonResponse({'location': file_url})
    
# 답변등록 answer_create view (9/17 생성완료)
def comment_create(request, post_id):
    """
    pybo 답변등록
    """
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('board_detail', post_id=post.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'post': post, 'form': form}
    return render(request, 'board_detail.html', context)


def comment_delete(request,post_id, comment_id ):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('board_detail', post_id)

def comment_update(request,post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    form = CommentForm(instance=comment)
    post = get_object_or_404(Post, pk=post_id)
    # if request.method == "POST":
    update_form = CommentForm(request.POST, instance=comment)
    if update_form.is_valid():
        update_form.save()
        return redirect('board_detail', post_id)
    context = {'post': post, 'form': form}
    return render(request, 'board_detail.html', context)


def autocomplete(request):
    if request.method == "POST":

        #제목 필드값 가져옴
        prompt = request.POST.get('title')
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            # 반환된 응답에서 텍스트 추출해 변수에 저장
            message = response['choices'][0]['message']['content']
        except Exception as e:
            message = str(e)
        return JsonResponse({"message": message})
    return render(request, 'autocomplete.html')