# es-toolkit · [![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/toss/es-toolkit/blob/main/LICENSE) [![codecov](https://codecov.io/gh/toss/es-toolkit/graph/badge.svg?token=8N5S3AR3C7)](https://codecov.io/gh/toss/es-toolkit) [![NPM badge](https://img.shields.io/npm/v/es-toolkit?logo=npm)](https://www.npmjs.com/package/es-toolkit) [![JSR badge](https://jsr.io/badges/@es-toolkit/es-toolkit)](https://jsr.io/@es-toolkit/es-toolkit) [![Discord Badge](https://discord.com/api/guilds/1281071127052943361/widget.png?style=shield)](https://discord.gg/vGXbVjP2nY)

## 개요

es-toolkit은 작고 빠른 최신 JavaScript 유틸리티 라이브러리입니다. Lodash와 비슷한 함수를 제공하며, 트리 셰이킹을 지원하므로 사용하는 함수만 번들에 포함됩니다. TypeScript 타입 정의도 함께 제공됩니다.

## 설치

```bash
npm install es-toolkit
```

JSR을 사용하는 경우 `npx jsr add @es-toolkit/es-toolkit` 명령을 실행합니다.

## 기본 사용법

```js
import { chunk } from 'es-toolkit';

chunk([1, 2, 3, 4, 5], 2);
// [[1, 2], [3, 4], [5]]
```

## API

### chunk(arr, size)

배열을 `size` 길이의 작은 배열로 나눕니다. 마지막 조각은 남은 항목만큼 짧을 수 있습니다.

| 매개변수 | 타입     | 설명               |
| -------- | -------- | ------------------ |
| arr      | `T[]`    | 나눌 배열          |
| size     | `number` | 각 조각의 길이     |

**반환값:** `T[][]`

### groupBy(arr, getKey)

배열의 각 항목을 `getKey` 함수가 반환한 키를 기준으로 묶습니다.

```js
import { groupBy } from 'es-toolkit';

groupBy(['one', 'two', 'three'], s => s.length);
// { 3: ['one', 'two'], 5: ['three'] }
```

### pick(obj, keys)

객체에서 `keys`에 해당하는 속성만 골라 새 객체로 반환합니다.

```js
import { pick } from 'es-toolkit';

pick({ a: 1, b: 2, c: 3 }, ['a', 'c']);
// { a: 1, c: 3 }
```

### range(start, end, step)

`start`부터 `end` 직전까지 `step` 간격의 숫자 배열을 만듭니다. `step`의 기본값은 `1`입니다.

```js
import { range } from 'es-toolkit';

range(0, 4);     // [0, 1, 2, 3]
range(0, 10, 3); // [0, 3, 6, 9]
```

### debounce(func, debounceMs)

마지막 호출 후 `debounceMs` 밀리초가 지나야 `func`를 실행합니다. 반환된 함수에는 `cancel()`과 `flush()` 메서드가 있습니다.

```js
import { debounce } from 'es-toolkit';

const search = debounce(query => fetchResults(query), 300);
input.addEventListener('input', e => search(e.target.value));
```

## Lodash 호환 모드

Lodash에서 옮겨오는 경우 `es-toolkit/compat`에서 Lodash와 같은 인터페이스를 사용할 수 있습니다.

```js
import { chunk } from 'es-toolkit/compat';
```

## 라이선스

es-toolkit은 MIT 라이선스로 배포됩니다. 자세한 내용은 저장소의 LICENSE 파일을 참고하세요.
