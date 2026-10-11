# 프론트엔드 월간 소식 | 2024-07

안녕하세요, 이번 호에서는 2024년 6월 말부터 7월 초까지 프론트엔드 생태계에서 눈여겨볼 소식을 정리했습니다. 언어 표준, 프레임워크, 브라우저, 보안, 실무 팁 순서입니다.

> 참고: 버전과 날짜는 발행 전에 공식 릴리스 노트로 한 번 더 확인해 주세요.

---

## 📌 이번 호 한눈에 보기

- **ES2024** 표준 확정
- **TypeScript 5.5** 안정 버전 안착
- **React 19**는 RC 단계, 업그레이드 준비
- **Polyfill.io** 공급망 공격 사건
- 브라우저 릴리스: Firefox 128, Chrome 127, Safari 18 베타

---

## 1. 언어·표준: ES2024 확정

6월 말 Ecma 총회에서 **ECMAScript 2024**가 승인되었습니다. 실무에서 바로 쓸 만한 기능은 다음과 같습니다.

- `Object.groupBy` / `Map.groupBy`: 배열을 기준에 따라 그룹으로 묶습니다. 이제 `reduce`로 직접 구현하지 않아도 됩니다.
- `Promise.withResolvers()`: `resolve`와 `reject`를 바깥에서 쓸 수 있어, 이벤트 기반 코드를 Promise로 감쌀 때 편합니다.
- 정규식 `v` 플래그: 유니코드 집합 연산을 지원합니다.
- 크기 조절이 가능한 `ArrayBuffer`와 `Atomics.waitAsync`

```js
const items = [
  { type: 'fruit', name: '사과' },
  { type: 'veg', name: '당근' },
  { type: 'fruit', name: '배' },
];

const grouped = Object.groupBy(items, (item) => item.type);
// { fruit: [...], veg: [...] }
```

브라우저별 지원 범위가 다르니 도입 전에 지원 현황을 확인하고, 필요하면 트랜스파일이나 폴리필 전략을 함께 정하세요.

---

## 2. 도구: TypeScript 5.5

6월 중순에 나온 **TypeScript 5.5**를 팀 프로젝트에 적용해 볼 시기입니다.

- **추론된 타입 가드(Inferred Type Predicates)**: `filter(x => x !== undefined)` 같은 코드에서 타입 가드를 직접 쓰지 않아도 좁혀진 타입이 추론됩니다.
- **`isolatedDeclarations`**: 선언 파일(.d.ts)을 병렬로 빠르게 생성할 수 있는 기반이 마련되었습니다. 대형 모노레포의 빌드 시간 개선에 기대가 큽니다.
- **정규식 문법 검사**: 정규식 리터럴의 문법 오류를 컴파일 단계에서 잡아 줍니다.

업그레이드할 때는 `strict` 관련 에러가 늘어날 수 있으니, CI에서 먼저 돌려 보고 점진적으로 올리는 편이 안전합니다.

---

## 3. 프레임워크 동향

### React 19
React 19는 RC 단계입니다. 정식 출시 전에 점검하면 좋은 항목은 다음과 같습니다.

- `ref`를 일반 prop처럼 전달하는 방식 (`forwardRef` 단순화)
- Actions와 `useActionState`, `useOptimistic` 같은 폼·비동기 처리 API
- 서버 컴포넌트와 서버 액션의 안정화
- 사용하지 않는 레거시 API 제거에 따른 경고 확인

React 18에서 경고가 나오는 부분을 지금 정리해 두면 마이그레이션 부담이 줄어듭니다.

### Vue
Vue 3.5가 베타 단계에 들어가며 **반응성 시스템 내부 개선**과 메모리 사용량 감소가 주요 주제로 논의되고 있습니다. Props 구조 분해의 반응성 유지 같은 개발 경험 개선도 주목할 만합니다.

### Angular
Angular 18은 **zoneless 변경 감지**를 실험 기능으로 제공하면서 Signals 중심 방향을 더욱 분명히 했습니다. 신규 프로젝트라면 Signals 기반 설계를 염두에 두세요.

---

## 4. 브라우저 소식

| 브라우저 | 소식 |
|---|---|
| Firefox 128 | 7월 초 안정 버전 배포 |
| Chrome 127 | 7월 하순 안정 버전 배포 예정 |
| Safari 18 | WWDC에서 공개, 베타 테스트 중 |

Safari 18 베타에서는 새로운 CSS와 웹 API 지원이 늘고 있습니다. 새 기능은 반드시 **기능 감지(`@supports`, `'기능' in 객체`)** 로 점진적으로 적용하세요. 지원 여부는 [MDN](https://developer.mozilla.org)과 [Can I use](https://caniuse.com)에서 확인할 수 있습니다.

---

## 5. 보안 이슈: Polyfill.io 공급망 공격

6월 말에 알려진 **polyfill.io 도메인 악성 코드 삽입 사건**은 프론트엔드 개발자에게 중요한 교훈을 남겼습니다. 도메인 소유권이 바뀐 뒤, 이 CDN을 불러오던 수많은 사이트에서 사용자를 악성 사이트로 리디렉션하는 코드가 실행될 수 있었습니다.

**점검 체크리스트**

1. 코드베이스에서 `polyfill.io`를 검색해 남아 있는 참조를 제거합니다.
2. 외부 스크립트에는 **SRI(Subresource Integrity)** 속성을 적용합니다.
3. **CSP(Content Security Policy)** 로 허용 출처를 제한합니다.
4. 가능하면 핵심 스크립트는 직접 호스팅하거나 번들에 포함합니다.
5. 믿을 수 있는 대체 미러(Cloudflare, Fastly 등)를 쓰더라도 정기적으로 의존성을 감사합니다.

```html
<script
  src="https://example-cdn.com/lib.min.js"
  integrity="sha384-..."
  crossorigin="anonymous"></script>
```

---

## 6. 이달의 실무 팁

- **번들 크기 점검**: 분기마다 `source-map-explorer`나 번들 분석 도구로 불필요한 의존성을 찾아보세요. 날짜 라이브러리나 유틸 라이브러리를 통째로 가져오는 경우가 흔합니다.
- **Core Web Vitals의 INP**: 3월부터 FID를 대체한 INP(Interaction to Next Paint)를 측정하세요. 긴 작업을 쪼개고 `requestIdleCallback`이나 스케줄링 API를 활용하면 개선됩니다.
- **접근성 기본기**: 시맨틱 태그, 포커스 표시, 키보드 조작만 챙겨도 문제의 상당수를 예방할 수 있습니다.

---

## 7. 읽어 볼 만한 자료

- ECMAScript 2024 제안서 및 TC39 제안 저장소
- TypeScript 5.5 공식 릴리스 노트
- React 블로그의 React 19 업그레이드 가이드
- web.dev의 INP 최적화 가이드
- OWASP의 서드파티 스크립트 보안 권고

---

## ✍️ 마치며

7월 호의 키워드는 **표준의 안정화**와 **공급망 보안**입니다. 새 기능은 빠르게 익히되, 외부 의존성은 한 번 더 의심하는 태도가 필요한 달이었습니다. 다음 호에서는 React 19 정식 출시 소식과 새 브라우저 기능을 더 깊이 다루겠습니다.

의견이나 제보하고 싶은 소식이 있다면 언제든 알려 주세요. 다음 호에서 뵙겠습니다. 🙌

---

본문은 약 3,000자 분량입니다. 날짜와 버전은 제가 아는 범위에서 작성했으니, 발행 전에 공식 릴리스 노트로 확인해 주세요. 특히 Vue 3.5, Angular zoneless, Chrome 127 부분은 한 번 더 확인하시길 권합니다.
