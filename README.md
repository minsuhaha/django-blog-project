# 글 자동 완성 기능이 있는 블로그 만들기
## 개발 기간
#### 2023.09.11 ~ 2023.09.19
<br>

## 프로젝트 조원
|<a href="https://github.com/minsuhaha" target="_blank"> <img src="https://avatars.githubusercontent.com/u/105342203?v=4" alt="하민수" style="width:150px; border-radius:50px"/> </a> |<a href="https://github.com/KimChaeHong" target="_blank"> <img src="https://avatars.githubusercontent.com/u/49267413?v=4" alt="김채홍" style="width:150px; border-radius:50px"/> </a> |<a href="https://github.com/answjdchl" target="_blank"> <img src="https://avatars.githubusercontent.com/u/121854246?v=4" alt="최문정" style="width:150px; border-radius:50px"/> </a> |<a href="https://github.com/w1193" target="_blank"> <img src="https://avatars.githubusercontent.com/u/18063935?v=4" alt="허승범" style="width:150px; border-radius:50px"/> </a> |
|:----:|:-----:|:-----:|:-----:|
|하민수|김채홍|최문정|허승범|
<br>

## 프로젝트 개요
 - django 와 AI를 활용해 자동완성 기능이 존재하는 블로그를 만들어 보자! 오르미 2기 블만조 블로그 프로젝트 입니다.
 - 릴레이 코딩 방식 이용 (매일 다른 브랜치에서 코딩진행)
 - clone > python -m venv myvenv > pip install -r requirement.txt > password.json 작성
<br>


## 프로젝트 피그마
[프로젝트 피그마 바로가기](https://www.figma.com/file/9GMksH05GZAejl3UewASNd/%EC%98%A4%EB%A5%B4%EB%AF%B8-2%EA%B8%B0-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8(%EB%B8%94%EB%A1%9C%EA%B7%B8)-(Copy)?type=design&node-id=0-1&mode=design&t=CCql6XVRzchHDHFy-0)
<br><br>


## 프로젝트 모델 erd
<img width="555" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/09c46690-a98b-4940-8e37-0d90949d3992">
<br><br>


## 프로젝트 소개(UI)

### 로그인
<img width="412" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/dd4f5544-19de-467a-a7b6-f4caf92ac913">
<br>

### 메인페이지 (client)
<img width="412" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/64b976c4-f280-404d-a3f7-7e05cb0de2d1"><img width="412" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/3581daae-83de-4c4d-9106-6d204a4cb23a">
<br>

### 메인페이지 (admin)
<img width="412" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/c68f3de8-887e-4985-b2e3-54abea12eacc"><img width="400" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/feccd7be-c9f4-4abb-9414-72a04b93e7e8">
<br>

### 상세페이지 (client)
<img width="412" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/77f39dcf-03ea-4508-a1c1-bbe372af8c0b"><img width="414" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/48702067-ae45-47bb-8965-49e5d59424b2">
<br>

### 상세페이지 (admin)
<img width="412" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/1e2c8d07-4bea-46fb-9bb7-85beafae54bc"><img width="413" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/d3f3e9b4-1dfc-4972-86e3-51644152cd30">
<br>

### 글 작성페이지(CRUD)
<img width="412" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/05162f7c-321e-4918-8477-cf984378467d"><img width="412" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/157806b1-b049-4227-a865-2a682f4576b4">
<br>

### 댓글
<img width="412" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/d1807437-a8f2-4f75-bdd1-4753b59a0b1a"><img width="412" alt="image" src="https://github.com/minsuhaha/django-blog-project/assets/105342203/22a6f56b-4374-41d8-8274-43890b5a590b">
<br><br>


## 핵심 기능

### 메인페이지
- 로그인, 로그아웃 기능 구현
- 게시글 토픽 별 필터링
- 페이지네이션 기능
- 조회수에 따른 정렬 (조회수가 가장 많은 게시물이 대표 게시물로 나오도록 설정)
- 게시글 클릭 시 해당 게시글 상세페이지로 이동


### 상세페이지
- 추천 게시물 : 해당 게시글와 동일한 토픽
- 로그인 하지 않은 유저라면 공유하기 버튼만 보이도록 구현
- 로그인 한 유저라면 수정하기, 삭제하기, 공유하기(url복사) 버튼이 모두 보이도록 구현
- 동일한 토픽 중 게시글 올린 순서에 따른 이전글, 다음글 표시
- 댓글 CRUD 기능 구현 / 댓글 작성 시 익명이름과 비밀번호를 입력받고 댓글 수정 시 비밀번호를 먼저 입력받아 해당 댓글의 비밀번호와 동일한 비밀번호를 입력 시에만 댓글을 수정할 수 있도록 구현


### 글작성페이지
- AI 글 자동완성 기능 추가
- 게시글 CRUD 기능 구햔
- 임시저장기능 구현
- Tinymce 텍스트에디터 활용
<br><br>


## 프로젝트 노션 페이지
[블만조 노션 바로가기](https://smart-bill-194.notion.site/f675a118e3b34333990f1732e248d4e4?pvs=4)
<br><br>


## 활용 기술 스택
 - python
 - django
<br><br>

## 향후 추가하고 싶은 기능
- 회원가입 및 소셜로그인
- 좋아요 기능
- 제목 음성인식 기능
- 동일 아이피에서 접속했을 때 조회수가 더 이상 안올라가게 하는 기능
