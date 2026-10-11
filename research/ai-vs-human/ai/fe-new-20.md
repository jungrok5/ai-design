# 🗞️ 프론트엔드 월간 소식 — 2022-02

안녕하세요, 독자 여러분! 2월은 짧은 달이었지만 프론트엔드 생태계는 바빴습니다. Vue 3가 마침내 기본 버전이 되었고, TypeScript 4.6이 정식 출시되었습니다. 여러 브라우저도 CSS Cascade Layers 지원을 앞다퉈 내놓았습니다. 이번 호에서는 그중 꼭 알아야 할 소식을 골라 정리했습니다.

---

## 🔥 이달의 하이라이트

### Vue 3, 드디어 '기본값'이 되다

2월 7일부로 npm의 `vue` 패키지 `latest` 태그가 3.x 버전으로 바뀌었습니다. 이제 `npm install vue`만 실행해도 Vue 3가 설치됩니다. 공식 문서 사이트(vuejs.org)도 Vue 3 기준의 새 문서로 바뀌었습니다. 새 문서에서는 Options API와 Composition API를 토글로 바꿔 가며 볼 수 있습니다. Vue Router, Vuex, Vue DevTools 같은 핵심 생태계 라이브러리도 Vue 3 버전이 기본이 되었습니다. 새 프로젝트의 공식 추천 조합은 **Vite + Pinia**입니다.

> 💡 **체크 포인트**: 아직 Vue 2를 쓰는 프로젝트라면 `package.json`에서 버전 범위를 확인해 두세요. 범위가 느슨하면 의도치 않게 Vue 3가 설치될 수 있습니다. Vue 2.7(가칭 'Naruto')에서는 Composition API 일부를 백포트할 예정이니 마이그레이션 계획을 세울 때 참고하세요.

### TypeScript 4.6 정식 출시

2월 말 TypeScript 4.6이 정식 출시되었습니다. 주요 변경 사항은 다음과 같습니다.

- **구조 분해된 판별 유니온의 제어 흐름 분석**: 판별 유니온 객체를 구조 분해한 뒤에도, 판별 필드로 분기하면 나머지 변수의 타입이 정확히 좁혀집니다.
- **생성자에서 `super()` 앞에 코드 작성 허용**: `this`를 참조하지 않는다면 `super()` 호출 전에 다른 코드를 둘 수 있습니다.
- **재귀 타입 검사 개선**: 깊게 중첩된 제네릭 타입의 검사 성능과 정확도가 좋아졌습니다.
- **`--target es2022` 추가**: 클래스 필드, `Array.prototype.at()` 같은 ES2022 기능을 그대로 출력할 수 있습니다.
- **JS 파일 문법 오류 보고 강화**: `// @ts-check`를 쓰지 않은 JavaScript 파일에서도 문법 오류를 알려 줍니다.

---

## 🌐 브라우저 소식

### Cascade Layers(`@layer`) 지원 확산

이번 달 가장 눈에 띈 CSS 소식은 **Cascade Layers**입니다. 2월 초 출시된 **Firefox 97**이 `@layer`를 기본 지원하기 시작했습니다. **Chrome 99 베타**와 **Safari 15.4 베타**에도 포함되었습니다. 덕분에 몇 달 안에 주요 브라우저 모두에서 쓸 수 있을 것으로 보입니다.

```css
@layer reset, base, components, utilities;

@layer components {
  .button { padding: 0.5rem 1rem; }
}
```

명시도(specificity) 싸움이나 `!important` 남발 없이 스타일 우선순위를 '레이어 순서'로 관리할 수 있습니다. 디자인 시스템이나 서드파티 CSS를 다루는 팀이라면 꼭 살펴보세요.

### Safari 15.4 베타: 대규모 업데이트

Safari 15.4 베타는 최근 몇 년 사이 가장 큰 업데이트로 꼽힙니다. 주요 추가 기능은 다음과 같습니다.

- `<dialog>` 요소 지원
- `loading="lazy"` 이미지 지연 로딩
- 새 뷰포트 단위 `svh` / `lvh` / `dvh`: 모바일 주소창 때문에 생기는 `100vh` 문제를 해결합니다.
- `:focus-visible`, `structuredClone()`, `Array.prototype.at()`, `BroadcastChannel`

"Safari가 새로운 IE"라는 오명을 벗으려는 의지가 보이는 릴리스입니다.

### Chrome 98 출시

Chrome 98은 **COLRv1 컬러 폰트**를 지원합니다. 벡터 기반이라 가볍고 그라데이션까지 표현할 수 있는 컬러 폰트 포맷입니다. 같은 시기 공개된 Chrome 99 베타에는 Cascade Layers 외에도 `<input>`의 네이티브 선택기를 코드로 여는 `showPicker()`가 포함되었습니다.

---

## ⚛️ 프레임워크 & 라이브러리

### Next.js 12.1

- **On-demand ISR(베타)**: `res.unstable_revalidate()`로 원하는 시점에 정적 페이지를 다시 생성할 수 있습니다. CMS에서 콘텐츠를 수정하자마자 반영할 수 있게 됩니다.
- **SWC 지원 확대**: styled-components, Emotion, Relay 등의 변환을 SWC로 처리합니다. Jest 설정도 SWC 기반으로 간단해졌습니다.
- **셀프 호스팅 개선**: `output: 'standalone'` 옵션으로 필요한 파일만 추려 배포 용량을 크게 줄일 수 있습니다(실험 기능).

### React 18 막바지 준비

React 18 베타 이후 피드백을 반영하는 작업이 이어지고 있습니다. 머지않아 RC(릴리스 후보)가 나올 것으로 예상됩니다. 미리 준비해 두면 좋은 항목은 다음과 같습니다.

- `createRoot` API 전환
- 자동 배칭(Automatic Batching)
- `startTransition`

---

## 🛠️ 언어 & 툴링

### Node.js 17.5: 실험적 `fetch()` 도입

Node.js 17.5에서 `--experimental-fetch` 플래그로 브라우저와 같은 `fetch()` API를 쓸 수 있게 되었습니다. 내부 구현은 undici 기반입니다. 이제 `node-fetch`나 `axios` 없이도 서버와 클라이언트에서 같은 코드를 쓰는 날이 가까워졌습니다.

### Vite 2.8

Vite 2.8에서는 Web Worker 처리 방식이 개선되었고, 설치 용량이 줄었습니다. 앞서 말했듯 Vue 공식 추천 도구가 되면서 Vite의 존재감은 더 커질 전망입니다.

### Deno 1.19

`deno vendor` 명령이 추가되어 원격 의존성을 로컬로 내려받아 관리할 수 있습니다. 진단 메시지도 개선되었습니다.

### ES2022 기능 윤곽 확정

TC39에서 Stage 4에 도달한 기능들로 ES2022의 구성이 사실상 정해졌습니다.

- **클래스**: 클래스 필드, private 메서드, static 블록
- **비동기**: Top-level `await`
- **배열·객체 유틸**: `Array.prototype.at()`, `Object.hasOwn()`
- **에러 처리**: Error `cause`
- **정규식**: RegExp 매치 인덱스(`/d` 플래그)

대부분은 이미 최신 브라우저에서 쓸 수 있습니다.

---

## 📌 이달의 한 줄 팁

```js
// 배열의 마지막 요소, 이제는 이렇게!
const last = items.at(-1);
```

`items[items.length - 1]`과는 이제 작별해도 좋습니다. 단, 구형 Safari를 지원해야 한다면 폴리필을 확인하세요.

---

## ✍️ 마치며

2022년 2월은 "기다리던 것들이 도착한 달"이었습니다. Vue 3의 기본 버전 전환, 브라우저 간 CSS 기능 격차 축소, Node.js의 웹 표준 API 수용까지 모두 같은 방향을 가리킵니다. **표준을 따르는 코드가 점점 더 많은 곳에서 그대로 돌아가는 시대**가 오고 있다는 것입니다.

다음 호에서는 3월 출시가 예정된 Chrome 99·Safari 15.4 정식 버전과 React 18 소식을 더 자세히 다루겠습니다. 다음 달에 다시 만나요! 👋

---

*이 뉴스레터가 유익했다면 동료에게 공유해 주세요. 피드백과 소식 제보는 언제나 환영합니다.*
