# es-toolkit/fp

`es-toolkit/fp`는 es-toolkit의 유틸리티 함수를 함수형 프로그래밍 스타일로 사용할 수 있게 해주는 진입점입니다. 함수들은 **데이터 마지막(data-last)** 인자 순서와 **커링(currying)**을 지원합니다. 따라서 콜백이나 옵션을 먼저 전달해 함수를 미리 만들어 두고, 나중에 데이터를 넘겨 재사용할 수 있습니다.

## 가져오기

```js
import { map, filter } from 'es-toolkit/fp';
```

기본 엔트리(`es-toolkit`)의 함수는 데이터를 첫 번째 인자로 받습니다. 반면 `fp` 버전은 콜백이나 옵션을 먼저 받고, 데이터는 마지막에 받습니다.

## 사용 예시

```js
const double = map(x => x * 2);

double([1, 2, 3]); // [2, 4, 6]

const getActiveNames = users => map(user => user.name)(
  filter(user => user.active)(users)
);

getActiveNames([
  { name: 'Alice', active: true },
  { name: 'Bob', active: false },
]); // ['Alice']
```

## 주요 특징

- **자동 커링**: 인자가 부족하면 남은 인자를 받는 함수를 반환합니다.
- **데이터 마지막 인자 순서**: 설정을 먼저 고정하고 데이터를 나중에 넘기는 패턴에 적합합니다.
- **불변성**: 원본 데이터를 변경하지 않고 새 값을 반환합니다.
- **타입 지원**: TypeScript 타입 정의가 커링된 시그니처를 추론합니다.
- **트리 셰이킹**: 사용한 함수만 번들에 포함됩니다.

## 주의 사항

- `fp` 버전과 기본 버전은 인자 순서가 다릅니다. 두 버전을 섞어 쓰면 잘못된 인자가 전달될 수 있으니 주의하세요.
- 인자 개수가 정해진 함수는 커링 시점에 기대와 다른 동작을 보일 수 있습니다. 함수별 시그니처는 공식 문서에서 확인하세요.
- 데이터가 많은 경우에도 원본을 복사하며 동작하므로, 대용량 배열에서는 메모리 사용량을 고려하세요.

## 관련 문서

- `es-toolkit`: 기본 유틸리티 API
- `es-toolkit/compat`: lodash 호환 API
