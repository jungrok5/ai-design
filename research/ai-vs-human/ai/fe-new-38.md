# 프론트엔드 월간 소식 — 2023-02

> 2월에는 브라우저 업데이트가 많았습니다. 웹 플랫폼의 한 해 목표를 정하는 Interop 2023이 발표됐고, Safari 16.4 베타에는 기다리던 기능이 대거 들어왔습니다. React 생태계에서는 Create React App의 앞날을 두고 논쟁이 벌어졌습니다. 이번 호도 핵심만 추렸습니다.

---

## 🔥 이달의 헤드라인

### Interop 2023 발표
Apple, Google, Microsoft, Mozilla, Igalia, Bocoup이 함께하는 **Interop 2023**이 2월 1일 발표됐습니다. 올해 중점 영역은 다음과 같습니다.

- **Container Queries**(크기 쿼리)와 **`:has()`** 선택자
- **Subgrid**, **CSS Color Level 4**, **Math 함수**
- **Web Components**, **Modules in Web Workers**
- **Pointer/Mouse 이벤트**, **Form 요소** 동작 일관성

브라우저마다 다르게 동작하던 기능들이 연말까지 상당 부분 맞춰질 예정입니다. 크로스 브라우저 대응에 시간을 많이 쓰던 팀이라면 반가운 소식입니다.

### Create React App, 이제 어디로?
React 공식 문서에서 CRA 대신 Vite를 추천하자는 PR을 두고 커뮤니티에서 논쟁이 이어졌습니다. 이에 React 팀의 Dan Abramov가 긴 답변을 남겼습니다. 요지는 **"앞으로는 프레임워크(Next.js, Remix 등)를 기본 출발점으로 권장하고, CRA는 그 방향에 맞게 정리하겠다"** 는 것입니다. 곧 공개될 새 공식 문서(react.dev)에서도 이 방향이 반영될 것으로 보입니다. 새 프로젝트를 시작할 때 무엇을 고를지 다시 생각해 볼 시점입니다.

---

## 🌐 브라우저 소식

### Safari 16.4 베타
2월 중순에 공개된 Safari 16.4 베타는 근래 Safari 업데이트 가운데 가장 큰 편입니다.

- **iOS/iPadOS 홈 화면 웹 앱에서 Web Push 지원**: PWA를 운영하는 팀이 오래 기다린 기능입니다.
- **Badging API**, **Screen Wake Lock API**
- **Import Maps**, **OffscreenCanvas**, **WebAssembly SIMD**
- 그 밖에 CSS와 Web Components 관련 개선이 다수 포함됐습니다.

정식 출시는 봄으로 예상되므로 지금 베타로 미리 테스트해 두기를 권합니다.

### Chrome 110
- CSS **`initial-letter`** 속성으로 문단 첫 글자를 크게 꾸미는 드롭캡을 쉽게 만들 수 있습니다.
- **`:picture-in-picture`** 의사 클래스가 추가됐습니다.
- 다음 버전(111)에는 **View Transitions API**와 CSS Color Level 4가 예고돼 있습니다.

### Firefox 110
- **Container Queries**가 기본으로 활성화됐습니다. 이로써 주요 3대 브라우저 엔진 모두에서 컨테이너 쿼리를 쓸 수 있게 됐습니다.

---

## ⚛️ 프레임워크 & 라이브러리

### Next.js 13.2
2월 말에 나온 13.2 버전은 App Router(beta)를 중심으로 개선됐습니다.

- **Metadata API**: `metadata` 객체나 `generateMetadata` 함수로 SEO 태그를 선언적으로 관리합니다.
- **Route Handlers**: `app` 디렉터리에서 Web 표준 `Request`/`Response` 기반으로 API를 작성합니다.
- **Statically Typed Links**(실험적): `<Link href>` 경로 오타를 타입 수준에서 잡아냅니다.
- Turbopack 개선과 MDX 지원도 함께 들어왔습니다.

### Angular, Signals 실험 시작
Angular 팀이 **Signals** 기반의 세밀한 반응성 모델 프로토타입을 공개했습니다. 장기적으로 Zone.js 의존을 줄이고 변경 감지 성능을 높이려는 시도입니다. Solid, Preact, Vue에 이어 Angular까지 Signal 계열 상태 모델로 모이는 흐름이 보입니다.

### Nuxt 3.2
커스텀 `$fetch` 설정, 빌드 성능 개선, 실험적 기능 추가 등 Nuxt 3의 안정화가 계속되고 있습니다.

---

## 🛠 도구 & 런타임

- **Vite 4.1**: 의존성 사전 번들링과 CSS 처리 등이 소폭 개선됐습니다. CRA 논쟁 덕분에 대안으로서 존재감도 더 커졌습니다.
- **TypeScript 5.0 베타 테스트 진행 중**: 1월 말 베타가 나온 뒤 ECMAScript 표준 **데코레이터**, `const` 타입 매개변수, `--moduleResolution bundler` 등을 실제로 써 본 피드백이 활발히 모이고 있습니다. RC는 3월 예정입니다.
- **Deno 1.31**: `package.json`을 인식하게 되어 npm 생태계와의 호환성이 한층 높아졌습니다.
- **Bun 0.5.x**: 잇따른 패치 릴리스로 Node.js API 호환 범위를 빠르게 넓히고 있습니다.

---

## 📚 이달의 읽을거리

1. **`:has()` 실전 활용 패턴**: "부모 선택자"로 폼 상태 스타일링, 레이아웃 분기 등을 JS 없이 처리하는 사례가 많이 공유됐습니다.
2. **Signals는 왜 다시 유행하는가**: 가상 DOM 비교 방식과 세밀한 반응성의 장단점을 다룬 글이 주목받았습니다.
3. **CRA 이후의 React 시작 가이드**: Vite + React, Next.js, Remix 중 무엇을 고를지 비교한 글이 쏟아졌습니다. 팀 상황에 맞춰 비교해 보세요.

---

## ✍️ 마치며

2월은 **웹 플랫폼이 빠르게 표준을 맞춰 가는 달**이었습니다. Container Queries가 3대 엔진 모두에서 동작하게 됐고, iOS 웹 푸시도 가시권에 들어왔습니다. 그동안 "아직 지원이 부족해서" 미뤄 둔 기능이 있다면 다시 살펴볼 때입니다.

다음 호에서는 3월에 예정된 **TypeScript 5.0 정식 출시**와 **새 React 공식 문서** 소식을 중심으로 전하겠습니다. 다음 달에 또 만나요! 👋
