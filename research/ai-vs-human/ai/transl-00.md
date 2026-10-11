```markdown
---
title: "Django 튜토리얼 파트 11: Django 웹사이트 공개하기"
slug: Learn_web_development/Extensions/Server-side/Django/Deployment
---

{{LearnSidebar}}

{{PreviousMenuNext("Learn_web_development/Extensions/Server-side/Django/Testing", "Learn_web_development/Extensions/Server-side/Django/web_application_security", "Learn_web_development/Extensions/Server-side/Django")}}

지금까지 [LocalLibrary](/ko/docs/Learn_web_development/Extensions/Server-side/Django/Tutorial_local_library_website) 웹사이트를 만들고 테스트했습니다. 이제 도서관 직원과 회원이 인터넷으로 사이트에 접속할 수 있도록 공개 웹 서버에 올릴 차례입니다. 이 문서에서는 웹사이트를 배포할 호스트를 찾는 방법과, 사이트를 프로덕션 환경에 맞게 준비하는 데 필요한 작업을 개략적으로 설명합니다.

<table class="standard-table">
  <tbody>
    <tr>
      <th scope="row">전제 조건:</th>
      <td>
        이 튜토리얼의
        <a href="/ko/docs/Learn_web_development/Extensions/Server-side/Django/Testing">Django 튜토리얼 파트 10: Django 웹 애플리케이션 테스트하기</a>까지 마치기.
      </td>
    </tr>
    <tr>
      <th scope="row">목표:</th>
      <td>
        Django 앱을 프로덕션 환경에 어디에, 어떻게 배포할 수 있는지 알아보기.
      </td>
    </tr>
  </tbody>
</table>

## 개요

웹사이트가 완성되었거나 공개 테스트를 시작할 만큼 진행되었다면, 개인 개발 컴퓨터보다 더 공개적이고 접근하기 쉬운 곳에 사이트를 올려야 합니다.

지금까지는 개발 환경에서 작업했습니다. Django 개발용 웹 서버로 사이트를 로컬 브라우저와 네트워크에만 공유했고, 디버그 로그와 상세 오류 메시지가 켜진 (안전하지 않은) 개발 설정으로 실행했습니다. 사이트를 외부에 공개하려면 다음 작업을 해야 합니다.

- 프로젝트 설정 중 일부를 변경합니다.
- Django 앱을 호스팅할 환경을 선택합니다.
- 정적 파일을 호스팅할 환경을 선택합니다.
- 웹사이트를 제공할 프로덕션 수준의 인프라를 구성합니다.

이 튜토리얼에서는 호스팅 환경을 고르는 데 도움이 되는 정보를 알아보고, Django 앱을 프로덕션에 올리기 위해 해야 할 일을 간단히 정리한 다음, LocalLibrary 웹사이트를 [Railway](https://railway.com/) 클라우드 호스팅 서비스에 설치하는 방법을 살펴봅니다.

## 프로덕션 환경이란?

프로덕션 환경은 외부에서 사용할 수 있도록 웹사이트를 실행하는 서버 컴퓨터가 제공하는 환경입니다. 이 환경에는 다음이 포함됩니다.

- 웹사이트를 실행하는 컴퓨터 하드웨어
- 운영 체제(예: Linux, Windows)
- 프로그래밍 언어 런타임과 웹사이트를 작성하는 데 사용한 프레임워크 라이브러리
- 페이지와 기타 콘텐츠를 제공하는 웹 서버 인프라(예: Nginx, Apache)
- Django 웹사이트와 웹 서버 사이에서 동적 요청을 전달하는 애플리케이션 서버
- 웹사이트가 의존하는 데이터베이스

> [!NOTE]
> 프로덕션 환경을 어떻게 구성하느냐에 따라 리버스 프록시, 로드 밸런서 등이 추가로 필요할 수도 있습니다.

서버 컴퓨터는 직접 소유하고 빠른 인터넷 회선으로 연결해 운영할 수도 있지만, "클라우드"에 호스팅된 컴퓨터를 사용하는 것이 훨씬 일반적입니다. 이런 원격 컴퓨팅 하드웨어를 흔히 *IaaS(Infrastructure as a Service)* 라고 부릅니다. 반면 운영 체제, 웹 서버, 런타임까지 관리해 주어 애플리케이션 코드에만 집중할 수 있게 해 주는 서비스를 *PaaS(Platform as a Service)* 라고 합니다. PaaS는 확장성이 뛰어나고 설정할 것이 적어 처음 배포할 때 특히 편리합니다.

## 호스팅 제공자 선택하기

Django를 지원하는 호스팅 제공자는 많습니다. 제공자를 고를 때는 다음 사항을 고려하세요.

- 사이트가 얼마나 바쁠지, 그리고 그 수요를 감당하는 데 드는 데이터 및 컴퓨팅 자원의 비용
- 수평(머신 추가) 및 수직(더 강력한 머신으로 업그레이드) 확장 지원 수준과 그 비용
- 데이터 센터의 위치(가장 빠르게 접속할 수 있는 위치)
- 과거 가동 시간 및 다운타임 성능
- 사이트 관리를 위한 도구가 사용하기 쉽고 안전한지(예: SSH 대 FTP)
- 서버 모니터링을 위한 내장 프레임워크
- 알려진 제약 사항(예: 특정 서비스를 일부러 중단하거나, 일정 시간 동안 요청이 없으면 앱을 잠재우는 경우)
- 확장할 때 드는 비용과 무료 체험 기간 이후의 요금

학습 단계에서는 무료 또는 저렴한 요금제가 있는 서비스로 시작하고, 사이트가 성장하면 더 비싼 요금제로 옮기는 것이 좋습니다.

## 웹사이트를 공개할 준비하기

`django-admin`과 `manage.py`로 만든 [Django 프로젝트 골격](/ko/docs/Learn_web_development/Extensions/Server-side/Django/skeleton_website)은 개발을 쉽게 하도록 구성되어 있습니다. 보안이나 성능 때문에 많은 Django 설정(**settings.py**에 지정된 값)은 프로덕션 환경에서 다르게 지정해야 합니다.

> [!NOTE]
> 개발 환경과 프로덕션 환경에 서로 다른 설정 파일을 두는 경우가 흔합니다. 이 튜토리얼에서는 같은 **settings.py** 파일을 사용하되, 민감한 값은 환경 변수에서 읽어 오도록 바꿉니다.

반드시 확인해야 할 핵심 설정은 다음과 같습니다.

- `DEBUG`: 프로덕션에서는 `False`로 설정해야 합니다(`DEBUG = False`). 그래야 민감하고 기밀인 디버그 추적 정보와 변수 정보가 표시되지 않습니다.
- `SECRET_KEY`: CSRF 보호 등에 사용되는 큰 무작위 값입니다. 프로덕션에서 쓰는 키를 소스 코드 저장소에 넣거나 프로덕션 서버 밖에서 접근할 수 있게 두어서는 안 됩니다.
- `ALLOWED_HOSTS`: 사이트가 응답할 호스트/도메인 이름 목록입니다.
- `CSRF_TRUSTED_ORIGINS`: HTTPS로 안전하지 않은 요청(예: POST)을 보낼 수 있는 신뢰할 수 있는 출처 목록입니다.

`SECRET_KEY`와 `DEBUG`를 환경 변수에서 읽도록 **settings.py**를 다음과 같이 수정합니다.

```python
import os

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-개발용으로만-쓰는-키",
)

# DJANGO_DEBUG 환경 변수가 'False'이면 디버그 모드를 끕니다
DEBUG = os.environ.get("DJANGO_DEBUG", "") != "False"
```

Django는 배포 전에 설정을 점검할 수 있는 명령도 제공합니다. 다음 명령을 실행해 경고를 확인하세요.

```bash
python3 manage.py check --deploy
```

### 데이터베이스 구성

개발 중에는 SQLite를 사용했지만, 많은 호스팅 서비스는 파일 시스템을 영구적으로 보존하지 않으므로 PostgreSQL 같은 별도의 데이터베이스 서버를 사용하는 것이 좋습니다. [dj-database-url](https://pypi.org/project/dj-database-url/) 패키지를 쓰면 `DATABASE_URL` 환경 변수에서 데이터베이스 설정을 읽어 올 수 있습니다.

```bash
pip3 install dj-database-url psycopg2-binary
```

```python
import dj_database_url

if "DATABASE_URL" in os.environ:
    DATABASES["default"] = dj_database_url.config(
        conn_max_age=500,
        conn_health_checks=True,
    )
```

### 정적 파일 제공하기

개발 서버는 정적 파일(CSS, JavaScript, 이미지)을 자동으로 제공하지만 프로덕션에서는 그렇지 않습니다. `collectstatic` 명령으로 모든 정적 파일을 한곳에 모은 뒤, [WhiteNoise](https://pypi.org/project/whitenoise/)를 사용해 Django 앱에서 직접 효율적으로 제공할 수 있습니다.

```bash
pip3 install whitenoise
```

```python
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # SecurityMiddleware 바로 다음
    # …
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

> [!NOTE]
> `STORAGES`를 지정할 때 기본 파일 저장소를 쓰려면 `"default"` 키(`"django.core.files.storage.FileSystemStorage"`)도 함께 정의해야 합니다.

### 애플리케이션 서버와 의존성

Django 개발 서버는 프로덕션용이 아닙니다. 대신 [Gunicorn](https://gunicorn.org/) 같은 WSGI 애플리케이션 서버를 사용합니다.

```bash
pip3 install gunicorn
```

호스팅 서비스가 설치할 패키지를 알 수 있도록 저장소 루트에 **requirements.txt** 파일을 만듭니다.

```bash
pip3 freeze > requirements.txt
```

마지막으로 많은 PaaS 서비스는 **Procfile**을 읽어 앱을 어떻게 시작할지 결정합니다.

```plain
web: python manage.py migrate && python manage.py collectstatic --no-input && gunicorn locallibrary.wsgi
```

## 예시: Railway에 LocalLibrary 배포하기

준비가 끝나면 다음 순서로 사이트를 배포할 수 있습니다.

1. 프로젝트를 GitHub 저장소에 커밋하고 푸시합니다.
2. Railway에 로그인한 뒤 **New Project**를 선택하고 GitHub 저장소에서 배포하도록 지정합니다.
3. 같은 프로젝트에 PostgreSQL 데이터베이스를 추가하고, 앱 서비스의 `DATABASE_URL` 변수가 이 데이터베이스를 참조하도록 설정합니다.
4. `DJANGO_SECRET_KEY`와 `DJANGO_DEBUG=False` 환경 변수를 추가합니다.
5. 생성된 도메인을 `ALLOWED_HOSTS`와 `CSRF_TRUSTED_ORIGINS`에 추가한 후 다시 배포합니다.

배포가 완료되면 Railway CLI 등을 사용해 관리자 계정을 만듭니다(`python manage.py createsuperuser`). 이제 브라우저에서 생성된 URL로 접속하면 LocalLibrary 사이트를 확인할 수 있습니다.

## 요약

Django 웹사이트를 프로덕션 환경에 배포하는 튜토리얼과 Django 튜토리얼 시리즈를 모두 마쳤습니다. 이번 글에서는 호스팅 제공자를 고르는 기준을 살펴보고, 보안 설정, 데이터베이스, 정적 파일, 애플리케이션 서버를 프로덕션에 맞게 구성한 뒤 실제 PaaS에 사이트를 배포했습니다. 다음 단계로 웹 애플리케이션 보안에 관한 글을 읽어 보세요.

## 같이 보기

- [Django 배포 체크리스트](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/) (Django 문서)
- [WSGI로 배포하는 방법](https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/) (Django 문서)
- [정적 파일 배포하기](https://docs.djangoproject.com/en/stable/howto/static-files/deployment/) (Django 문서)
- [WhiteNoise 문서](https://whitenoise.readthedocs.io/en/stable/django.html)

{{PreviousMenuNext("Learn_web_development/Extensions/Server-side/Django/Testing", "Learn_web_development/Extensions/Server-side/Django/web_application_security", "Learn_web_development/Extensions/Server-side/Django")}}
```
