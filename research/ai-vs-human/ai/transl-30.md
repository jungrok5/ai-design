---
title: "Django 튜토리얼 파트 10: Django 웹 어플리케이션 테스트하기"
slug: Learn/Server-side/Django/Testing
---

{{LearnSidebar}}{{PreviousMenuNext("Learn/Server-side/Django/Forms", "Learn/Server-side/Django/Deployment", "Learn/Server-side/Django")}}

웹사이트가 커질수록 직접 테스트하기는 어려워집니다. 테스트할 것이 많아질 뿐 아니라 컴포넌트 사이의 상호작용도 복잡해지기 때문입니다. 한 곳을 조금 바꾸면 다른 곳에 영향이 갈 수 있으므로, 모든 것이 계속 제대로 동작하는지 확인하려면 더 많이 바꾸고 더 많이 테스트해야 합니다. 이 문제를 줄이는 방법 중 하나가 자동화된 테스트입니다. 자동화된 테스트는 코드를 바꿀 때마다 쉽고 확실하게 실행할 수 있습니다. 이 튜토리얼에서는 Django의 테스트 프레임워크로 웹사이트 _단위 테스트(unit test)_ 를 자동화하는 방법을 알아봅니다.

<table>
  <tbody>
    <tr>
      <th scope="row">전제 조건:</th>
      <td>
        <a href="/ko/docs/Learn/Server-side/Django/Forms">Django 튜토리얼 파트 9: 폼 작업하기</a>까지 포함해 앞의 튜토리얼을 모두 마칩니다.
      </td>
    </tr>
    <tr>
      <th scope="row">목표:</th>
      <td>Django 기반 웹사이트의 단위 테스트를 작성하는 방법을 이해합니다.</td>
    </tr>
  </tbody>
</table>

## 개요

[LocalLibrary](/ko/docs/Learn/Server-side/Django/Tutorial_local_library_website)에는 지금 도서, 저자 목록과 상세 정보를 보여 주는 페이지, `BookInstance`를 대여하고 갱신하는 페이지, `Author`를 만들고 수정하고 삭제하는 페이지가 있습니다. 사이트가 이 정도 크기만 되어도 모든 페이지를 직접 확인하는 데 몇 분이 걸립니다. 그리고 코드를 바꿀 때마다 이 확인을 반복해야 합니다.

자동화된 테스트를 쓰면 다음과 같은 점이 좋습니다.

- 코드가 의도대로 동작하는지 빠르게 확인할 수 있습니다.
- 리팩터링하거나 기능을 추가할 때 생긴 _회귀(regression)_ 를 찾아낼 수 있습니다.
- 테스트는 코드가 어떻게 동작해야 하는지 보여 주는 문서 역할도 합니다.

### 테스트의 종류

- **단위 테스트(Unit test)**: 개별 컴포넌트가 제대로 동작하는지 함수와 메서드 수준에서 확인합니다.
- **회귀 테스트(Regression test)**: 예전에 고친 버그가 다시 생기지 않는지 확인합니다.
- **통합 테스트(Integration test)**: 여러 컴포넌트를 함께 묶었을 때 제대로 동작하는지 확인합니다.

> [!NOTE]
> 이 밖에도 블랙박스 테스트, 화이트박스 테스트, 수동 테스트, 부하 테스트 등 여러 종류가 있습니다. 더 알고 싶다면 따로 검색해 보세요.

### Django의 테스트 도구

Django는 파이썬 표준 라이브러리 [`unittest`](https://docs.python.org/3/library/unittest.html#module-unittest)를 기반으로 테스트 프레임워크를 제공합니다. 테스트 클래스는 보통 `django.test.TestCase`를 상속합니다. 이 클래스는 테스트마다 깨끗한 데이터베이스를 준비해 주고, 테스트 _클라이언트_ 로 GET·POST 요청을 흉내 내어 응답을 검사할 수 있게 해 줍니다.

```python
from django.test import TestCase

class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 클래스 전체에서 한 번만 실행되며, 수정하지 않을 데이터를 준비합니다.
        pass

    def setUp(self):
        # 각 테스트 메서드가 실행되기 전마다 실행됩니다.
        pass

    def test_one_plus_one_equals_two(self):
        self.assertEqual(1 + 1, 2)
```

테스트 메서드의 이름은 반드시 `test`로 시작해야 하며, `assertTrue`, `assertEqual`, `assertFalse` 같은 단언(assert) 메서드로 결과를 확인합니다.

## 무엇을 테스트해야 할까?

파이썬이나 Django가 제공하는 기능은 테스트할 필요가 없습니다. _여러분이 작성한 코드_ 만 테스트하면 됩니다. 예를 들어 `CharField`가 실제로 문자열을 저장하는지 확인할 필요는 없지만, 필드의 `label`과 `max_length`가 설계대로 설정됐는지, 직접 만든 메서드가 올바른 값을 돌려주는지는 확인해야 합니다.

## 테스트 구조

Django는 이름이 `test*.py` 패턴과 일치하는 파일에서 테스트를 찾습니다. 다음처럼 `catalog/tests/` 폴더를 만들어 파일을 나누는 것이 좋습니다.

```plain
catalog/
  /tests/
    __init__.py
    test_models.py
    test_forms.py
    test_views.py
```

`__init__.py`는 빈 파일로 만들고, 기존 `catalog/tests.py`는 지웁니다.

## 테스트 실행하기

다음 명령으로 모든 테스트를 실행합니다.

```bash
python3 manage.py test
```

특정 모듈이나 클래스만 실행할 수도 있습니다.

```bash
python3 manage.py test catalog.tests.test_models
python3 manage.py test catalog.tests.test_models.AuthorModelTest
```

`--verbosity 2` 옵션을 주면 더 자세한 결과를 볼 수 있고, `--parallel auto`를 쓰면 테스트를 병렬로 실행합니다.

> [!WARNING]
> 정적 파일 관련 오류가 생기면 먼저 `python3 manage.py collectstatic`을 실행하세요.

## 모델 테스트

`Author` 모델에서 필드 라벨, 최대 길이, 사용자 정의 메서드를 확인해 봅시다. **/catalog/tests/test_models.py**:

```python
from django.test import TestCase
from catalog.models import Author

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')
```

`verbose_name`은 `author.first_name.verbose_name`처럼 바로 읽을 수 없습니다. `author.first_name`은 필드 객체가 아니라 문자열 값이기 때문입니다. 그래서 `_meta.get_field()`로 필드 객체를 가져와야 합니다.

## 폼 테스트

`RenewBookForm`이 날짜를 올바르게 검증하는지 확인합니다. **/catalog/tests/test_forms.py**:

```python
import datetime
from django.test import TestCase
from django.utils import timezone
from catalog.forms import RenewBookForm

class RenewBookFormTest(TestCase):
    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
```

검증 범위의 _경계값_ (오늘, 정확히 4주 뒤)과 범위를 벗어난 값을 함께 테스트한다는 점을 눈여겨보세요.

## 뷰 테스트

뷰는 테스트 클라이언트 `self.client`로 테스트합니다. 이 클라이언트는 가상의 웹 브라우저처럼 URL에 요청을 보내고 응답을 받아 옵니다. **/catalog/tests/test_views.py**:

```python
from django.test import TestCase
from django.urls import reverse
from catalog.models import Author

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 페이지네이션 테스트용으로 저자 13명을 만듭니다.
        for author_id in range(13):
            Author.objects.create(
                first_name=f'Dominique {author_id}',
                last_name=f'Surname {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['author_list']), 10)

    def test_lists_all_authors(self):
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(len(response.context['author_list']), 3)
```

### 로그인이 필요한 뷰

로그인한 사용자만 접근할 수 있는 뷰는 테스트 사용자를 만들고 `self.client.login()`으로 로그인한 다음 테스트합니다.

```python
def test_redirect_if_not_logged_in(self):
    response = self.client.get(reverse('my-borrowed'))
    self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')

def test_logged_in_uses_correct_template(self):
    self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
    response = self.client.get(reverse('my-borrowed'))
    self.assertEqual(str(response.context['user']), 'testuser1')
    self.assertEqual(response.status_code, 200)
```

폼을 처리하는 뷰라면 `self.client.post()`로 데이터를 보낸 뒤 리디렉션 여부(`assertRedirects`)나 폼 오류(`assertFormError`)를 확인할 수 있습니다.

## 과제

`BookInstance`, `Book`, `Genre` 모델과 `AuthorCreate` 뷰에 대한 테스트를 직접 작성해 보세요. 권한이 없는 사용자는 리디렉션되는지, 권한이 있는 사용자는 폼을 볼 수 있는지, 데이터를 제출하면 올바른 페이지로 이동하는지 확인하면 됩니다.

## 요약

테스트 코드를 작성하는 일이 재미있지는 않습니다. 그래서 사이트를 만들 때 맨 마지막으로 미루거나 아예 건너뛰는 경우가 많습니다. 하지만 테스트는 코드를 바꾼 뒤에도 안전하게 출시할 수 있게 해 주는 중요한 도구입니다. 이 튜토리얼에서는 모델, 폼, 뷰를 테스트하는 방법을 배웠습니다. 다음 글에서는 완성한 LocalLibrary 웹사이트를 프로덕션 환경에 배포하는 방법을 알아봅니다.

## 같이 보기

- [Writing and running tests](https://docs.djangoproject.com/en/stable/topics/testing/overview/) (Django 문서)
- [Writing your first Django app, part 5 > Introducing automated testing](https://docs.djangoproject.com/en/stable/intro/tutorial05/) (Django 문서)
- [Testing tools reference](https://docs.djangoproject.com/en/stable/topics/testing/tools/) (Django 문서)
- [Advanced testing topics](https://docs.djangoproject.com/en/stable/topics/testing/advanced/) (Django 문서)

{{PreviousMenuNext("Learn/Server-side/Django/Forms", "Learn/Server-side/Django/Deployment", "Learn/Server-side/Django")}}
