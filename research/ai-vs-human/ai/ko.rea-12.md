# react.dev를 소개합니다

*2023년 3월 16일, Dan Abramov, Rachel Nabors 작성*

---

오늘 React와 React 문서의 새로운 보금자리인 [react.dev](https://react.dev)를 공개합니다. 이 글에서는 새 사이트를 소개하고, 이 사이트를 만든 이유와 앞으로의 방향을 설명합니다.

---

## 요약 {/*tldr*/}

- 새 React 사이트([react.dev](https://react.dev))는 함수 컴포넌트와 Hook으로 최신 React를 가르칩니다.
- 다이어그램, 그림, 챌린지, 그리고 직접 편집할 수 있는 예제 600여 개를 담았습니다.
- 이전 문서 사이트는 [legacy.reactjs.org](https://legacy.reactjs.org)로 옮겼습니다.

## 새 도메인, 새 문서 {/*new-site-new-domain-new-homepage*/}

먼저 정리할 것이 있습니다.

새 문서 공개를 기념해서, 그리고 무엇보다 기존 콘텐츠와 확실히 구분하기 위해 짧은 도메인인 **react.dev**로 옮기기로 했습니다. 기존 **reactjs.org** 주소는 이제 react.dev로 리디렉션됩니다.

기존 React 문서는 [legacy.reactjs.org](https://legacy.reactjs.org)에 보관합니다. 기존 콘텐츠로 연결된 링크는 "링크 깨짐"을 막기 위해 자동으로 그쪽으로 이동하지만, 레거시 문서는 앞으로 거의 업데이트하지 않을 예정입니다.

믿기 어렵겠지만 React는 곧 열 살이 됩니다. JavaScript 기준으로 보면 한 세기가 지난 셈입니다. 그동안 [React 홈페이지](https://react.dev)도 손보아, 오늘날 React로 사용자 인터페이스를 만드는 것이 왜 좋은지 더 잘 드러나도록 했습니다. 오늘날 사람들이 React를 쓰는 방식에 맞추어 시작하기 가이드도 새로 썼습니다.

## 새 문서에서 최신 React를 배우세요 {/*modern-react-with-hooks*/}

2018년 Hook을 공개했을 때, Hook 문서는 독자가 클래스 컴포넌트에 익숙하다고 가정했습니다. 그 덕분에 커뮤니티는 Hook을 빠르게 받아들일 수 있었지만, 시간이 지나면서 기존 문서는 새로 배우는 사람들에게 도움이 되지 못했습니다. 새로 배우는 사람들은 React를 두 번, 즉 클래스 컴포넌트로 한 번, Hook으로 또 한 번 배워야 했습니다.

**새 문서는 처음부터 Hook으로 React를 가르칩니다.** 문서는 크게 두 부분으로 나뉩니다.

- **[React 배우기](/learn)**: 처음부터 React를 배울 수 있는 자기 주도형 강좌입니다.
- **[API 참고서](/reference/react)**: 모든 React API의 세부 사항과 사용 예시를 담았습니다.

각 부분을 자세히 살펴보겠습니다.

> **참고**
>
> 아직 클래스 기반으로 작성된 Hook 문서가 몇 개 남아 있으며, 가까운 시일 내에 업데이트할 예정입니다.

## 빠르게 시작하기 {/*quick-start*/}

이제 학습 섹션은 [빠르게 시작하기](/learn) 페이지로 시작합니다. 짧게 React를 둘러보는 페이지로, 컴포넌트 작성, 데이터 표시, 상태 추가 같은 핵심 개념을 소개합니다.

이 페이지의 코드 예제는 모두 브라우저에서 바로 편집하고 결과를 확인할 수 있습니다. 위에서 아래로 페이지를 따라가며 조금씩 고쳐 보세요.

```js
function MyButton() {
  return (
    <button>I'm a button</button>
  );
}

export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton />
    </div>
  );
}
```

직접 해 보면서 배우는 것을 좋아한다면 [틱택토 튜토리얼](/learn/tutorial-tic-tac-toe)을 이어서 해 보시길 권합니다. React로 작은 게임을 만들면서 매일 쓰게 될 기술을 익힐 수 있습니다.

## React로 생각하기 {/*thinking-in-react*/}

많은 사람이 [React로 생각하기](/learn/thinking-in-react)를 읽고 나서야 React가 "와닿았다"고 말합니다. 아마 가장 오래된 React 안내서일 텐데, 지금도 여전히 유효합니다. 이번에 이 고전적인 안내서를 그 정신은 그대로 살리면서 최신 내용으로 다시 썼습니다.

## 단계별로 배우기 {/*learn-react-step-by-step*/}

학습 섹션은 하나의 커리큘럼처럼 구성되어 있습니다. 각 장은 이전 장의 지식을 바탕으로 이어집니다.

- **[UI 표현하기](/learn/describing-the-ui)**: 컴포넌트, JSX, props로 정보를 표시하는 방법
- **[상호작용성 더하기](/learn/adding-interactivity)**: 이벤트 처리와 상태 관리의 기초
- **[상태 관리하기](/learn/managing-state)**: 상태 구조를 잡고, 컴포넌트 간에 상태를 공유하는 방법
- **[탈출구](/learn/escape-hatches)**: ref와 Effect로 React 바깥과 연결하는 방법

각 장은 개요 페이지로 시작하므로, 이미 아는 내용은 빠르게 확인하고 넘어갈 수 있습니다.

### 챌린지 {/*challenges*/}

대부분의 페이지 마지막에는 챌린지가 있습니다. 배운 내용을 확인할 수 있는 문제로, 막히면 해답을 볼 수도 있습니다. 문제를 풀다 보면 미처 몰랐던 부분을 발견하게 됩니다.

### 다이어그램과 그림 {/*diagrams-and-illustrations*/}

코드와 글만으로 설명하기 어려운 개념에는 다이어그램과 그림을 곁들였습니다. 렌더링 과정, 상태 스냅샷, 컴포넌트 트리 같은 개념을 눈으로 확인할 수 있습니다.

## API 참고서 {/*api-reference*/}

[API 참고서](/reference/react)는 모든 React API의 세부 사항을 담고 있습니다. 각 API 페이지는 두 부분으로 나뉩니다.

1. **참고서**: 함수 시그니처, 매개변수, 반환값, 주의 사항을 간결하게 설명합니다.
2. **사용법**: 실제로 이 API를 쓰는 이유와 방법을 예제와 함께 보여 줍니다.

예를 들어 [`useState`](/reference/react/useState) 페이지는 상태 추가, 이전 상태를 기반으로 업데이트하기, 객체와 배열 업데이트하기 같은 쓰임새를 하나씩 설명합니다. 페이지 끝에는 흔히 겪는 문제와 해결 방법을 정리한 **문제 해결** 섹션도 있습니다.

## 프레임워크로 시작하기 {/*start-a-new-react-project*/}

새 프로젝트를 시작하는 방법도 바뀌었습니다. 이제 새 앱을 만들 때는 [Next.js](https://nextjs.org) 같은 **React 기반 프레임워크**로 시작하기를 권장합니다. 프레임워크는 라우팅, 데이터 가져오기, 서버 렌더링처럼 대부분의 앱에 필요한 기능을 기본으로 제공합니다. 자세한 내용은 [새 React 앱 만들기](/learn/start-a-new-react-project)를 참고하세요.

## 앞으로의 계획 {/*whats-next*/}

이번 공개가 끝이 아닙니다. 앞으로도 남은 레거시 문서를 옮기고 피드백을 반영해 계속 다듬을 예정입니다. 문서에서 잘못된 내용이나 개선할 점을 발견하면 각 페이지 하단의 피드백 버튼을 누르거나 [GitHub 저장소](https://github.com/reactjs/react.dev)에 이슈를 남겨 주세요.

## 감사의 말 {/*thank-you*/}

새 문서는 React 팀만의 작업이 아닙니다. 수많은 커뮤니티 기여자가 원고를 검토하고, 예제를 시험하고, 번역에 참여했습니다. 베타 기간에 피드백을 보내 주신 모든 분께 감사드립니다.

여러분이 새 문서로 즐겁게 React를 배우고 만들기를 바랍니다. 이제 [react.dev](https://react.dev)에서 만나요!

---

이 문서는 2023년 3월 React 공식 블로그 글 "Introducing react.dev"를 바탕으로 다시 쓴 것이고, 원문을 그대로 옮긴 번역은 아닙니다. 공개하실 계획이면 [원문](https://react.dev/blog/2023/03/16/introducing-react-dev)과 함께 날짜, 작성자, 예제 수 같은 세부 내용이 맞는지 확인해 주세요.
