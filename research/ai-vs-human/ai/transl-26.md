# 속성 선택자 (Attribute selectors)

속성 선택자(attribute selector)는 HTML 요소에 **지정된 속성이 있는지**, 또는 **속성 값이 특정 조건을 만족하는지**에 따라 요소를 선택하는 CSS 선택자입니다. 클래스나 아이디가 없는 요소도 `href`, `type`, `alt`, `data-*` 같은 속성을 기준으로 스타일을 줄 수 있어 활용도가 높습니다.

## 기본 문법

속성 선택자는 대괄호(`[ ]`) 안에 속성 이름과 선택적으로 비교 연산자, 값을 씁니다.

```css
[attr]               /* attr 속성이 있는 요소 */
[attr=value]         /* attr 값이 정확히 value인 요소 */
[attr~=value]        /* attr 값이 공백으로 구분된 목록에 value를 포함하는 요소 */
[attr|=value]        /* attr 값이 value이거나 value- 로 시작하는 요소 */
[attr^=value]        /* attr 값이 value로 시작하는 요소 */
[attr$=value]        /* attr 값이 value로 끝나는 요소 */
[attr*=value]        /* attr 값에 value 문자열이 포함된 요소 */
```

값에는 따옴표를 사용할 수 있습니다. 값이 식별자 형식(영문자, 숫자, 하이픈, 밑줄)만으로 이루어졌다면 따옴표를 생략해도 되지만, 공백이나 특수문자가 있으면 반드시 따옴표로 감싸야 합니다.

```css
input[type=text]     /* 따옴표 생략 가능 */
input[placeholder="이름을 입력하세요"]  /* 공백이 있으므로 따옴표 필수 */
```

## 속성 존재 여부 선택

값과 상관없이 속성이 있는지만 확인하려면 `[attr]` 형태를 사용합니다. 예를 들어 `target` 속성이 지정된 링크에만 아이콘을 붙이는 경우에 유용합니다.

```css
a[target] {
  padding-right: 1em;
}
```

## 값 비교 연산자 자세히 보기

### 정확히 일치: `[attr=value]`

속성 값 전체가 `value`와 같을 때만 선택합니다.

```css
input[type="checkbox"] {
  accent-color: #0a84ff;
}
```

### 단어 포함: `[attr~=value]`

속성 값이 공백으로 구분된 단어 목록일 때, 그중 하나가 `value`와 정확히 일치하면 선택합니다. `class` 속성을 다룰 때 `.classname`과 같은 효과를 내는 방식으로 이해하면 편합니다.

```html
<p data-tags="news urgent">긴급 뉴스</p>
<p data-tags="news">일반 뉴스</p>
```

```css
[data-tags~="urgent"] {
  color: red;   /* 첫 번째 문단만 적용 */
}
```

### 하이픈 접두: `[attr|=value]`

속성 값이 `value`와 같거나, `value-`로 시작할 때 선택합니다. 주로 언어 코드에 사용됩니다. 예를 들어 `en`, `en-US`, `en-GB`를 모두 선택할 수 있습니다.

```css
[lang|="en"] {
  font-family: Georgia, serif;
}
```

### 접두사 일치: `[attr^=value]`

속성 값이 `value`로 시작하는 요소를 선택합니다.

```css
a[href^="https://"] {
  color: green;   /* 보안 연결 링크 */
}

a[href^="mailto:"]::after {
  content: " ✉";
}
```

### 접미사 일치: `[attr$=value]`

속성 값이 `value`로 끝나는 요소를 선택합니다. 파일 확장자를 기준으로 스타일을 줄 때 자주 씁니다.

```css
a[href$=".pdf"]::before {
  content: "📄 ";
}
```

### 부분 문자열 일치: `[attr*=value]`

속성 값 어디에든 `value` 문자열이 포함되어 있으면 선택합니다.

```css
[class*="col-"] {
  box-sizing: border-box;   /* col-md-6, col-lg-4 등 모두 해당 */
}
```

`[attr^=value]`, `[attr$=value]`, `[attr*=value]`는 `value`가 빈 문자열이면 아무 요소도 선택하지 않습니다.

## 대소문자 구분: `i`와 `s` 플래그

HTML에서 속성 **이름**은 대소문자를 구분하지 않습니다. 속성 **값**은 기본적으로 대소문자를 구분하지만, HTML 명세상 대소문자를 구분하지 않는 속성(예: `type`)은 예외입니다.

값의 대소문자 처리를 직접 지정하려면 닫는 대괄호 앞에 플래그를 씁니다.

- `i`: 대소문자를 구분하지 않습니다(ASCII 문자 기준).
- `s`: 대소문자를 구분합니다.

```css
a[href$=".PDF" i] {
  color: crimson;   /* .pdf, .PDF, .Pdf 모두 선택 */
}
```

## 여러 조건 조합하기

속성 선택자는 요소 선택자, 클래스 선택자, 다른 속성 선택자와 자유롭게 결합할 수 있습니다. 조건을 붙일수록 선택 범위가 좁아집니다.

```css
input[type="email"][required] {
  border-left: 3px solid orange;
}

a[target="_blank"][rel~="noopener"] {
  font-style: italic;
}
```

`:not()`, `:is()` 같은 가상 클래스 안에서도 사용할 수 있습니다.

```css
a:not([href^="https://"]) {
  color: gray;   /* 보안 연결이 아닌 링크 */
}
```

## 실전 예제: 폼 요소 상태 표시

```html
<form>
  <input type="text" name="name" required>
  <input type="email" name="email" required>
  <input type="text" name="nickname">
</form>
```

```css
/* 필수 입력란 표시 */
input[required] {
  background-color: #fff8e1;
}

/* 이메일 입력란만 다른 스타일 */
input[type="email"] {
  font-family: monospace;
}

/* name 속성이 "email"로 끝나는 모든 입력란 */
input[name$="email"] {
  border-color: #0a84ff;
}
```

## 데이터 속성과 함께 사용하기

`data-*` 속성은 자바스크립트와 CSS 모두에서 상태를 표현하는 데 유용합니다. 속성 선택자를 쓰면 클래스를 바꾸지 않고도 상태에 따라 스타일을 적용할 수 있습니다.

```html
<button data-state="loading">저장 중</button>
<button data-state="done">완료</button>
```

```css
button[data-state="loading"] {
  opacity: 0.6;
  cursor: wait;
}

button[data-state="done"] {
  background-color: #34c759;
  color: white;
}
```

## 명시도(Specificity)

속성 선택자는 클래스 선택자와 같은 수준인 **(0, 1, 0)** 명시도를 가집니다. 따라서 `a[href]`는 `a`보다 높고, `.link`와 같은 수준입니다. 명시도가 같으면 나중에 선언된 규칙이 적용되므로 스타일 충돌을 예측할 때 이를 고려해야 합니다.

## 주의할 점

1. **성능**: 속성 선택자는 일반적으로 빠르지만, `*=`와 같이 광범위하게 매칭하는 선택자를 많이 쓰면 불필요한 요소까지 선택될 수 있습니다. 가능하면 구체적인 조건을 사용하세요.
2. **의도치 않은 매칭**: `[class*="btn"]`은 `btn`, `btn-primary`뿐 아니라 `mybtnwrapper`도 선택합니다. 단어 단위로 맞추려면 `[class~="btn"]`을 고려하세요.
3. **따옴표 습관**: 값에 공백이나 특수문자가 없더라도 따옴표를 붙이면 실수를 줄일 수 있습니다.
4. **XML과 SVG**: 네임스페이스가 있는 속성은 `[xlink|href]`처럼 네임스페이스 접두사를 함께 써야 합니다.

## 브라우저 지원

`[attr]`, `[attr=value]`, `[attr~=value]`, `[attr|=value]`, `[attr^=value]`, `[attr$=value]`, `[attr*=value]`의 기본 형태는 CSS2.1 이상에서 정의되어 현재 주요 브라우저 모두 지원합니다. 값의 대소문자를 지정하는 `i`와 `s` 플래그는 CSS 선택자 레벨 4에서 정의되었으며, 최신 Chrome, Firefox, Safari, Edge에서 지원합니다. 오래된 브라우저를 고려해야 한다면 플래그 사용 전에 지원 여부를 확인하세요.

## 관련 문서

- 선택자(CSS 선택자 개요)
- 가상 클래스와 가상 요소
- 명시도(Specificity)
- `:is()`, `:not()`, `:where()`
- HTML 데이터 속성 (`data-*`)
