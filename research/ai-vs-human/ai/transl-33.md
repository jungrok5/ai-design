---
title: 이미지, 미디어 및 양식 요소
slug: Learn/CSS/Building_blocks/Images_media_form_elements
---

{{LearnSidebar}}{{PreviousMenuNext("Learn/CSS/Building_blocks/Sizing_items_in_CSS", "Learn/CSS/Building_blocks/Styling_tables", "Learn/CSS/Building_blocks")}}

이 단원에서는 CSS가 특정 요소를 다루는 방식을 살펴봅니다. 이미지, 기타 미디어, 양식 요소는 CSS로 스타일을 지정할 때 일반적인 상자와 조금 다르게 동작합니다. 무엇을 할 수 있고 무엇을 할 수 없는지 알아 두면 불필요한 시행착오를 줄일 수 있습니다.

<table>
  <tbody>
    <tr>
      <th scope="row">전제 조건:</th>
      <td>
        기본적인 컴퓨터 사용 능력,
        <a href="/ko/docs/Learn/Getting_started_with_the_web/Installing_basic_software">기본 소프트웨어 설치</a>,
        <a href="/ko/docs/Learn/HTML/Introduction_to_HTML">HTML 기초</a>,
        <a href="/ko/docs/Learn/CSS/First_steps">CSS 작동 방식</a>에 대한 이해
      </td>
    </tr>
    <tr>
      <th scope="row">목표:</th>
      <td>
        일부 요소가 CSS에서 특이하게 동작하는 이유를 이해하고, 이런 요소에 스타일을 지정하는 방법을 배웁니다.
      </td>
    </tr>
  </tbody>
</table>

## 대체 요소

이미지와 비디오는 **[대체 요소](/ko/docs/Web/CSS/Replaced_element)**(replaced element)에 해당합니다. CSS는 이런 요소의 내부 레이아웃에 영향을 줄 수 없습니다. 페이지 안에서 다른 요소와의 상대적인 위치만 정할 수 있습니다. 하지만 앞으로 살펴볼 것처럼 이미지로 할 수 있는 일은 여럿 있습니다.

{{htmlelement("video")}}, {{htmlelement("iframe")}}, {{htmlelement("embed")}}와 같은 요소도 대체 요소입니다. 이미지를 비롯한 일부 대체 요소에는 **종횡비**(aspect ratio)가 있습니다. 가로 크기와 세로 크기가 모두 정해져 있어서, 기본적으로 파일 자체의 크기대로 표시됩니다.

## 이미지 크기 조정

지금까지 배운 것처럼 CSS에서 모든 것은 상자를 만듭니다. 이미지 파일의 고유 크기보다 작거나 큰 상자 안에 이미지를 넣으면, 이미지가 상자보다 작게 표시되거나 상자 밖으로 넘칩니다. 두 경우 모두 어떻게 처리할지 결정해야 합니다.

흔히 쓰는 방법은 이미지에 {{cssxref("max-width")}}를 `100%`로 지정하는 것입니다. 이렇게 하면 이미지 크기가 고유 크기보다 작아질 수는 있지만 커지지는 않습니다. 이 기법은 다른 대체 요소에도 적용됩니다.

```css
img {
  max-width: 100%;
}
```

이미지가 상자를 빈틈없이 덮도록 늘리고 싶을 수도 있습니다. 이럴 때 {{cssxref("object-fit")}} 속성을 사용하면 대체 요소의 크기를 상자에 맞게 여러 방식으로 조정할 수 있습니다.

```css
.box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

- `cover`: 종횡비를 유지한 채 상자를 완전히 덮도록 이미지를 키우거나 줄입니다. 상자와 비율이 다르면 이미지 일부가 잘립니다.
- `contain`: 종횡비를 유지한 채 이미지 전체가 상자 안에 들어오도록 크기를 맞춥니다. 상자와 비율이 다르면 레터박스처럼 빈 공간이 생깁니다.
- `fill`: 종횡비를 무시하고 상자를 꽉 채웁니다. 이미지가 찌그러질 수 있습니다.

> [!NOTE]
> `object-fit`은 `<video>` 같은 다른 대체 요소에도 똑같이 사용할 수 있습니다.

## 레이아웃 안의 대체 요소

CSS 레이아웃 기법을 대체 요소에 적용하면 다른 요소와 조금 다르게 동작할 수 있습니다. 예를 들어 그리드 레이아웃에서 요소는 기본적으로 영역 전체를 채우도록 늘어납니다. 하지만 이미지는 늘어나지 않고 그리드 영역의 시작 지점에 정렬됩니다.

```css
.wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 200px 200px;
  gap: 20px;
}

.wrapper > div {
  background-color: rebeccapurple;
  border-radius: 0.5em;
}
```

이처럼 동작하는 이유는 사양에 "대체 요소는 늘어나지 않는다"고 정해져 있기 때문입니다. 이미지가 그리드 영역을 채우게 하려면 다음과 같이 작성합니다.

```css
img {
  width: 100%;
  height: 100%;
}
```

이 경우에도 이미지가 찌그러지지 않게 하려면 앞에서 배운 `object-fit: cover`를 함께 사용합니다.

## 양식 요소

양식 요소는 CSS로 스타일을 지정하기 까다로울 수 있습니다. [웹 양식 모듈](/ko/docs/Learn/Forms)에서 브라우저마다 스타일을 지정하기 어려운 양식 요소를 자세히 다룹니다. 여기서는 알아 두어야 할 기본 사항만 살펴보겠습니다.

`<input>` 요소로 정의하는 텍스트 입력 칸과 `<textarea>` 같은 여러 양식 컨트롤은 일반 상자처럼 동작하므로 스타일을 지정하기 비교적 쉽습니다. 반면 날짜 선택기처럼 운영 체제의 기본 UI를 사용하는 요소는 스타일을 바꾸기 어렵습니다.

```css
input[type="text"],
input[type="email"] {
  border: 2px solid #000;
  margin: 0 0 1em 0;
  padding: 10px;
  width: 100%;
}

input[type="submit"] {
  border: 3px solid #333;
  background-color: #999;
  border-radius: 5px;
  padding: 10px 2em;
  font-weight: bold;
  color: #fff;
}
```

> [!WARNING]
> 양식 요소의 스타일을 바꿀 때는 사용자가 그것이 양식 요소라는 사실을 쉽게 알아볼 수 있어야 합니다. 테두리와 배경이 없는 입력 칸은 다른 콘텐츠와 구분하기 어려워 사용성이 떨어집니다.

### 글꼴과 텍스트 상속

일부 브라우저에서는 양식 요소가 글꼴 스타일을 상속하지 않습니다. 양식 칸이 본문에 정의한 글꼴을 사용하도록 하려면 다음 규칙을 추가합니다.

```css
button,
input,
select,
textarea {
  font-family: inherit;
  font-size: 100%;
}
```

### 양식 요소와 box-sizing

브라우저마다 양식 요소에 서로 다른 상자 크기 규칙을 적용합니다. 어떤 요소는 `content-box`를, 어떤 요소는 `border-box`를 쓰기 때문에 같은 너비를 지정해도 렌더링 결과가 달라질 수 있습니다. 일관성을 위해 모든 요소의 여백과 패딩을 `0`으로 설정한 뒤 개별 컨트롤에 다시 지정하고, `box-sizing`을 통일하는 것이 좋습니다.

```css
button,
input,
select,
textarea {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}
```

### 기타 유용한 설정

위 규칙 외에도 `<textarea>`에 `overflow: auto`를 지정하면 스크롤 막대가 필요 없을 때 Internet Explorer가 스크롤 막대를 표시하는 문제를 막을 수 있습니다.

```css
textarea {
  overflow: auto;
}
```

### 정규화 스타일 모으기

지금까지 살펴본 규칙을 한데 모으면 작업을 시작할 때 쓸 수 있는 간단한 "리셋"이 됩니다. [Normalize.css](https://necolas.github.io/normalize.css/)처럼 많은 개발자가 프로젝트마다 사용하는 정규화 스타일시트도 있습니다.

## 실력 테스트

이 단원에서 배운 내용을 잘 이해했는지 확인하려면 [이미지와 양식 요소 실력 테스트](/ko/docs/Learn/CSS/Building_blocks/Images_tasks)를 풀어 보세요.

## 요약

이 단원에서는 이미지, 미디어, 기타 특이한 요소를 CSS에서 다룰 때의 차이점을 살펴보았습니다. 다음 단원에서는 HTML 표에 스타일을 지정하는 방법을 알아보겠습니다.

{{PreviousMenuNext("Learn/CSS/Building_blocks/Sizing_items_in_CSS", "Learn/CSS/Building_blocks/Styling_tables", "Learn/CSS/Building_blocks")}}
