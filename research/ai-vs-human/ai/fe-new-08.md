# 프론트엔드 월간 소식 — 2024-12

> 한 해를 마무리하는 12월에도 큰 릴리스가 이어졌습니다. 이번 호에서는 React 19 정식 출시 소식을 먼저 다루고, Astro 5와 Next.js 15.1, Node.js의 `require(esm)` 기본 활성화를 이어서 소개합니다. 지난달 말에 나온 주요 릴리스도 짧게 정리했습니다.

---

## 🔥 이달의 헤드라인: React 19 정식 출시

2024년 4월 RC가 공개된 뒤 오래 기다렸던 **React 19**가 12월 5일 stable로 출시되었습니다.

### 주요 변화

- **Actions**: 비동기 함수를 transition 안에서 실행하면 pending 상태, 에러 처리, 낙관적 업데이트를 React가 관리합니다. `<form action={fn}>`처럼 폼에 함수를 바로 넘길 수도 있습니다.
- **새로운 훅**: `useActionState`, `useOptimistic`, 그리고 react-dom의 `useFormStatus`가 추가되었습니다.
- **`use` API**: 렌더링 중에 Promise나 Context를 읽을 수 있습니다. 조건문 안에서도 호출할 수 있다는 점이 기존 훅과 다릅니다.
- **`ref`를 prop으로 전달**: 함수 컴포넌트에서 `forwardRef` 없이 `ref`를 받을 수 있습니다. `forwardRef`는 앞으로 deprecated될 예정입니다.
- **`<Context>`를 Provider로 사용**: `<ThemeContext.Provider>` 대신 `<ThemeContext>`라고 쓰면 됩니다.
- **문서 메타데이터 지원**: 컴포넌트 안에 `<title>`, `<meta>`, `<link>`를 쓰면 `<head>`로 자동으로 옮겨집니다.
- **Server Components와 Server Actions 안정화**: 프레임워크 차원에서 사용할 수 있는 수준이 되었습니다.

### 업그레이드 팁

공식 블로그의 업그레이드 가이드와 codemod(`npx codemod@latest react/19/migration-recipe`)를 함께 사용하는 것을 권합니다. `propTypes`, 문자열 ref, 레거시 Context처럼 오래전에 deprecated된 API는 이번에 제거되었습니다. 라이브러리 의존성이 많은 프로젝트라면 React 18.3으로 먼저 올려서 경고를 확인한 뒤 넘어가는 편이 안전합니다.

---

## 🚀 Astro 5.0: Content Layer와 Server Islands

12월 3일 출시된 **Astro 5.0**은 콘텐츠 중심 사이트를 만드는 방식을 크게 바꾼 릴리스입니다.

- **Content Layer API**: 로컬 Markdown뿐 아니라 CMS나 API 같은 외부 소스에서도 loader로 콘텐츠를 가져와 타입이 지정된 컬렉션으로 관리할 수 있습니다. 대규모 사이트의 빌드 속도와 메모리 사용량도 크게 개선되었다고 합니다.
- **Server Islands**: 정적 페이지 안에서 일부 영역만 서버에서 늦게 렌더링합니다. 개인화된 영역을 분리해 페이지 전체의 캐시 효율을 유지할 수 있습니다.
- **`astro:env`**: 타입 안전한 환경 변수 모듈이 정식 기능이 되었습니다.
- 기존 `hybrid` 출력 모드가 `static`으로 통합되어 사전 렌더링 설정이 단순해졌습니다.

---

## ⚡ Next.js 15.1

12월 10일 공개된 **Next.js 15.1**은 React 19 stable을 공식 지원합니다.

- **`after()` API 안정화**: 응답을 보낸 뒤에 로깅이나 분석 같은 작업을 실행할 수 있습니다.
- **`forbidden()` / `unauthorized()`**(실험적): 403·401 상황을 `notFound()`처럼 다룰 수 있습니다.
- 에러 오버레이와 스택 트레이스가 개선되어 디버깅이 한결 쉬워졌습니다.

---

## 🟢 Node.js 22.12: `require(esm)` 기본 활성화

Node.js 23에서 먼저 플래그 없이 쓸 수 있게 된 **`require(esm)`**이 LTS 라인인 **22.12.0**에도 백포트되어 기본으로 활성화되었습니다. 이제 CommonJS 코드에서 동기 ES 모듈을 `require()`로 불러올 수 있습니다. 덕분에 라이브러리 작성자가 CJS와 ESM을 함께 배포해야 하는 부담이 줄어들 것으로 보입니다. 다만 top-level `await`를 사용하는 모듈은 `require()`로 불러올 수 없으니 주의하세요.

---

## 📦 지난달 놓친 릴리스 한눈에 보기

| 프로젝트 | 핵심 내용 |
|---|---|
| **Vite 6** | 실험적인 Environment API 도입으로 SSR과 엣지 런타임 같은 다중 환경 지원 강화, Node 18·20·22+ 지원 |
| **Angular 19** | standalone이 기본값이 됨, 증분 하이드레이션(developer preview), `linkedSignal`, `resource` API |
| **TypeScript 5.7** | 초기화되지 않은 변수 검사 강화, `--target es2024`, `--rewriteRelativeImportExtensions` |
| **React Router v7** | Remix와 통합되어 라이브러리 모드와 프레임워크 모드를 함께 제공, 타입 안전한 라우트 모듈 |
| **Tailwind CSS v4 베타** | 새 엔진 Oxide, CSS 우선 설정(`@theme`), 정식 출시를 앞두고 베타 업데이트가 이어지는 중 |

---

## 📊 State of JavaScript 2024 결과 공개

연례 개발자 설문인 **State of JavaScript 2024** 결과가 공개되었습니다. 눈에 띄는 흐름은 다음과 같습니다.

- **TypeScript 사용이 기본이 된 흐름**이 이어졌습니다. 상당수 응답자가 코드 대부분을 TypeScript로 작성한다고 답했습니다.
- 빌드 도구에서는 **Vite**가 사용률과 만족도 모두 상위권을 지켰습니다.
- 프레임워크 사용률은 React가 여전히 압도적이지만, 만족도와 관심도에서는 **Svelte**와 **Solid** 같은 대안이 꾸준히 높은 점수를 받았습니다.
- 메타 프레임워크 영역에서는 Next.js 사용률이 높은 반면, 만족도에서는 Astro가 강세를 보였습니다.

우리 팀이 쓰는 기술 스택을 이 결과와 비교해 보는 것도 연말 회고에 도움이 될 것입니다.

---

## 🎄 그 밖의 소식

- **Advent of Svelte**: Svelte 팀이 12월 한 달 동안 매일 새 기능이나 개선 사항을 하나씩 공개하는 이벤트를 열었습니다. Svelte 5 출시 이후 개발 속도가 빨라진 모습입니다.
- **"JavaScript" 상표권 논쟁**: Deno가 Oracle의 "JavaScript" 상표 취소를 요구하며 미국 특허청에 제기한 청원이 계속 화제가 되고 있습니다. 개발자 커뮤니티의 지지 서명도 이어지고 있습니다.

---

## ✍️ 편집자 노트

2024년은 React 19, Svelte 5, Angular 19, Vite 6, Astro 5처럼 주요 도구의 메이저 버전이 연이어 나온 해였습니다. 큰 흐름을 보면 **서버와 클라이언트의 경계를 다시 설계**하는 움직임(Server Components, Server Islands, 증분 하이드레이션)과 **설정을 줄이고 기본값을 개선**하는 움직임이 함께 나타났습니다.

새해에는 Tailwind CSS v4 정식 출시와 Vite 생태계의 Environment API 확산이 기대됩니다. 업그레이드는 서두르지 말고 단계적으로 진행하세요.

올 한 해도 함께해 주셔서 감사합니다. 다음 호에서 뵙겠습니다! 🎉
