# template (Lodash 호환성)

`template` 함수는 문자열 템플릿을 컴파일해 데이터를 바인딩한 결과 문자열을 만드는 함수입니다. Lodash의 `_.template`과 같은 구분자와 옵션을 지원하므로, Lodash 기반 코드를 큰 수정 없이 옮길 수 있습니다.

## 시그니처

```js
template(string, [options]) → Function
```

반환된 함수에 데이터 객체를 전달하면 렌더링된 문자열을 얻을 수 있습니다.

## 구분자

| 구문 | 설명 |
|---|---|
| `<%= value %>` | 값을 그대로 출력합니다 (interpolate) |
| `<%- value %>` | HTML 특수문자를 이스케이프하여 출력합니다 (escape) |
| `<% code %>` | JavaScript 코드를 실행합니다 (evaluate) |
| `${ value }` | ES 템플릿 스타일 보간입니다. `interpolate` 옵션으로 변경할 수 있습니다. |

## 주요 옵션

| 옵션 | 설명 |
|---|---|
| `escape` | 이스케이프 구분자 정규식 |
| `evaluate` | 평가 구분자 정규식 |
| `interpolate` | 보간 구분자 정규식 |
| `imports` | 템플릿 안에서 사용할 함수나 객체 |
| `variable` | 데이터를 받을 변수 이름입니다. 지정하면 `with` 문을 사용하지 않습니다. |
| `sourceURL` | 디버깅용 소스 URL |

## 예제

```js
const compiled = template('안녕하세요, <%= name %>님! <%- html %>');

compiled({ name: '민수', html: '<b>&</b>' });
// '안녕하세요, 민수님! &lt;b&gt;&amp;&lt;/b&gt;'
```

## Lodash 호환 사항

- 구분자, `imports`, `variable` 옵션의 의미가 Lodash와 같습니다.
- `<%= %>`에 `null`이나 `undefined`를 넘기면 빈 문자열로 출력됩니다.
- 데이터에 없는 키를 참조하면 `ReferenceError`가 발생합니다.

## 주의 사항

- `<% %>` 구문은 임의의 JavaScript 코드를 실행하므로, 신뢰할 수 있는 템플릿 문자열만 사용하세요.
- 사용자 입력을 템플릿 소스로 직접 컴파일하지 마세요. 값으로 전달하는 것은 안전하지만, 소스 자체를 입력받으면 코드 주입 위험이 있습니다.
