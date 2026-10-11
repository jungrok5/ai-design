# exec

정규식을 문자열 전체에 적용하고, 일치하는 결과를 모두 배열로 반환합니다. 기본 `RegExp.prototype.exec`를 반복 호출할 때 생기는 `lastIndex` 관리 문제나 무한 루프 걱정 없이 모든 일치 항목을 한 번에 얻을 수 있습니다.

## 문법

```js
exec(pattern, input)
```

## 매개변수

| 이름 | 타입 | 설명 |
| --- | --- | --- |
| `pattern` | `RegExp \| string` | 검색할 정규식입니다. 문자열을 넘기면 정규식으로 변환합니다. |
| `input` | `string` | 검색 대상 문자열입니다. |

## 반환값

`Array<Match>`: 일치 항목 객체의 배열입니다. 일치하는 항목이 없으면 빈 배열을 반환합니다.

각 `Match` 객체에는 다음 속성이 있습니다.

- `value`: 일치한 전체 문자열
- `index`: 입력 문자열에서 일치가 시작된 위치
- `groups`: 이름 있는 캡처 그룹 객체(없으면 `{}`)
- `captures`: 번호 캡처 그룹 값의 배열

## 예제

```js
import { exec } from 'my-utils';

const text = '2024-01-15, 2025-03-02';
const result = exec(/(?<year>\d{4})-(\d{2})-(\d{2})/, text);

console.log(result.length);          // 2
console.log(result[0].value);        // '2024-01-15'
console.log(result[0].groups.year);  // '2024'
console.log(result[1].captures);     // ['2025', '03', '02']
```

## 동작 방식

- `pattern`에 `g` 플래그가 없으면 내부에서 자동으로 추가합니다. 원본 정규식 객체는 수정하지 않습니다.
- 빈 문자열과 일치하는 패턴(예: `/a*/`)도 무한 루프에 빠지지 않습니다. 빈 일치가 나오면 다음 위치로 한 칸씩 이동합니다.
- `input`이 문자열이 아니면 `TypeError`를 던집니다.

## 주의 사항

- 매우 긴 문자열에 복잡한 패턴을 적용하면 결과 배열이 커질 수 있습니다. 첫 번째 일치만 필요하다면 `String.prototype.match`나 기본 `exec`를 사용하는 편이 효율적입니다.
- 문자열로 패턴을 넘기면 특수 문자는 이스케이프되지 않습니다. 리터럴 검색이 필요하면 `escapeRegExp`와 함께 사용하세요.

## 관련 항목

- `test`: 일치 여부만 불리언으로 반환합니다.
- `replaceAll`: 일치 항목을 일괄 치환합니다.
- `escapeRegExp`: 정규식 특수 문자를 이스케이프합니다.
