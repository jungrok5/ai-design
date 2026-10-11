# CSS와 JavaScript의 접근성 모범 사례

## 개요

웹 접근성은 장애가 있는 사용자를 포함한 모든 사람이 웹 콘텐츠를 인지하고, 이해하고, 탐색하고, 조작할 수 있도록 보장하는 일입니다. HTML이 콘텐츠의 의미를 제공한다면, CSS는 그 의미를 시각적으로 드러내고, JavaScript는 상호작용의 흐름을 만듭니다. 세 가지 중 하나라도 접근성을 해치면 사용자 경험 전체가 무너질 수 있습니다.

이 문서는 WCAG 2.2 AA 수준을 목표로 할 때 CSS와 JavaScript에서 특히 주의해야 할 사항을 정리합니다.

## 1. 의미를 해치지 않는 스타일

CSS는 요소의 외관을 바꿀 수 있지만, 접근성 트리에 노출되는 역할(role)과 이름을 바꾸어서는 안 됩니다. 일부 브라우저와 보조 기술 조합에서는 `list-style: none`이나 `display: contents`를 적용했을 때 목록이나 버튼의 의미가 사라지는 문제가 보고되어 왔습니다. 스타일을 바꾸기 전후에 스크린리더로 실제 결과를 확인하는 것이 안전합니다.

## 2. 포커스 표시 유지

키보드 사용자에게 포커스 위치는 마우스 사용자의 커서와 같습니다. 다음 코드는 포커스 표시를 제거하는 대표적인 실수입니다.

```css
/* 피해야 할 방식 */
:focus {
  outline: none;
}
```

대신 `:focus-visible`로 키보드 포커스에만 뚜렷한 표시를 주고, 배경과의 대비가 3:1 이상이 되도록 합니다.

```css
:root {
  --focus-color: #1a4fd6;
}

:focus-visible {
  outline: 3px solid var(--focus-color);
  outline-offset: 2px;
}
```

## 3. 색상 대비와 색에만 의존하지 않기

본문 텍스트는 배경과 4.5:1 이상의 대비를 갖추어야 하며, 큰 텍스트와 아이콘, 입력 필드 테두리 같은 UI 요소는 3:1 이상이 필요합니다. 오류 상태를 빨간색으로만 표시하면 색각 이상 사용자가 구분하기 어렵습니다. 아이콘이나 텍스트 메시지를 함께 제공하세요.

## 4. 사용자 환경 설정 존중

운영체제의 설정을 CSS 미디어 쿼리로 읽어 반영할 수 있습니다.

```css
:root {
  color-scheme: light dark;
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

움직임에 민감한 사용자는 전정기관 장애로 어지러움을 느낄 수 있으므로, 자동 재생 애니메이션이나 시차 효과는 이 설정에서 줄이거나 제거해야 합니다.

## 5. 확대와 텍스트 크기

고정 픽셀 단위 대신 `rem`이나 `em`을 사용하면 사용자가 브라우저 기본 글꼴 크기를 바꿨을 때 레이아웃이 함께 반응합니다. 텍스트를 200%까지 확대해도 내용이 잘리거나 겹치지 않아야 하며, 320px 너비에서 가로 스크롤 없이 읽힐 수 있어야 합니다.

## 6. 동적 변경 알리기

JavaScript로 콘텐츠를 바꿀 때 스크린리더 사용자는 그 변화를 알아차리지 못할 수 있습니다. 중요하지 않은 상태 변화는 `aria-live` 영역으로 알립니다.

```html
<div aria-live="polite" id="status"></div>
```

```javascript
function showStatus(message) {
  const status = document.getElementById('status');
  status.textContent = message;
}
```

오류처럼 즉시 주의가 필요한 내용에는 `aria-live="assertive"`를 사용하되, 남용하지 않는 것이 좋습니다.

## 7. 키보드 조작과 포커스 관리

모든 기능은 마우스 없이 키보드만으로 사용할 수 있어야 합니다. `div`에 클릭 이벤트만 붙인 요소는 키보드로 접근할 수 없으므로, 가능하면 `<button>`이나 `<a>`를 사용하세요. 부득이하게 `tabindex`를 쓸 때는 `tabindex="0"`이나 `-1`만 사용하고, 양수 값은 탭 순서를 예측하기 어렵게 만들므로 피합니다.

모달 대화상자를 열면 포커스를 대화상자 안으로 옮기고, 닫을 때는 원래 버튼으로 되돌려야 합니다.

```javascript
function openDialog(dialog, trigger) {
  dialog.hidden = false;
  dialog.querySelector('button, [href], input, select, textarea')?.focus();

  dialog.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeDialog(dialog, trigger);
  }, { once: true });
}

function closeDialog(dialog, trigger) {
  dialog.hidden = true;
  trigger.focus();
}
```

최신 브라우저에서는 `<dialog>` 요소와 `showModal()`을 사용하면 포커스 가두기와 Escape 처리가 기본으로 제공되므로 가능한 한 이를 활용하는 것이 좋습니다.

## 8. ARIA는 최후의 수단

ARIA 속성은 HTML 요소만으로 표현할 수 없을 때 보완하는 용도입니다. 가장 중요한 원칙은 "네이티브 HTML을 먼저 사용하라"는 것입니다. 예를 들어 `<button>`은 역할, 상태, 키보드 동작을 모두 갖추고 있습니다. 확장 메뉴처럼 상태가 바뀌는 요소라면 `aria-expanded`를 JavaScript로 함께 갱신해야 합니다.

```javascript
button.addEventListener('click', () => {
  const expanded = button.getAttribute('aria-expanded') === 'true';
  button.setAttribute('aria-expanded', String(!expanded));
  panel.hidden = expanded;
});
```

## 9. 숨김 처리의 구분

시각적으로만 숨기고 스크린리더에는 읽히게 하려면 `sr-only` 패턴을 사용합니다. 반대로 모든 사용자에게서 숨기려면 `hidden` 속성이나 `display: none`을 씁니다.

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

`opacity: 0`이나 `font-size: 0`은 보이지 않아도 보조 기술에 읽힐 수 있어 의도와 다르게 동작하기도 합니다.

## 10. 검증 방법

자동화 도구는 문제의 약 30~40%만 찾아낸다고 알려져 있으므로, 다음 방법을 함께 사용해야 합니다.

- **자동 검사**: axe DevTools, Lighthouse 접근성 감사로 명백한 오류를 확인합니다.
- **키보드 테스트**: Tab, Shift+Tab, Enter, Space, 화살표 키만으로 모든 기능을 완료할 수 있는지 점검합니다.
- **스크린리더 테스트**: NVDA, VoiceOver 등으로 주요 흐름을 실제로 들어 봅니다.
- **확대 및 설정 테스트**: 브라우저 확대 200%, 다크 모드, 동작 줄이기 설정에서 화면을 확인합니다.

## 요약

접근성은 마지막에 덧붙이는 기능이 아니라 설계 단계부터 고려해야 할 품질 요소입니다. 의미 있는 HTML을 기반으로, CSS로는 포커스와 대비를 명확히 하고 사용자 설정을 존중하며, JavaScript로는 상태 변화를 알리고 포커스를 적절히 관리하면 대부분의 사용자가 불편 없이 웹을 사용할 수 있습니다.

---

*참고: 이 문서는 MDN 스타일의 구성과 용어를 따라 작성한 설명서이며, MDN 웹 문서의 원문을 그대로 옮긴 것은 아닙니다.*
