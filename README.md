# QA(Question Answering Service) 서비스 

## 1. BERT 모델 다운로드
https://sites.google.com/view/aitutorial 에서 bert_small.zip 파일을 다운로드하여서 프로젝트 디렉토리에 압축해제 하세요.

## 2. 파이썬 가상환경 생성 및 실행
- python –m venv venv 
- Windows : venv\Scripts\activate.bat
- Linux : source venv/bin/activate

## 3. 파이썬 패키지 설치
- pip install django
- pip install djangorestframework
- pip install drf-yasg
- pip install django-import-export
- pip install django-cors-headers
- pip install konlpy
- pip install torch==1.8.1

## 4. 테이블 생성
- cd server
- python manage.py migrate
- python manage.py makemigrations mrc
- python manage.py migrate mrc

## 5. 데이터베이스 관리자 계정 생성
- python manage.py createsuperuser

## 6. MRC QA 데이터셋 로드
- python manage.py shell < load_korquad_data.py

## 7. 백엔드 실행
- python manage.py runserver

## 8. 프론트엔드 소스 다운로드 
- https://github.com/kgpark88/client

## 9. NPM 패키지 설치 
- npm run install

## 10. 프론트엔드 실행
- npm run serve

