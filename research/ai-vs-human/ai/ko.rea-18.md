# preinit

`preinit`를 사용하면 스타일시트나 외부 스크립트를 미리 가져와서 실행할 수 있습니다.

```js
preinit("https://example.com/script.js", {as: "script"});
```

---

## 레퍼런스 {/*reference*/}

### `preinit(href, options)` {/*preinit*/}

스크립트나 스타일시트를 미리 초기화하려면 `react-dom`에서 `preinit` 함수를 호출하세요.

```js
import { preinit } from 'react-dom';

function AppRoot() {
  preinit("https://example.com/script.js", {as: "script"});
  // ...
}
```

`preinit` 함수는 지정한 리소스를 다운로드하고 실행하라는 힌트를 브라우저에 보냅니다. 이렇게 하면 시간을 아낄 수 있습니다.

#### 매개변수 {/*parameters*/}

* `href`: 문자열. 다운로드하고 실행할 리소스의 URL입니다.
* `options`: 객체. 다음 속성을 포함합니다.
  * `as`: 필수 문자열. 리소스의 유형이며 `'script'`와 `'style'` 중 하나입니다.
  * `precedence`: 문자열. 스타일시트에는 필수입니다. 다른 스타일시트와 비교해 이 스타일시트를 어디에 넣을지 정합니다. 우선순위가 높은 스타일시트는 낮은 스타일시트의 규칙을 덮어쓸 수 있습니다. 가능한 값은 `reset`, `low`, `medium`, `high`입니다.
  * `crossOrigin`: 문자열. 사용할 [CORS 정책](https://developer.mozilla.org/ko/docs/Web/HTML/Attributes/crossorigin)이며 `anonymous`와 `use-credentials` 중 하나입니다.
  * `integrity`: 문자열. 리소스의 [진위 여부를 확인](https://developer.mozilla.org/ko/docs/Web/Security/Subresource_Integrity)하는 데 쓰는 암호화 해시입니다.
  * `nonce`: 문자열. 엄격한 콘텐츠 보안 정책(CSP)을 사용할 때 [리소스를 허용](https://developer.mozilla.org/ko/docs/Web/HTML/Global_attributes/nonce)하기 위한 암호화 nonce입니다.
  * `fetchPriority`: 문자열. 리소스를 가져올 때의 상대적 우선순위를 제안합니다. 가능한 값은 `auto`(기본값), `high`, `low`입니다.

#### 반환값 {/*returns*/}

`preinit`은 아무것도 반환하지 않습니다.

#### 주의 사항 {/*caveats*/}

* 같은 `href`로 `preinit`을 여러 번 호출해도 한 번 호출한 것과 결과가 같습니다.
* 브라우저에서는 컴포넌트를 렌더링할 때, Effect 안에서, 이벤트 핸들러 안에서 등 어떤 상황에서든 `preinit`을 호출할 수 있습니다.
* 서버 측 렌더링이나 서버 컴포넌트를 렌더링할 때는 두 경우에만 `preinit`이 효과가 있습니다. 컴포넌트를 렌더링하는 도중에 호출하거나, 컴포넌트 렌더링에서 시작된 비동기 컨텍스트 안에서 호출하는 경우입니다. 그 밖의 경우에 호출하면 무시됩니다.

---

## 사용법 {/*usage*/}

### 렌더링할 때 미리 초기화하기 {/*preiniting-when-rendering*/}

어떤 컴포넌트나 그 자식 컴포넌트가 특정 리소스를 사용하고, 그 리소스를 다운로드한 뒤 바로 실행해도 괜찮다면 컴포넌트를 렌더링할 때 `preinit`을 호출하세요.

#### 외부 스크립트 미리 초기화하기 {/*preiniting-an-external-script*/}

```js
import { preinit } from 'react-dom';

function AppRoot() {
  preinit("https://example.com/script.js", {as: "script"});
  return ...;
}
```

스크립트를 다운로드만 하고 바로 실행하지는 않으려면 [`preload`](/reference/react-dom/preload)를 사용하세요. ESM 모듈을 불러오려면 [`preinitModule`](/reference/react-dom/preinitModule)을 사용하세요.

#### 스타일시트 미리 초기화하기 {/*preiniting-a-stylesheet*/}

```js
import { preinit } from 'react-dom';

function AppRoot() {
  preinit("https://example.com/style.css", {as: "style", precedence: "medium"});
  return ...;
}
```

`precedence` 옵션은 필수입니다. 이 옵션으로 문서 안에서 스타일시트의 순서를 정할 수 있습니다. 우선순위가 높은 스타일시트는 낮은 스타일시트를 덮어쓸 수 있습니다.

스타일시트를 다운로드만 하고 바로 문서에 넣지는 않으려면 [`preload`](/reference/react-dom/preload)를 사용하세요.

### 이벤트 핸들러에서 미리 초기화하기 {/*preiniting-in-an-event-handler*/}

외부 리소스가 필요한 페이지나 상태로 전환하기 전에 이벤트 핸들러에서 `preinit`을 호출하세요. 새 페이지나 상태를 렌더링할 때 호출하는 것보다 더 일찍 작업을 시작할 수 있습니다.

```js
import { preinit } from 'react-dom';

function CallToAction() {
  const onClick = () => {
    preinit("https://example.com/wizardStyles.css", {as: "style", precedence: "medium"});
    startWizard();
  }
  return (
    <button onClick={onClick}>Start Wizard</button>
  );
}
```
