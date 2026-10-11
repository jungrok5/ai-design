---
title: "장고 튜토리얼 강좌 2: 뼈대 사이트 만들기"
slug: Learn/Server-side/Django/skeleton_website
---

{{LearnSidebar}}

{{PreviousMenuNext("Learn/Server-side/Django/Tutorial_local_library_website", "Learn/Server-side/Django/Models", "Learn/Server-side/Django")}}

이 글은 [장고 튜토리얼](/ko/docs/Learn/Server-side/Django/Tutorial_local_library_website)의 두 번째 강좌입니다. 여기서는 "뼈대(skeleton)" 웹사이트 프로젝트를 만듭니다. 뼈대 사이트를 만든 뒤에는 사이트 설정, URL 경로, 모델, 뷰, 템플릿을 차례로 채워 나갑니다.

<table>
  <tbody>
    <tr>
      <th scope="row">사전 지식:</th>
      <td>
        <a href="/ko/docs/Learn/Server-side/Django/development_environment">장고 개발 환경 설정하기</a>,
        <a href="/ko/docs/Learn/Server-side/Django/Tutorial_local_library_website">장고 튜토리얼 1: 지역 도서관 웹사이트</a>를 읽으세요.
      </td>
    </tr>
    <tr>
      <th scope="row">목표:</th>
      <td>장고 도구를 사용해 새 웹사이트 프로젝트를 시작할 수 있습니다.</td>
    </tr>
  </tbody>
</table>

## 개요

이 글에서는 "뼈대" 웹사이트를 만드는 방법을 보여 줍니다. 여기에 사이트별 설정, 경로, 모델, 뷰, 템플릿을 채워 넣게 됩니다. 순서는 다음과 같습니다.

1. `django-admin` 도구로 프로젝트 폴더, 기본 템플릿 파일, 프로젝트 관리 스크립트(**manage.py**)를 만듭니다.
2. **manage.py**로 하나 이상의 _애플리케이션_ 을 만듭니다.

   > [!NOTE]
   > 웹사이트는 하나 이상의 섹션으로 이루어질 수 있습니다. 예를 들어 메인 사이트, 블로그, 위키, 다운로드 영역 등이 있습니다. 장고에서는 이런 구성 요소를 _애플리케이션_ 으로 나누어 개발하는 방식을 권장합니다. 이렇게 나눈 애플리케이션은 다른 프로젝트에서도 다시 사용할 수 있습니다.

3. 새 애플리케이션을 프로젝트에 등록합니다.
4. 각 애플리케이션의 URL을 연결(map)합니다.

[지역 도서관 웹사이트](/ko/docs/Learn/Server-side/Django/Tutorial_local_library_website)에서는 웹사이트 폴더와 프로젝트 폴더의 이름을 모두 _locallibrary_ 로 정합니다. 애플리케이션은 _catalog_ 하나만 만듭니다. 최종 폴더 구조는 다음과 같습니다.

```plain
locallibrary/         # 웹사이트 폴더
    manage.py         # 장고 도구를 실행하는 스크립트(django-admin이 생성)
    locallibrary/     # 웹사이트/프로젝트 폴더(django-admin이 생성)
    catalog/          # 애플리케이션 폴더(manage.py가 생성)
```

이제 단계별로 살펴보겠습니다.

## 프로젝트 만들기

먼저 명령 프롬프트나 터미널을 열고, [가상 환경](/ko/docs/Learn/Server-side/Django/development_environment#using_a_virtual_environment)이 활성화되어 있는지 확인합니다. 그다음 장고 앱을 저장할 위치로 이동해 아래와 같이 새 프로젝트를 만듭니다.

```bash
mkdir django_projects
cd django_projects
django-admin startproject locallibrary
cd locallibrary
```

`django-admin` 도구는 다음과 같은 폴더 구조를 만듭니다.

```plain
locallibrary/
    manage.py
    locallibrary/
        __init__.py
        settings.py
        urls.py
        wsgi.py
        asgi.py
```

_locallibrary_ 프로젝트 하위 폴더는 웹사이트의 시작점이며, 다음 파일을 담고 있습니다.

- **\_\_init\_\_.py**: 이 폴더를 파이썬 패키지로 취급하라고 알려 주는 빈 파일입니다.
- **settings.py**: 웹사이트의 모든 설정을 담고 있습니다. 애플리케이션을 등록하고, 정적 파일의 위치와 데이터베이스 설정 등을 지정하는 곳입니다.
- **urls.py**: 사이트의 URL과 뷰를 연결합니다. 모든 URL 매핑을 여기에 둘 수도 있지만, 보통은 일부를 각 애플리케이션에 위임합니다.
- **wsgi.py**: 장고 애플리케이션이 웹 서버와 통신할 수 있게 해 줍니다. 이 파일은 그대로 사용하면 됩니다.
- **asgi.py**: 비동기 웹 서버와 애플리케이션이 통신하기 위한 표준입니다.

**manage.py** 스크립트는 애플리케이션을 만들고, 데이터베이스를 다루고, 개발용 웹 서버를 실행할 때 사용합니다.

## catalog 애플리케이션 만들기

다음으로 아래 명령을 실행해 _catalog_ 애플리케이션을 만듭니다. 이 명령은 반드시 **manage.py**가 있는 폴더에서 실행해야 합니다.

```bash
# Linux/macOS
python3 manage.py startapp catalog

# Windows
py manage.py startapp catalog
```

이 명령은 새 폴더를 만들고 여러 파일을 채워 넣습니다. 각 파일의 이름은 용도를 나타냅니다. 예를 들어 모델은 **models.py**에, 뷰는 **views.py**에, 테스트는 **tests.py**에 작성합니다. 관리자 사이트 설정은 **admin.py**, 애플리케이션 등록 정보는 **apps.py**에 둡니다. **migrations** 폴더에는 모델을 수정할 때 데이터베이스를 자동으로 업데이트하는 "마이그레이션" 파일이 저장됩니다.

> [!NOTE]
> URL, 템플릿, 정적 파일을 위한 파일이나 폴더는 만들어지지 않습니다. 필요할 때 직접 만들어야 합니다.

## catalog 애플리케이션 등록하기

애플리케이션을 만들었으면 프로젝트에 등록해야 합니다. 그래야 여러 도구가 실행될 때 이 애플리케이션을 포함합니다. **locallibrary/locallibrary/settings.py** 파일을 열어 `INSTALLED_APPS` 목록 끝에 다음 줄을 추가합니다.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 아래 줄을 추가합니다
    'catalog.apps.CatalogConfig',
]
```

새로 추가한 줄은 애플리케이션 설정 객체(`CatalogConfig`)를 가리킵니다. 이 객체는 애플리케이션을 만들 때 **/catalog/apps.py**에 자동으로 생성됩니다.

## 데이터베이스와 기타 설정

**settings.py**에는 데이터베이스 설정도 들어 있습니다. 개발 단계에서는 기본값인 SQLite를 그대로 사용해도 됩니다.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

`TIME_ZONE`은 표준 [tz 데이터베이스 시간대](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) 이름으로 바꿔 주세요. 예를 들어 한국에서는 `'Asia/Seoul'`을 씁니다. 그 밖에 알아 둘 설정은 다음과 같습니다.

- `SECRET_KEY`: 보안에 쓰이는 비밀 키입니다. 개발 중에는 그대로 두어도 되지만, 운영 환경에서는 소스 코드 밖에서 불러와야 합니다.
- `DEBUG`: `True`이면 오류가 났을 때 상세한 디버그 정보를 보여 줍니다. 운영 환경에서는 반드시 `False`로 바꿉니다.

## URL 매퍼 연결하기

웹사이트 폴더의 **urls.py**에는 기본적으로 관리자 사이트 경로만 들어 있습니다. 여기에 catalog 애플리케이션으로 요청을 넘기는 경로, 루트 URL을 `catalog/`로 보내는 리디렉션, 개발 중에 정적 파일을 제공하는 설정을 추가합니다.

```python
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='catalog/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

`include()`는 `catalog/`로 시작하는 요청을 **catalog/urls.py** 모듈에 넘깁니다. 이 파일은 아직 없으므로 직접 만들어 둡니다.

```python
# catalog/urls.py
from django.urls import path
from . import views

urlpatterns = [

]
```

## 웹사이트 테스트하기

이제 뼈대 프로젝트가 완성되었습니다. 아직 페이지는 없지만, 서버를 실행해 오류가 없는지 확인해 보겠습니다.

### 데이터베이스 마이그레이션 실행하기

장고는 객체 관계 매퍼(ORM)를 사용해 모델 정의를 데이터베이스 테이블로 바꿉니다. 아래 명령으로 데이터베이스를 처음 생성합니다.

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

> [!WARNING]
> 모델이 바뀌어 데이터 구조에 영향을 줄 때마다 위 명령을 다시 실행해야 합니다. 바뀌는 필드나 클래스 추가·삭제도 여기에 포함됩니다.

`makemigrations`는 설치된 애플리케이션의 마이그레이션 파일을 _만들기만_ 하고 적용하지는 않습니다. 실제로 데이터베이스에 적용하는 명령은 `migrate`입니다.

### 웹사이트 실행하기

개발 중에는 장고의 개발용 웹 서버로 웹사이트를 확인할 수 있습니다.

```bash
python3 manage.py runserver
```

서버가 실행되면 브라우저에서 `http://127.0.0.1:8000/`을 열어 보세요. `/catalog/`로 리디렉션된 뒤 "Page not found" 오류 페이지가 나타납니다. catalog 애플리케이션에 아직 페이지나 URL이 정의되지 않았기 때문입니다. 지금 단계에서는 이 결과가 정상입니다.

## 스스로 해 보기

**catalog/** 폴더에는 뷰, 모델 등을 위한 파일이 이미 있습니다. 각 파일을 열어 내용을 살펴보세요. 앞서 본 것처럼 관리자 사이트 경로는 프로젝트의 **urls.py**에 이미 추가되어 있습니다. 브라우저에서 관리자 영역에 접속해 어떤 화면이 나오는지 확인해 보세요.

## 요약

이제 뼈대 웹사이트 프로젝트를 완성했습니다. 다음 강좌부터는 URL, 모델, 뷰, 템플릿을 추가해 지역 도서관 웹사이트를 만들어 나갑니다.

## 같이 보기

- [첫 번째 장고 앱 작성하기 - 1부](https://docs.djangoproject.com/en/stable/intro/tutorial01/) (장고 공식 문서)
- [애플리케이션](https://docs.djangoproject.com/en/stable/ref/applications/#configuring-applications) (장고 공식 문서)

{{PreviousMenuNext("Learn/Server-side/Django/Tutorial_local_library_website", "Learn/Server-side/Django/Models", "Learn/Server-side/Django")}}
