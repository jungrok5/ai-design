# 🗞️ 프론트엔드 월간 뉴스레터 — 2024-06

안녕하세요, 구독자 여러분! 6월에는 큰 발표가 많았습니다. TypeScript 5.5가 정식 출시됐고, ECMAScript 2024가 표준으로 승인됐습니다. WWDC에서는 Safari 18 베타가 공개됐고, React 19 RC는 동작 방식 하나를 두고 논쟁이 벌어졌습니다. 이번 호에서 하나씩 정리했습니다.

---

## 1. TypeScript 5.5 정식 출시 🎉

6월 20일에 TypeScript 5.5가 나왔습니다. 일상적인 코드 작성에서 바로 체감할 수 있는 개선이 많습니다.

- **타입 술어 추론(Inferred Type Predicates)**: 이제 `filter(x => x !== undefined)` 같은 코드에서 결과 배열의 타입이 자동으로 좁혀집니다. `x is T`를 직접 쓰지 않아도 됩니다.
- **정규식 문법 검사**: 정규식 리터럴의 문법 오류를 컴파일 단계에서 잡아 줍니다.
- **`isolatedDeclarations` 옵션**: 다른 도구가 타입 검사기 없이 선언 파일(`.d.ts`)을 병렬로 만들 수 있습니다. 대규모 모노레포의 빌드 속도를 높이는 데 도움이 됩니다.
- **JSDoc `@import` 태그**: JS 파일에서 타입만 가져와 쓰기가 편해졌습니다.

```ts
const nums = [1, 2, undefined, 4].filter(n => n !== undefined);
// 5.4: (number | undefined)[]
// 5.5: number[]  ✅
```

---

## 2. ECMAScript 2024 표준 승인

6월 말 Ecma 총회에서 **ES2024**가 공식 승인됐습니다. 주요 내용은 다음과 같습니다.

- `Object.groupBy` / `Map.groupBy`: 배열을 기준에 따라 그룹으로 묶습니다. lodash의 `groupBy`가 언어에 기본으로 들어온 셈입니다.
- `Promise.withResolvers()`: `resolve`와 `reject`를 바깥으로 꺼내 쓰는 패턴을 표준 방식으로 쓸 수 있습니다.
- 정규식 `v` 플래그: 집합 연산과 유니코드 문자열 속성을 지원합니다.
- 크기를 바꿀 수 있는 `ArrayBuffer`와 `transfer()` 메서드
- `String.prototype.isWellFormed()` / `toWellFormed()`

대부분 주요 브라우저에서 이미 쓸 수 있습니다. 이번 승인으로 표준 지위가 확정됐다고 보면 됩니다.

---

## 3. React 19 RC와 Suspense 논쟁

React 19 RC에서 **Suspense 경계 안의 형제 컴포넌트를 미리 렌더링하지 않도록** 바뀐 점이 6월 중순 커뮤니티에서 크게 논란이 됐습니다. 이 때문에 컴포넌트마다 따로 데이터를 가져오는 구조에서는 요청이 병렬로 나가지 않고 차례로 하나씩 실행되는 **워터폴 문제**가 생길 수 있다는 지적이 나왔습니다.

React 팀은 이 의견을 받아들여 **더 나은 해법을 찾을 때까지 19 정식 출시를 미루겠다**고 밝혔습니다. RC 단계에서 커뮤니티 피드백이 실제 결정에 반영된 사례입니다. React 19를 도입하려는 팀은 데이터 패칭 구조를 미리 점검해 두는 것이 좋습니다.

> 💡 참고: 5월 말에 나온 **Next.js 15 RC**는 React 19 RC를 기반으로 합니다. 캐싱 기본값이 바뀌었고(`fetch`와 GET 라우트 핸들러를 기본으로 캐싱하지 않음), React Compiler를 실험적으로 지원합니다.

---

## 4. 브라우저 소식: View Transitions 확산 🌐

### Safari 18 베타 (WWDC24)
6월 10일 WWDC에서 Safari 18 베타가 공개됐습니다. 가장 큰 소식은 **View Transitions API**(같은 문서 내 전환) 지원입니다. 진입 애니메이션을 CSS만으로 만들 수 있게 해 주는 `@starting-style`도 지원 목록에 들어갔습니다.

### Chrome 126
6월 11일 정식 출시된 Chrome 126은 **문서 간(cross-document) View Transitions**를 지원합니다. 같은 출처(same-origin)의 MPA에서도 CSS 몇 줄로 페이지 전환 애니메이션을 넣을 수 있습니다.

```css
@view-transition {
  navigation: auto;
}
```

이제 SPA 프레임워크가 없어도 앱처럼 부드러운 화면 전환을 만들 수 있습니다. 블로그나 문서 사이트처럼 MPA로 만든 서비스에서 시도해 볼 만합니다.

---

## 5. 프레임워크 업데이트 모음 📦

| 프레임워크 | 소식 |
|---|---|
| **Nuxt 3.12** | `compatibilityVersion: 4` 옵션으로 Nuxt 4의 변경 사항을 미리 적용해 볼 수 있습니다. |
| **Angular 18** (5월 말) | Zone.js 없이 동작하는 zoneless 모드 실험 지원, Material 3와 Deferrable Views 안정화 |
| **Remix → React Router v7** | Remix의 기능을 React Router v7로 합치는 계획이 발표돼 마이그레이션 경로에 관심이 모이고 있습니다. |
| **Astro 4.10** | 타입 안전한 환경 변수 API(`astro:env`)를 실험적으로 도입 |

---

## 6. 이달의 실무 팁 ✍️

**ESLint 9 Flat Config 마이그레이션, 아직 안 하셨나요?**
4월에 나온 ESLint 9부터 `eslint.config.js`(Flat Config)가 기본 설정 방식입니다. 기존 `.eslintrc` 방식은 사용 중단(deprecated) 상태입니다. 공식 마이그레이션 도구를 쓰면 기존 설정을 상당 부분 자동으로 바꿀 수 있습니다.

```bash
npx @eslint/migrate-config .eslintrc.json
```

플러그인마다 Flat Config 지원 상황이 다르므로, 바꾸기 전에 의존성을 하나씩 확인하세요.

---

## 📌 이번 호 요약

1. **TypeScript 5.5**: 타입 술어 추론 덕분에 `filter` 결과 타입이 자동으로 좁혀집니다.
2. **ES2024 승인**: `groupBy`, `Promise.withResolvers`가 표준이 됐습니다.
3. **React 19**: Suspense 동작 논쟁으로 정식 출시가 미뤄졌습니다.
4. **View Transitions**: Safari와 Chrome 모두에서 지원이 넓어졌습니다.

다음 호에서는 7월 소식을 전해 드리겠습니다. 의견이나 다루었으면 하는 주제가 있으면 언제든 회신해 주세요. 감사합니다! 🙌

---

본문은 약 3,000자입니다. 메일로 보내거나 팀에 공유할 거라면 HTML 페이지로도 만들어 드릴 수 있습니다.
