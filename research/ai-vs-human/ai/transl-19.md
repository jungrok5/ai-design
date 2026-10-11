# 텍스트 표시 방향 제어하기

> **참고:** 이 문서는 CSS 쓰기 방향(writing mode)과 양방향 텍스트(bidirectional text)를 다루는 방법을 설명합니다. 아랍어, 히브리어처럼 오른쪽에서 왼쪽으로 쓰는 언어나 일본어, 중국어, 몽골어처럼 세로로 쓰는 언어를 지원하는 웹 페이지를 만들 때 도움이 됩니다.

세상의 모든 언어가 왼쪽에서 오른쪽으로, 위에서 아래로 쓰이는 것은 아닙니다. 웹 콘텐츠를 여러 언어로 제공하려면 텍스트가 흐르는 방향을 올바르게 지정해야 합니다. 이 가이드에서는 HTML과 CSS에서 텍스트 방향을 제어하는 핵심 도구인 `dir` 속성, `direction`, `unicode-bidi`, `writing-mode`, `text-orientation` 속성과 논리적 속성(logical properties)을 소개합니다.

## 쓰기 방향의 기본 개념

텍스트 방향을 이해하려면 먼저 두 가지 개념을 구분해야 합니다.

- **인라인 방향(inline direction):** 한 줄 안에서 글자가 이어지는 방향입니다. 한국어, 영어는 왼쪽에서 오른쪽(LTR)이고, 아랍어와 히브리어는 오른쪽에서 왼쪽(RTL)입니다.
- **블록 방향(block direction):** 줄(또는 블록)이 쌓이는 방향입니다. 가로쓰기에서는 위에서 아래로, 전통적인 세로쓰기에서는 오른쪽에서 왼쪽 또는 왼쪽에서 오른쪽으로 쌓입니다.

CSS는 이 두 방향을 기준으로 레이아웃을 계산하므로, 물리적인 "왼쪽/오른쪽/위/아래" 대신 "시작/끝" 개념으로 생각하는 것이 좋습니다.

## HTML의 `dir` 속성

문서의 텍스트 방향을 지정하는 가장 기본적인 방법은 HTML의 `dir` 속성입니다. 이 속성은 다음 값을 가집니다.

- `ltr`: 왼쪽에서 오른쪽으로 표시합니다.
- `rtl`: 오른쪽에서 왼쪽으로 표시합니다.
- `auto`: 요소 안의 텍스트 내용을 보고 브라우저가 방향을 결정합니다.

```html
<html lang="ar" dir="rtl">
  <head>
    <meta charset="utf-8" />
    <title>مرحبا</title>
  </head>
  <body>
    <p>مرحبا بالعالم</p>
  </body>
</html>
```

가능하면 방향은 CSS 대신 HTML의 `dir` 속성으로 지정하는 것이 좋습니다. 방향은 문서의 의미(semantics)에 해당하는 정보이므로, CSS가 로드되지 않거나 비활성화된 환경에서도 올바르게 표시되어야 하기 때문입니다.

### 사용자 입력에는 `dir="auto"`

사용자가 직접 입력한 댓글이나 게시글처럼 어떤 언어로 작성될지 알 수 없는 콘텐츠에는 `dir="auto"`가 유용합니다. 브라우저는 요소 안에서 방향이 강한(strong) 첫 번째 문자를 찾아 전체 방향을 결정합니다.

```html
<ul>
  <li dir="auto">Hello, world!</li>
  <li dir="auto">שלום עולם</li>
</ul>
```

## CSS `direction` 속성

`direction` 속성은 인라인 방향을 지정합니다. 값으로 `ltr`과 `rtl`을 사용할 수 있습니다.

```css
.arabic {
  direction: rtl;
}
```

그러나 앞서 설명한 이유로 문서 콘텐츠의 방향은 `dir` 속성을 사용하길 권장합니다. `direction`은 주로 특별한 레이아웃 효과가 필요할 때, 예를 들어 스크롤바를 반대쪽에 배치하거나 테이블 열의 순서를 뒤집을 때 사용합니다.

## `unicode-bidi`와 양방향 텍스트

하나의 문장에 서로 다른 방향의 언어가 섞여 있으면 **양방향 텍스트(bidirectional text, bidi)** 문제가 생깁니다. 예를 들어 아랍어 문장 안에 영어 상표명이 들어가는 경우입니다. 브라우저는 유니코드 양방향 알고리즘(Unicode Bidirectional Algorithm)을 사용해 각 문자의 고유한 방향성에 따라 표시 순서를 결정합니다.

대부분의 경우 이 알고리즘이 올바르게 동작하지만, 숫자나 문장 부호처럼 방향이 약한(weak) 문자나 중립(neutral) 문자가 경계에 있을 때 의도와 다르게 표시될 수 있습니다. 이때 `unicode-bidi` 속성으로 동작을 조절합니다.

| 값 | 설명 |
| --- | --- |
| `normal` | 추가적인 임베딩을 만들지 않습니다(기본값). |
| `embed` | 요소 안에 새로운 임베딩 수준을 열고 `direction` 값을 따릅니다. |
| `isolate` | 주변 텍스트와 요소를 분리하여 서로 영향을 주지 않게 합니다. |
| `bidi-override` | 알고리즘을 무시하고 `direction` 값대로 강제로 표시합니다. |
| `isolate-override` | `isolate`와 `bidi-override`를 함께 적용합니다. |
| `plaintext` | 요소 내용에 따라 방향을 결정하며 주변과 분리합니다. |

HTML에서는 이러한 동작을 의미적으로 표현하는 `<bdi>`와 `<bdo>` 요소를 제공합니다.

```html
<p>사용자 <bdi>إيان</bdi>가 3개의 글을 작성했습니다.</p>
<p><bdo dir="rtl">이 문장은 거꾸로 표시됩니다.</bdo></p>
```

`<bdi>`는 `unicode-bidi: isolate`와 비슷하게 동작하여 내용이 주변 텍스트의 방향에 영향을 주지 않게 하고, `<bdo>`는 `bidi-override`와 같이 방향을 강제로 덮어씁니다.

## `writing-mode` 속성

`writing-mode` 속성은 텍스트 줄이 가로로 배치되는지 세로로 배치되는지, 그리고 블록이 쌓이는 방향을 지정합니다.

| 값 | 설명 |
| --- | --- |
| `horizontal-tb` | 가로쓰기. 줄은 위에서 아래로 쌓입니다(기본값). |
| `vertical-rl` | 세로쓰기. 줄은 오른쪽에서 왼쪽으로 쌓입니다. |
| `vertical-lr` | 세로쓰기. 줄은 왼쪽에서 오른쪽으로 쌓입니다. |
| `sideways-rl` | 글자를 옆으로 눕힌 세로 흐름. 줄은 오른쪽에서 왼쪽으로 쌓입니다. |
| `sideways-lr` | 글자를 옆으로 눕힌 세로 흐름. 줄은 왼쪽에서 오른쪽으로 쌓입니다. |

```css
.vertical {
  writing-mode: vertical-rl;
}
```

한국어, 일본어, 중국어의 전통적인 세로쓰기는 `vertical-rl`을 사용합니다. 몽골어의 전통 문자처럼 왼쪽에서 오른쪽으로 줄이 쌓이는 경우에는 `vertical-lr`이 적합합니다.

### 글자 방향 조절: `text-orientation`

세로쓰기 모드에서 개별 글자를 어떻게 회전시킬지는 `text-orientation` 속성이 결정합니다.

- `mixed`: 한자, 한글처럼 세로로 세워 쓰는 문자는 똑바로 두고, 알파벳 같은 가로쓰기 문자는 시계 방향으로 90도 회전합니다(기본값).
- `upright`: 모든 글자를 똑바로 세웁니다. 이때 `direction`은 `ltr`로 취급됩니다.
- `sideways`: 모든 글자를 시계 방향으로 90도 회전시켜 가로쓰기 문자처럼 표시합니다.

```css
.vertical-upright {
  writing-mode: vertical-rl;
  text-orientation: upright;
}
```

## 논리적 속성과 값

쓰기 방향이 바뀌면 `margin-left`, `padding-right`, `width`, `height` 같은 물리적 속성은 의도와 다른 결과를 낳을 수 있습니다. 예를 들어 RTL 문서에서 `margin-left`로 아이콘과 글자 사이를 띄웠다면 간격이 엉뚱한 쪽에 생깁니다.

논리적 속성은 쓰기 방향에 따라 자동으로 물리적 방향에 대응됩니다.

| 물리적 속성 | 논리적 속성 |
| --- | --- |
| `width` | `inline-size` |
| `height` | `block-size` |
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-top` | `padding-block-start` |
| `border-bottom` | `border-block-end` |
| `left` | `inset-inline-start` |

```css
.icon {
  margin-inline-end: 0.5rem;
}
```

위 코드는 LTR에서는 아이콘 오른쪽에, RTL에서는 아이콘 왼쪽에 여백을 만듭니다. 별도의 RTL 전용 스타일 없이도 양쪽 방향에서 올바르게 표시됩니다.

텍스트 정렬에도 `text-align: left` 대신 `text-align: start`를 사용하면 방향에 맞게 정렬됩니다. 또한 `float: inline-start`, `clear: inline-end`처럼 논리적 값을 지원하는 속성도 있습니다.

## 실전 팁

1. **`lang`과 `dir`을 함께 지정하세요.** `lang`은 발음, 글꼴 선택, 하이픈 처리에 영향을 주고, `dir`은 표시 방향을 결정합니다. 두 속성은 서로 대체할 수 없습니다.
2. **사용자 생성 콘텐츠는 격리하세요.** 이름이나 댓글을 삽입할 때 `<bdi>` 또는 `dir="auto"`를 사용하면 주변 텍스트의 순서가 흐트러지는 것을 막을 수 있습니다.
3. **물리적 속성보다 논리적 속성을 선호하세요.** 처음부터 논리적 속성으로 작성하면 나중에 다국어를 지원할 때 수정할 부분이 크게 줄어듭니다.
4. **아이콘의 방향을 점검하세요.** 뒤로 가기 화살표처럼 방향성이 있는 아이콘은 RTL에서 좌우를 반전해야 할 수 있습니다. 반면 시계나 체크 표시처럼 방향과 무관한 아이콘은 그대로 둡니다.
5. **Flexbox와 Grid는 자동으로 따라갑니다.** `flex-direction: row`는 문서 방향이 RTL이면 오른쪽에서 시작하므로 별도의 처리가 필요하지 않은 경우가 많습니다.

## 명세

- CSS Writing Modes Level 3 / Level 4
- CSS Logical Properties and Values Level 1
- HTML Living Standard (`dir` 속성, `<bdi>`, `<bdo>`)

## 같이 보기

- [`dir` 전역 속성](https://developer.mozilla.org/ko/docs/Web/HTML/Global_attributes/dir)
- [`direction`](https://developer.mozilla.org/ko/docs/Web/CSS/direction)
- [`unicode-bidi`](https://developer.mozilla.org/ko/docs/Web/CSS/unicode-bidi)
- [`writing-mode`](https://developer.mozilla.org/ko/docs/Web/CSS/writing-mode)
- [`text-orientation`](https://developer.mozilla.org/ko/docs/Web/CSS/text-orientation)
- [CSS 논리적 속성과 값](https://developer.mozilla.org/ko/docs/Web/CSS/CSS_logical_properties_and_values)
