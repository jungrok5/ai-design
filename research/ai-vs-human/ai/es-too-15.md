# es-toolkit/compat

`es-toolkit/compat`은 **lodash와 100% 가까운 호환성**을 제공하는 es-toolkit의 별도 진입점입니다. 기존 lodash 코드를 큰 수정 없이 옮기면서도 더 작은 번들 크기와 빠른 성능을 얻을 수 있습니다.

## 개요

es-toolkit의 메인 모듈은 현대적이고 엄격한 타입을 지향하기 때문에, lodash와 동작이 다른 부분이 있습니다. 예를 들어 `null`이나 `undefined` 입력을 허용하지 않고, 문자열 경로(`'a.b.c'`)를 받지 않는 함수도 있습니다. `es-toolkit/compat`은 이런 차이를 메워 lodash의 동작 방식을 그대로 재현합니다.

## 설치

```bash
npm install es-toolkit
```

## 기본 사용법

import 경로만 `lodash`에서 `es-toolkit/compat`으로 바꾸면 됩니다.

```ts
// 변경 전
import { chunk, get, debounce } from 'lodash';

// 변경 후
import { chunk, get, debounce } from 'es-toolkit/compat';

chunk([1, 2, 3, 4, 5], 2);
// => [[1, 2], [3, 4], [5]]

get({ a: { b: [10, 20] } }, 'a.b[1]');
// => 20
```

`lodash` 전체를 가져오는 방식처럼 기본 export도 지원합니다.

```ts
import toolkit from 'es-toolkit/compat';

toolkit.uniq([1, 1, 2]); // => [1, 2]
```

## 메인 모듈과의 차이

| 구분 | `es-toolkit` | `es-toolkit/compat` |
| --- | --- | --- |
| 목적 | 최소 크기, 최고 성능 | lodash 호환성 |
| `null`/`undefined` 입력 | 허용하지 않음 | lodash처럼 안전하게 처리 |
| 경로 문자열 | 일부 미지원 | `'a.b[0].c'` 지원 |
| 이터레이티 단축 표기 | 미지원 | `_.property`, `_.matches` 스타일 지원 |
| 번들 크기 | 매우 작음 | 상대적으로 큼 |

## 호환 함수 예시

### `get(object, path, defaultValue?)`

경로에 해당하는 값을 안전하게 가져옵니다. 경로가 없으면 기본값을 반환합니다.

```ts
import { get } from 'es-toolkit/compat';

get({ user: { name: 'Kim' } }, 'user.name'); // => 'Kim'
get({}, 'user.name', '익명'); // => '익명'
get(null, 'a.b'); // => undefined
```

### `sortBy(collection, ...iteratees)`

이터레이티로 정렬합니다. 속성 이름 문자열을 바로 전달할 수 있습니다.

```ts
import { sortBy } from 'es-toolkit/compat';

const users = [{ name: '박', age: 30 }, { name: '김', age: 25 }];
sortBy(users, 'age');
// => [{ name: '김', age: 25 }, { name: '박', age: 30 }]
```

### `isEmpty(value)`

배열, 문자열, 객체, `Map`, `Set` 등이 비어 있는지 검사합니다.

```ts
import { isEmpty } from 'es-toolkit/compat';

isEmpty([]); // => true
isEmpty({ a: 1 }); // => false
isEmpty(null); // => true
```

## 마이그레이션 가이드

1. `lodash` 또는 `lodash-es` import를 `es-toolkit/compat`으로 교체합니다.
2. 테스트를 실행해 동작이 동일한지 확인합니다.
3. 가능한 부분부터 `es-toolkit` 메인 모듈로 점진적으로 전환해 번들 크기를 더 줄입니다.

> 번들러 설정에서 `lodash`를 `es-toolkit/compat`으로 별칭(alias) 처리하면, 서드파티 라이브러리가 사용하는 lodash까지 한 번에 대체할 수 있습니다.

## 주의 사항

- 일부 lodash 함수(`_.template` 등)는 아직 지원되지 않거나 부분적으로만 지원될 수 있습니다.
- compat 함수는 호환성을 위해 추가 검사를 수행하므로, 메인 모듈보다 약간 느릴 수 있습니다.
- 새 프로젝트에서는 가능하면 메인 모듈(`es-toolkit`)을 우선 사용하세요.
