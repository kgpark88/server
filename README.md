# QA(Question Answering Service) 서비스 

## 1. 소스 다운로드
git clone https://github.com/kgpark88/server

## 2. BERT 모델과 KorQuAD 샘플 데이터셋 다운로드
- https://sites.google.com/view/ai-tutorial 에서 [자연어처리] 메뉴를 클릭하세요.
- 모든 파일을 server/bert_small/  디렉토리에 다운로드 하세요.
-  KorQuAD_v1.0_train.json, KorQuAD_v1.0_dev.json 파일은 server/ 디렉토리에 다운로드 하세요.

## 3. 파이썬 가상환경 생성 및 실행
- python –m venv venv 
- Windows : venv\Scripts\activate.bat
- Linux : source venv/bin/activate

## 4. 파이썬 패키지 설치
- pip install django
- pip install djangorestframework
- pip install drf-yasg
- pip install django-import-export
- pip install django-cors-headers
- pip install konlpy
- pip install torch==1.8.1
- pip install transformers

## 5. 테이블 생성
- cd server
- python manage.py migrate
- python manage.py makemigrations mrc
- python manage.py migrate mrc

## 6. 데이터베이스 관리자 계정 생성
- python manage.py createsuperuser

## 7. KorQuAD 샘플 데이터셋 로드
- python manage.py shell < load_korquad_data.py

## 8. 백엔드 실행
- python manage.py runserver

## 9. 프론트엔드 소스 다운로드 
- https://github.com/kgpark88/client

## 10. NPM 패키지 설치 
- npm run install

## 11. 프론트엔드 실행
- npm run serve

## 서버 실행 화면
![image](https://user-images.githubusercontent.com/17672596/142607252-a4aed5c0-9ccd-45c8-ac1d-ccc6f911d8c8.png)

![image](https://user-images.githubusercontent.com/17672596/142607302-2f63e975-b333-429d-b9f0-4f828caf7e19.png)


## 프론트엔드 실행 화면
![image](https://user-images.githubusercontent.com/17672596/142607326-21c86afe-8c5e-44b7-a62f-9728f64f4082.png)

![image](https://user-images.githubusercontent.com/17672596/142607340-75896bdd-f9f2-4dda-bc36-38c999a0303d.png)

