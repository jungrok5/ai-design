# es-toolkit/types

`es-toolkit/types`는 es-toolkit 함수의 시그니처에 쓰이는 공용 타입 유틸리티를 모아 둔 진입점입니다. 이 타입들을 가져와 쓰면 직접 만든 래퍼 함수도 es-toolkit과 같은 타입 규칙을 따를 수 있습니다. 모든 타입은 런타임 코드를 포함하지 않으므로 번들 크기에 영향을 주지 않습니다.

> 이 문서의 타입 이름과 예시는 설명을 위한 것입니다. 실제로 제공되는 타입은 설치한 버전의 `.d.ts` 파일에서 확인하세요.

## 가져오기

```ts
import type { Falsy, Nullable, Mutable } from 'es-toolkit/types';
```

타입만 가져오므로 `import type` 구문을 권장합니다. 이렇게 하면 컴파일 후 import 문이 완전히 제거됩니다.

## 타입 목록

### `Falsy`

JavaScript에서 거짓으로 평가되는 값을 나타내는 유니언 타입입니다.

```ts
type Falsy = false | 0 | 0n | '' | null | undefined;
```

**사용 예시**

```ts
import type { Falsy } from 'es-toolkit/types';

function isFalsy(value: unknown): value is Falsy {
  return !value;
}
```

### `Nullable<T>`

`T`에 `null`과 `undefined`를 모두 허용합니다.

```ts
type Nullable<T> = T | null | undefined;
```

**사용 예시**

```ts
import type { Nullable } from 'es-toolkit/types';

function greet(name: Nullable<string>): string {
  return `안녕하세요, ${name ?? '손님'}님`;
}

greet('민수'); // '안녕하세요, 민수님'
greet(null); // '안녕하세요, 손님님'
```

### `Mutable<T>`

객체의 모든 `readonly` 수식어를 제거합니다. 읽기 전용 객체를 복사해서 수정할 때 유용합니다.

```ts
type Mutable<T> = { -readonly [K in keyof T]: T[K] };
```

**사용 예시**

```ts
import type { Mutable } from 'es-toolkit/types';

interface Config {
  readonly host: string;
  readonly port: number;
}

const draft: Mutable<Config> = { host: 'localhost', port: 3000 };
draft.port = 8080; // 오류 없음
```

### `DeepPartial<T>`

객체의 모든 속성을 중첩된 수준까지 선택적으로 만듭니다. 설정 병합 함수의 인자 타입으로 자주 쓰입니다.

```ts
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};
```

**사용 예시**

```ts
import type { DeepPartial } from 'es-toolkit/types';

interface Options {
  server: { host: string; port: number };
  debug: boolean;
}

function configure(overrides: DeepPartial<Options>) {
  // ...
}

configure({ server: { port: 8080 } });
```

### `Primitive`

JavaScript의 원시 값 타입을 모두 포함하는 유니언입니다.

```ts
type Primitive = string | number | bigint | boolean | symbol | null | undefined;
```

## 타입 요약

| 타입 | 설명 | 대표 용도 |
| --- | --- | --- |
| `Falsy` | 거짓으로 평가되는 값 | 타입 가드, 필터링 |
| `Nullable<T>` | `T` 또는 `null`/`undefined` | 선택적 인자 |
| `Mutable<T>` | `readonly` 제거 | 복사본 수정 |
| `DeepPartial<T>` | 깊은 선택적 속성 | 설정 병합 |
| `Primitive` | 원시 값 전체 | 값 비교, 직렬화 |

## 활용 예시

타입 가드와 `Nullable`을 함께 쓰면 배열에서 비어 있는 값을 안전하게 걸러낼 수 있습니다.

```ts
import type { Nullable } from 'es-toolkit/types';

function compactValues<T>(items: Array<Nullable<T>>): T[] {
  return items.filter((item): item is T => item != null);
}

compactValues([1, null, 2, undefined, 3]); // [1, 2, 3]
```

## 참고 사항

- 이 모듈은 타입 선언만 제공합니다. 값이나 함수를 내보내지 않습니다.
- TypeScript 5.0 이상을 권장합니다.
- `DeepPartial`은 배열과 함수까지 재귀적으로 처리하지는 않습니다. 이런 경우에는 별도의 타입을 정의하세요.
- `isolatedModules`를 켠 프로젝트에서는 반드시 `import type`을 사용하세요.

## 관련 문서

- `es-toolkit/predicate`: 타입 가드로 쓸 수 있는 판별 함수 모음
- `es-toolkit/compat`: lodash 호환 함수와 타입
