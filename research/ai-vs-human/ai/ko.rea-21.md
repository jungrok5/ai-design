# 점진적 도입

React Compiler는 기존 코드베이스에 한 번에 적용하지 않고 단계적으로 도입할 수 있습니다. 이 페이지에서는 컴파일러를 안전하게 조금씩 적용하는 여러 방법을 알아봅니다.

<Intro>

이미 운영 중인 애플리케이션에 컴파일러를 적용할 때는 작은 범위에서 시작해 점차 넓혀 가는 편이 안전합니다. React Compiler는 컴파일 대상을 직접 정할 수 있는 여러 방법을 제공합니다.

</Intro>

<YouWillLearn>

* 점진적 도입이 권장되는 이유
* Babel의 `overrides`로 특정 디렉터리에만 컴파일러를 적용하는 방법
* 어노테이션 모드로 개별 함수를 직접 선택하는 방법
* 런타임 게이팅으로 기능 플래그와 함께 컴파일러를 사용하는 방법

</YouWillLearn>

---

## 왜 점진적으로 도입해야 하나요? {/*why-incremental-adoption*/}

React Compiler는 코드베이스 전체를 자동으로 최적화하도록 설계되었습니다. 하지만 기존 애플리케이션 전체에 한 번에 적용하는 것은 부담이 될 수 있습니다. 특히 다음과 같은 경우에는 단계적으로 도입하는 것이 좋습니다.

* 규모가 큰 코드베이스에서 변경의 영향을 단계별로 확인하고 싶을 때
* [React의 규칙](/reference/rules)을 지키지 않는 코드가 섞여 있을 수 있을 때
* 운영 환경에서 성능 변화를 측정하며 적용 범위를 조절하고 싶을 때

점진적으로 도입하면 문제가 생겼을 때 원인을 빨리 찾을 수 있고, 팀도 새로운 방식에 천천히 익숙해질 수 있습니다.

## 점진적 도입 방법 {/*approaches-to-incremental-adoption*/}

컴파일러를 점진적으로 도입하는 주요 방법은 세 가지입니다.

1. **디렉터리 기반 도입** — 특정 디렉터리에만 컴파일러를 적용합니다.
2. **어노테이션 모드** — `"use memo"` 지시어를 붙인 컴포넌트와 Hook만 컴파일합니다.
3. **런타임 게이팅** — 기능 플래그로 실행 시점에 컴파일된 코드를 쓸지 결정합니다.

각 방법은 함께 사용할 수 있습니다. 프로젝트 상황에 맞게 골라 쓰세요.

---

## Babel overrides를 이용한 디렉터리 기반 도입 {/*directory-based-adoption*/}

Babel의 `overrides` 옵션을 사용하면 코드베이스의 일부에만 플러그인을 적용할 수 있습니다. 새로 작성한 코드나 상대적으로 독립적인 디렉터리부터 시작하는 것이 좋습니다.

```js {3-8}
// babel.config.js
module.exports = {
  plugins: [
    // 모든 파일에 적용되는 전역 플러그인
  ],
  overrides: [
    {
      test: './src/modern/**/*.{js,jsx,ts,tsx}',
      plugins: [
        'babel-plugin-react-compiler'
      ]
    }
  ]
};
```

해당 디렉터리에서 문제가 없음을 확인했다면 대상 디렉터리를 하나씩 추가해 나가면 됩니다.

```js
overrides: [
  {
    test: ['./src/modern/**/*.{js,jsx,ts,tsx}', './src/features/**/*.{js,jsx,ts,tsx}'],
    plugins: ['babel-plugin-react-compiler']
  }
]
```

컴파일러 옵션도 디렉터리마다 다르게 지정할 수 있습니다.

```js
overrides: [
  {
    test: './src/experimental/**/*.{js,jsx,ts,tsx}',
    plugins: [
      ['babel-plugin-react-compiler', {
        // 옵션
      }]
    ]
  }
]
```

---

## 어노테이션 모드 사용하기 {/*opt-in-mode-with-use-memo*/}

가장 세밀하게 제어하고 싶다면 `compilationMode: 'annotation'` 옵션을 사용하세요. 이 모드에서는 `"use memo"` 지시어로 직접 선택한 컴포넌트와 Hook만 컴파일됩니다.

```js
// babel.config.js
module.exports = {
  plugins: [
    ['babel-plugin-react-compiler', {
      compilationMode: 'annotation',
    }],
  ],
};
```

컴파일할 함수 본문의 맨 처음에 `"use memo"`를 추가합니다.

```js {2,7}
function TodoList({ todos }) {
  "use memo"; // 이 컴포넌트를 컴파일 대상으로 지정합니다
  // ...
}

function useSortedData(data) {
  "use memo"; // 이 Hook을 컴파일 대상으로 지정합니다
  return data.slice().sort();
}
```

이 방식은 영향 범위를 한눈에 파악할 수 있어서 성능이 중요한 컴포넌트만 골라 최적화하고 싶을 때 유용합니다. 컴파일러를 충분히 검증했다면 `compilationMode`를 기본값으로 되돌려 전체 코드에 적용하면 됩니다.

<Note>

반대로 특정 컴포넌트를 컴파일 대상에서 빼야 한다면 `"use no memo"` 지시어를 사용하세요. 문제가 있는 컴포넌트를 임시로 제외하는 탈출구이므로, 원인을 해결한 뒤에는 지시어를 제거하는 것이 좋습니다.

</Note>

---

## 런타임 게이팅 사용하기 {/*runtime-feature-flags-with-gating*/}

`gating` 옵션을 사용하면 **실행 시점에** 기능 플래그 값에 따라 컴파일된 코드와 원본 코드 중 하나를 고를 수 있습니다. A/B 테스트를 하거나 사용자 일부에게만 먼저 적용할 때 유용합니다.

### 동작 방식 {/*how-gating-works*/}

컴파일러는 최적화된 코드를 런타임 검사로 감쌉니다. 게이트가 `true`를 반환하면 최적화된 버전이, `false`를 반환하면 원본 코드가 실행됩니다.

```js
// 컴파일 결과(개념적 예시)
const Button = isCompilerEnabled() ? Button_optimized : Button_original;
```

### 게이팅 설정하기 {/*gating-configuration*/}

```js
// babel.config.js
module.exports = {
  plugins: [
    ['babel-plugin-react-compiler', {
      gating: {
        source: 'ReactCompilerFeatureFlags',
        importSpecifierName: 'isCompilerEnabled',
      },
    }],
  ],
};
```

### 기능 플래그 구현하기 {/*implementing-the-feature-flag*/}

게이트 함수를 내보내는 모듈을 만듭니다.

```js
// ReactCompilerFeatureFlags.js
export function isCompilerEnabled() {
  // 사용 중인 기능 플래그 시스템을 활용하세요
  return getFeatureFlag('react-compiler-enabled');
}
```

이렇게 하면 다시 배포하지 않고도 컴파일러를 켜거나 끌 수 있고, 두 버전의 성능을 직접 비교할 수도 있습니다.

---

## 도입 중 문제 해결하기 {/*troubleshooting-adoption*/}

컴파일러를 적용한 뒤 문제가 생기면 다음 순서로 확인해 보세요.

1. `"use no memo"`로 문제가 되는 컴포넌트를 임시로 제외합니다.
2. 해당 컴포넌트가 React의 규칙을 지키는지 확인합니다.
3. ESLint 플러그인으로 규칙 위반을 찾아 수정합니다.
4. 문제를 해결했다면 지시어를 제거하고 다시 컴파일 대상에 포함합니다.

## 다음 단계 {/*next-steps*/}

* [설정 가이드](/reference/react/compiler/configuration)에서 더 많은 옵션을 살펴보세요.
* [디버깅 가이드](/learn/react-compiler/debugging)에서 문제 해결 방법을 알아보세요.
