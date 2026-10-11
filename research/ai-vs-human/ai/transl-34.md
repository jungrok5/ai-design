# 사용자 에이전트를 사용한 브라우저 감지

**사용자 에이전트(User-Agent) 문자열**은 브라우저가 서버에 요청을 보낼 때 함께 전송하는 문자열로, 브라우저의 종류와 버전, 운영 체제 등의 정보를 담고 있습니다. 오래전부터 이 문자열을 분석해 브라우저를 구분하는 방식(UA 스니핑)이 널리 쓰였습니다. 하지만 이 방법은 오류가 나기 쉽고 유지 보수 비용이 크기 때문에, 가능한 한 다른 방법을 먼저 고려해야 합니다. 이 문서에서는 UA 감지가 왜 위험한지, 대안은 무엇인지, 불가피하게 써야 할 때 어떻게 해야 하는지를 설명합니다.

## 브라우저 감지를 쓰기 전에 고려할 것

브라우저를 감지하려는 이유를 먼저 점검해 보세요. 대부분의 경우 다음과 같은 더 나은 방법이 있습니다.

- **기능 감지(feature detection):** 브라우저의 종류가 아니라, 필요한 기능을 지원하는지를 직접 확인합니다.
- **점진적 향상(progressive enhancement):** 모든 브라우저에서 동작하는 기본 기능을 먼저 만들고, 지원하는 브라우저에만 고급 기능을 덧붙입니다.
- **우아한 성능 저하(graceful degradation):** 최신 기능을 기준으로 만들되, 지원하지 않는 환경에서도 최소한의 동작을 보장합니다.
- **미디어 쿼리와 `@supports`:** CSS 수준에서 화면 크기나 기능 지원 여부에 따라 스타일을 분기합니다.

UA 문자열에 의존하면 새 브라우저가 나오거나 기존 브라우저의 문자열이 바뀔 때마다 코드를 고쳐야 합니다. 또한 사용자가 문자열을 직접 바꿀 수 있고, 일부 브라우저는 호환성을 위해 다른 브라우저인 척하는 값을 보내기도 합니다.

## 사용자 에이전트 문자열의 구조

현대 브라우저의 UA 문자열은 역사적 이유로 매우 복잡하고 서로 비슷합니다. 예를 들어 Chrome의 문자열은 다음과 같습니다.

```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36
```

이 문자열에는 실제로는 Chrome이지만 `Mozilla`, `AppleWebKit`, `KHTML`, `Gecko`, `Safari`라는 단어가 모두 들어 있습니다. 과거에 서버가 특정 브라우저에만 콘텐츠를 보내던 관행 때문에 다른 브라우저들이 호환성을 위해 이런 단어를 덧붙여 온 결과입니다. 따라서 `Safari`가 포함되어 있다고 해서 Safari라고 단정할 수 없습니다.

### 브라우저별 대표적인 토큰

| 브라우저 | 확인할 토큰 | 주의할 점 |
| --- | --- | --- |
| Firefox | `Firefox/버전` | `Seamonkey/버전`이 함께 있으면 SeaMonkey |
| Chrome | `Chrome/버전` | Chromium, Edge, Opera 등도 포함할 수 있음 |
| Edge (Chromium) | `Edg/버전` | `Edge/`는 구형 EdgeHTML 엔진 |
| Opera | `OPR/버전` | `Chrome/`도 함께 포함됨 |
| Safari | `Safari/버전` 이면서 `Chrome/`, `Chromium/`이 없음 | 다른 브라우저는 `Safari`를 포함함 |

핵심 원칙은 **더 구체적인 토큰을 먼저 검사하고, 포괄적인 토큰은 나중에 검사하는 것**입니다. 예를 들어 Chrome을 확인하기 전에 Edge와 Opera를 먼저 걸러내야 합니다.

## 모바일 기기 감지

모바일 기기를 구분해야 한다면 UA 문자열에서 `Mobi`라는 부분 문자열을 찾는 것이 가장 간단하고 권장되는 방법입니다. 대부분의 모바일 브라우저가 이 값을 포함합니다.

```js
const isMobile = /Mobi/i.test(navigator.userAgent);
```

다만 화면 크기에 따라 레이아웃을 바꾸려는 것이라면 UA 대신 CSS 미디어 쿼리를 쓰는 편이 훨씬 안정적입니다. 터치 입력 여부가 궁금하다면 `navigator.maxTouchPoints`나 `(pointer: coarse)` 미디어 쿼리를 활용할 수 있습니다.

```js
const hasTouch = navigator.maxTouchPoints > 0;
const coarsePointer = window.matchMedia("(pointer: coarse)").matches;
```

## 기능 감지의 예

특정 API가 있는지 확인하는 것은 브라우저 이름을 확인하는 것보다 정확합니다.

```js
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/sw.js");
} else {
  // 서비스 워커를 지원하지 않는 환경을 위한 대체 동작
}
```

CSS에서는 `@supports`를 사용합니다.

```css
.card {
  display: block;
}

@supports (display: grid) {
  .card {
    display: grid;
    gap: 1rem;
  }
}
```

이렇게 하면 새로운 브라우저가 해당 기능을 지원하기 시작했을 때 코드를 수정하지 않아도 자동으로 혜택을 받을 수 있습니다.

## 사용자 에이전트 클라이언트 힌트

UA 문자열은 점차 축소(User-Agent Reduction)되는 추세입니다. 개인정보 보호와 핑거프린팅 방지를 위해 브라우저가 상세한 버전과 기기 정보를 문자열에서 줄이고 있습니다. 대신 필요한 정보만 명시적으로 요청하는 **사용자 에이전트 클라이언트 힌트(User-Agent Client Hints)** 가 도입되었습니다.

서버는 `Accept-CH` 응답 헤더로 필요한 정보를 요청할 수 있습니다.

```http
Accept-CH: Sec-CH-UA-Platform, Sec-CH-UA-Platform-Version
```

그러면 브라우저는 이후 요청에 `Sec-CH-UA-Platform` 같은 헤더를 포함해 보냅니다. 자바스크립트에서는 `navigator.userAgentData`로 접근할 수 있습니다.

```js
if (navigator.userAgentData) {
  console.log(navigator.userAgentData.mobile);
  console.log(navigator.userAgentData.platform);

  const values = await navigator.userAgentData.getHighEntropyValues([
    "platformVersion",
    "model",
  ]);
  console.log(values);
}
```

이 API는 아직 모든 브라우저에서 지원되지 않으므로, 사용 전에 `navigator.userAgentData`가 존재하는지 확인해야 합니다.

## 그래도 UA 감지가 필요하다면

특정 브라우저의 알려진 버그를 우회해야 하는 것처럼, 기능 감지로는 해결할 수 없는 경우가 있습니다. 그럴 때는 다음 지침을 따르세요.

1. **감지 범위를 최소화하세요.** 문제가 되는 브라우저와 버전만 정확히 대상으로 삼습니다.
2. **버전 비교는 신중하게 하세요.** 버그가 수정된 이후의 버전에서는 우회 코드가 적용되지 않도록 합니다.
3. **알 수 없는 브라우저는 최신 브라우저로 간주하세요.** 목록에 없는 브라우저를 차단하지 말고, 표준을 따른다고 가정합니다.
4. **우회 코드를 문서화하세요.** 어떤 버그 때문에 필요한지 주석으로 남기면 나중에 제거하기 쉽습니다.
5. **서버와 클라이언트 중 한 곳에서만 처리하세요.** 두 곳에서 판단이 엇갈리면 디버깅이 어려워집니다.

## 정리

- UA 문자열은 위조가 쉽고, 호환성을 위한 거짓 토큰이 많아 신뢰하기 어렵습니다.
- 브라우저를 구분하기보다 **필요한 기능이 있는지** 확인하세요.
- 모바일 여부는 `Mobi`를 찾거나, 가능하면 미디어 쿼리와 터치 지원 여부를 활용하세요.
- 새로운 환경에서는 **사용자 에이전트 클라이언트 힌트**가 UA 문자열을 대체해 가고 있습니다.
- 어쩔 수 없이 UA 감지를 쓴다면 범위를 좁히고, 알 수 없는 브라우저는 허용하는 방향으로 작성하세요.

## 같이 보기

- `navigator.userAgent`
- `navigator.userAgentData`
- HTTP `User-Agent` 헤더
- HTTP 클라이언트 힌트
- CSS `@supports`
- CSS 미디어 쿼리
