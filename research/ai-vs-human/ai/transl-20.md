# 웹 성능

웹 성능(Web Performance)은 웹 애플리케이션이 얼마나 빠르게 로드되고, 얼마나 빠르게 반응하며, 사용자가 상호작용하는 동안 얼마나 부드럽게 동작하는지를 측정하고 개선하는 것을 말합니다. 웹 페이지가 빠를수록 사용자는 콘텐츠를 더 빨리 이용할 수 있고, 이탈률은 낮아지며, 검색 엔진 노출에도 긍정적인 영향을 받습니다.

## 웹 성능이 중요한 이유

사용자는 페이지가 응답하지 않거나 느리게 보이면 쉽게 떠납니다. 모바일 네트워크나 저사양 기기에서 접속하는 사용자에게는 이 문제가 더 크게 나타납니다. 성능 개선은 단순히 기술적인 목표가 아니라 사용자 경험, 전환율, 접근성과 직접 연결됩니다.

## 성능 측정하기

성능을 개선하려면 먼저 측정해야 합니다. 웹 브라우저는 성능 정보를 얻기 위한 여러 API를 제공합니다.

- **Navigation Timing API**: 문서 탐색의 단계별 소요 시간을 제공합니다.
- **Resource Timing API**: 이미지, 스크립트, 스타일시트 등 개별 리소스의 로딩 시간을 보여 줍니다.
- **Performance Observer API**: 성능 관련 이벤트를 비동기적으로 관찰할 수 있게 합니다.
- **User Timing API**: `performance.mark()`와 `performance.measure()`로 직접 정의한 구간의 시간을 측정합니다.

```javascript
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log(entry.name, entry.startTime, entry.duration);
  }
});
observer.observe({ type: "resource", buffered: true });
```

측정은 실험실 환경(Lighthouse 등 합성 테스트)과 현장 데이터(실제 사용자로부터 수집한 RUM, Real User Monitoring) 두 가지 방식으로 나눌 수 있습니다. 실험실 데이터는 재현성이 높아 디버깅에 유용하고, 현장 데이터는 실제 사용자가 겪는 경험을 반영합니다.

## 핵심 웹 지표 (Core Web Vitals)

Google이 정의한 핵심 웹 지표는 사용자 경험의 핵심 측면을 대표하는 세 가지 지표입니다.

| 지표 | 의미 | 권장 기준 (75백분위수) |
| --- | --- | --- |
| LCP (Largest Contentful Paint) | 가장 큰 콘텐츠 요소가 화면에 그려지는 시간 | 2.5초 이하 |
| INP (Interaction to Next Paint) | 사용자 상호작용부터 다음 화면 갱신까지의 지연 | 200밀리초 이하 |
| CLS (Cumulative Layout Shift) | 페이지 로딩 중 예기치 않은 레이아웃 이동의 누적 점수 | 0.1 이하 |

INP는 2024년 FID(First Input Delay)를 대체한 지표입니다. 페이지의 모든 상호작용을 고려하므로 첫 입력뿐 아니라 전반적인 반응성을 평가합니다.

## 로딩 성능 개선

### 중요한 리소스 우선순위 지정

가장 먼저 보여야 하는 리소스는 빠르게 가져오고, 나머지는 뒤로 미루는 것이 기본 전략입니다.

- `<link rel="preload">`는 현재 페이지에서 곧 필요한 리소스를 미리 요청합니다.
- `<link rel="preconnect">`는 외부 출처와의 연결(DNS 조회, TCP, TLS)을 미리 설정합니다.
- `fetchpriority="high"` 속성은 LCP 이미지처럼 중요한 리소스의 우선순위를 높입니다.

### 스크립트 로딩

`<script>` 요소는 기본적으로 HTML 파싱을 멈추고 실행됩니다. `defer` 속성을 사용하면 HTML 파싱이 끝난 뒤 순서대로 실행되며, `async` 속성을 사용하면 다운로드가 끝나는 즉시 실행됩니다. 분석 스크립트나 광고처럼 페이지 동작과 무관한 코드는 `async`로 불러오는 것이 적절합니다.

```html
<script src="app.js" defer></script>
<script src="analytics.js" async></script>
```

### 코드 분할

번들 크기를 줄이기 위해 사용자가 당장 필요로 하지 않는 코드를 나누어 필요할 때만 불러올 수 있습니다. 동적 `import()` 구문을 활용하면 라우트나 기능 단위로 코드를 분리할 수 있습니다.

```javascript
button.addEventListener("click", async () => {
  const { openChart } = await import("./chart.js");
  openChart();
});
```

### 이미지 최적화

이미지는 대개 페이지 용량의 큰 부분을 차지합니다. 다음 방법으로 전송량을 줄일 수 있습니다.

- AVIF나 WebP 같은 최신 형식을 사용합니다.
- `srcset`과 `sizes`로 기기 해상도와 뷰포트 크기에 맞는 이미지를 제공합니다.
- 화면 밖에 있는 이미지에는 `loading="lazy"`를 지정합니다. 단, LCP 이미지에는 지연 로딩을 적용하지 않는 것이 좋습니다.
- 이미지의 `width`와 `height` 속성을 명시해 레이아웃 이동(CLS)을 막습니다.

```html
<img src="hero-800.avif"
     srcset="hero-400.avif 400w, hero-800.avif 800w, hero-1600.avif 1600w"
     sizes="(max-width: 600px) 100vw, 800px"
     width="800" height="450"
     alt="제품 소개 이미지"
     fetchpriority="high">
```

### 전송 및 캐싱

- Gzip이나 Brotli 압축을 사용해 텍스트 리소스의 크기를 줄입니다.
- `Cache-Control` 헤더로 변하지 않는 정적 파일을 오래 캐시하고, 파일 이름에 해시를 포함해 갱신을 관리합니다.
- CDN을 활용해 사용자와 가까운 위치에서 콘텐츠를 제공합니다.
- HTTP/2 이상의 프로토콜을 사용해 여러 요청을 효율적으로 처리합니다.

## 렌더링 성능 개선

### 레이아웃 스래싱 피하기

DOM을 변경한 직후 레이아웃 값(예: `offsetHeight`)을 읽으면 브라우저는 레이아웃을 강제로 다시 계산합니다. 읽기와 쓰기를 분리하면 이 비용을 줄일 수 있습니다.

```javascript
// 나쁜 예: 읽기와 쓰기가 번갈아 발생
items.forEach((item) => {
  item.style.width = container.offsetWidth + "px";
});

// 좋은 예: 읽기를 먼저 모아서 수행
const width = container.offsetWidth;
items.forEach((item) => {
  item.style.width = width + "px";
});
```

### 애니메이션

애니메이션은 가능한 한 `transform`과 `opacity`처럼 합성(compositing) 단계에서 처리되는 속성을 사용하세요. `width`, `top`, `left` 같은 속성을 애니메이션하면 레이아웃과 페인트가 반복되어 비용이 커집니다. 또한 `requestAnimationFrame()`을 사용하면 브라우저의 화면 갱신 주기에 맞춰 작업을 수행할 수 있습니다.

### 긴 작업 나누기

메인 스레드를 50밀리초 이상 점유하는 작업은 사용자 입력에 대한 응답을 지연시킵니다. 큰 작업은 작은 단위로 나누고, 사이사이에 브라우저에 양보(yield)하면 INP를 개선할 수 있습니다. 무거운 계산은 Web Worker로 옮기는 것도 좋은 방법입니다.

### 보이지 않는 영역의 렌더링 줄이기

`content-visibility: auto`를 사용하면 화면 밖 요소의 렌더링을 건너뛰어 초기 렌더링 시간을 줄일 수 있습니다. 긴 목록에서는 가상화(virtualization) 기법을 함께 고려할 수 있습니다.

## 웹 폰트 최적화

웹 폰트가 로드되기 전까지 텍스트가 보이지 않는 현상을 막기 위해 `font-display: swap`을 지정하는 것이 일반적입니다. 필요한 글자만 포함하도록 서브셋을 만들고, 가능하면 WOFF2 형식을 사용하세요. 폰트 교체로 인한 레이아웃 이동은 시스템 폰트와의 크기 조정(`size-adjust`)으로 줄일 수 있습니다.

## 성능 예산

성능 예산(Performance Budget)은 번들 크기, 요청 수, 핵심 지표의 목표치를 미리 정해 두고 이를 넘으면 빌드나 배포 단계에서 경고를 받는 방식입니다. 기능을 추가할 때마다 성능이 악화되는 것을 막는 데 효과적입니다.

## 정리

웹 성능 최적화는 한 번의 작업으로 끝나는 것이 아니라 측정, 분석, 개선, 검증을 반복하는 과정입니다. 사용자의 실제 환경에서 측정한 데이터를 기준으로 가장 큰 병목부터 해결하고, 핵심 웹 지표를 꾸준히 모니터링하는 것이 중요합니다.

## 함께 보기

- Navigation Timing API
- Resource Timing API
- Performance Observer API
- Core Web Vitals
- `loading` 속성
- `content-visibility`
