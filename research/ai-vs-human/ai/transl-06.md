---
title: 접근성
slug: Web/Accessibility
page-type: landing-page
---

{{AccessibilitySidebar}}

웹 개발에서 **접근성**(Accessibility, 줄여서 **A11y**)은 사용 능력이나 장애 여부와 관계없이 가능한 한 많은 사람이 웹사이트를 사용할 수 있게 하는 것을 말합니다. 어떤 사람은 눈이 보이지 않아 화면 낭독기를 쓰고, 어떤 사람은 손을 다쳐 마우스 대신 키보드만 씁니다. 저시력 사용자는 화면을 크게 확대하고, 인지 장애가 있는 사용자는 간결하고 예측 가능한 인터페이스가 필요합니다. 접근성을 갖춘 사이트는 이런 사용자들이 콘텐츠를 인식하고, 이해하고, 탐색하고, 조작할 수 있게 합니다.

접근성은 장애가 있는 사람만을 위한 것이 아닙니다. 느린 네트워크로 접속하거나, 작은 화면의 휴대 기기를 쓰거나, 햇빛 아래에서 화면을 보는 사람처럼 일시적이거나 상황에 따른 제약이 있는 사용자도 접근성 높은 사이트에서 혜택을 봅니다. 고령 사용자도 마찬가지입니다. 또한 많은 국가에서 공공기관과 일부 기업의 웹사이트에 접근성 준수를 법으로 요구하고 있습니다.

## 핵심 원칙

[W3C](https://www.w3.org/)의 [웹 콘텐츠 접근성 지침(WCAG)](https://www.w3.org/WAI/standards-guidelines/wcag/)은 웹 접근성을 네 가지 원칙으로 정리합니다. 각 원칙의 영문 첫 글자를 따서 **POUR**라고 부르기도 합니다.

- **인식의 용이성(Perceivable)**
  - : 사용자가 정보와 사용자 인터페이스 구성 요소를 인식할 수 있어야 합니다. 예를 들어 이미지에는 대체 텍스트를, 동영상에는 자막을 제공해야 합니다.
- **운용의 용이성(Operable)**
  - : 인터페이스 구성 요소와 탐색 기능을 조작할 수 있어야 합니다. 모든 기능을 키보드만으로 사용할 수 있어야 하고, 사용자가 콘텐츠를 읽고 사용할 시간이 충분해야 합니다.
- **이해의 용이성(Understandable)**
  - : 정보와 인터페이스의 동작을 이해할 수 있어야 합니다. 텍스트는 읽기 쉬워야 하고, 페이지는 예측 가능한 방식으로 동작해야 하며, 사용자가 실수를 피하고 바로잡도록 도와야 합니다.
- **견고성(Robust)**
  - : 보조 기술을 비롯한 다양한 사용자 에이전트가 콘텐츠를 안정적으로 해석할 수 있어야 합니다.

## 시작하기

접근성을 높이는 가장 효과적인 방법은 처음부터 올바른 HTML을 쓰는 것입니다. 많은 문제는 특별한 기법 없이 기본기만으로 해결할 수 있습니다.

### 시맨틱 HTML 사용하기

요소는 생김새가 아니라 의미에 맞게 고르세요. 클릭할 수 있는 요소에는 {{htmlelement("div")}} 대신 {{htmlelement("button")}}을 쓰세요. 버튼 요소는 키보드 포커스, <kbd>Enter</kbd>와 <kbd>Space</kbd> 키 동작, 보조 기술에 전달되는 역할 정보를 기본으로 제공합니다.

```html
<!-- 좋지 않은 예 -->
<div class="button" onclick="save()">저장</div>

<!-- 좋은 예 -->
<button type="button" onclick="save()">저장</button>
```

페이지 구조에는 {{htmlelement("header")}}, {{htmlelement("nav")}}, {{htmlelement("main")}}, {{htmlelement("footer")}} 같은 랜드마크 요소와 순서에 맞는 제목({{htmlelement("Heading_Elements", "&lt;h1&gt;–&lt;h6&gt;")}})을 쓰세요. 화면 낭독기 사용자는 이런 구조를 이용해 페이지를 빠르게 훑어봅니다.

### 텍스트 대안 제공하기

의미를 전달하는 이미지에는 [`alt`](/ko/docs/Web/HTML/Reference/Elements/img#alt) 특성으로 내용을 설명하세요. 장식용 이미지라면 `alt=""`처럼 빈 값을 주어 보조 기술이 건너뛰게 합니다.

```html
<img src="chart.png" alt="2025년 분기별 매출. 4분기에 가장 높음." />
<img src="divider.png" alt="" />
```

### 양식 레이블 연결하기

모든 양식 컨트롤에는 {{htmlelement("label")}}을 연결해야 합니다. 그러면 화면 낭독기가 입력 칸의 용도를 읽어 주고, 레이블을 클릭해도 컨트롤에 포커스가 갑니다.

```html
<label for="email">이메일</label>
<input type="email" id="email" name="email" autocomplete="email" />
```

### 색상과 대비 고려하기

텍스트와 배경 사이에는 충분한 명도 대비가 있어야 합니다. WCAG AA 기준은 일반 텍스트 4.5:1, 큰 텍스트 3:1입니다. 또한 오류 표시처럼 중요한 정보를 색으로만 전달하지 말고, 아이콘이나 텍스트를 함께 쓰세요.

### 키보드 접근성 확보하기

모든 대화형 요소는 <kbd>Tab</kbd> 키로 이동하고 조작할 수 있어야 합니다. 포커스 표시를 `outline: none`으로 없애지 말고, 꼭 바꿔야 한다면 {{cssxref(":focus-visible")}}로 눈에 잘 띄는 스타일을 지정하세요.

## WAI-ARIA

[WAI-ARIA](/ko/docs/Web/Accessibility/ARIA)(Accessible Rich Internet Applications)는 HTML만으로 표현하기 어려운 역할, 상태, 속성을 보조 기술에 알려 주는 특성 모음입니다. 탭, 대화 상자, 실시간으로 바뀌는 알림 영역처럼 복잡한 위젯을 만들 때 유용합니다.

```html
<div role="alert">저장되었습니다.</div>
<button aria-expanded="false" aria-controls="menu">메뉴</button>
```

그러나 ARIA는 기본 HTML을 보완하는 도구일 뿐 대체 수단이 아닙니다. 흔히 "ARIA를 쓰지 않는 것이 잘못 쓰는 것보다 낫다"고 합니다. 원하는 의미와 동작을 가진 네이티브 HTML 요소가 있다면 그 요소를 먼저 쓰세요.

## 접근성 테스트

자동화 도구는 문제를 빠르게 찾는 데 도움이 되지만, 모든 문제를 잡아내지는 못합니다. 다음 방법을 함께 쓰는 것이 좋습니다.

- 브라우저 개발자 도구의 접근성 검사기로 접근성 트리를 확인합니다.
- 마우스 없이 키보드만으로 모든 기능을 써 봅니다.
- NVDA, VoiceOver, TalkBack 같은 화면 낭독기로 페이지를 들어 봅니다.
- 화면을 200%까지 확대해도 콘텐츠가 잘리거나 겹치지 않는지 확인합니다.
- 가능하다면 장애가 있는 실제 사용자와 함께 사용성 테스트를 진행합니다.

## 안내서

- [접근성이란?](/ko/docs/Learn_web_development/Core/Accessibility/What_is_accessibility)
  - : 접근성의 개념, 보조 기술의 종류, 관련 법과 지침을 소개합니다.
- [HTML: 접근성의 좋은 기반](/ko/docs/Learn_web_development/Core/Accessibility/HTML)
  - : 시맨틱 HTML로 접근성을 높이는 방법을 설명합니다.
- [CSS와 JavaScript 접근성 모범 사례](/ko/docs/Learn_web_development/Core/Accessibility/CSS_and_JavaScript)
  - : 스타일과 스크립트를 쓸 때 주의할 점을 다룹니다.
- [WAI-ARIA 기초](/ko/docs/Learn_web_development/Core/Accessibility/WAI-ARIA_basics)
  - : ARIA로 복잡한 위젯의 접근성을 높이는 방법을 안내합니다.
- [모바일 접근성](/ko/docs/Learn_web_development/Core/Accessibility/Mobile)
  - : 터치 기기와 작은 화면에서 고려해야 할 사항을 정리합니다.

## 참고 자료

- [ARIA 참고서](/ko/docs/Web/Accessibility/ARIA/Reference)
- [WCAG 이해하기](/ko/docs/Web/Accessibility/Guides/Understanding_WCAG)
- [W3C 웹 접근성 이니셔티브(WAI)](https://www.w3.org/WAI/)
- [ARIA 작성 실무 지침(APG)](https://www.w3.org/WAI/ARIA/apg/)
