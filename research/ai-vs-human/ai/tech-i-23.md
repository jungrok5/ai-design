# Vue.js 라이프사이클 이해하기

## 1. 라이프사이클이란?

Vue 컴포넌트 인스턴스는 생성 → 마운트 → 업데이트 → 언마운트의 과정을 거칩니다. 각 단계마다 **라이프사이클 훅(Lifecycle Hook)** 이 호출되며, 개발자는 이 훅에 코드를 등록해 특정 시점에 원하는 작업(데이터 요청, DOM 접근, 정리 작업 등)을 실행할 수 있습니다.

## 2. 단계별 훅 정리

| 단계 | Options API | Composition API | 설명 |
|---|---|---|---|
| 생성 전 | `beforeCreate` | `setup()` 자체 | 데이터·이벤트 초기화 이전 |
| 생성 | `created` | `setup()` 자체 | 반응형 데이터 준비 완료, DOM 없음 |
| 마운트 전 | `beforeMount` | `onBeforeMount` | 렌더링 직전 |
| 마운트 | `mounted` | `onMounted` | DOM 생성 완료, 접근 가능 |
| 업데이트 전 | `beforeUpdate` | `onBeforeUpdate` | 반응형 데이터 변경, DOM 패치 직전 |
| 업데이트 | `updated` | `onUpdated` | DOM 패치 완료 |
| 언마운트 전 | `beforeUnmount` | `onBeforeUnmount` | 인스턴스 아직 살아 있음 |
| 언마운트 | `unmounted` | `onUnmounted` | 정리 완료 |

> Vue 2의 `beforeDestroy` / `destroyed`는 Vue 3에서 `beforeUnmount` / `unmounted`로 이름이 바뀌었습니다.

Composition API에는 `onBeforeCreate`, `onCreated`가 없습니다. `<script setup>`이나 `setup()` 본문이 그 역할을 하기 때문입니다.

## 3. 핵심 훅 자세히 보기

### created
- 반응형 상태, computed, watch, 메서드가 준비된 상태입니다.
- `this.$el`은 아직 없으므로 DOM 접근은 불가능합니다.
- 초기 API 호출을 시작하기에 적합합니다. SSR에서도 실행되는 훅이라는 점이 중요합니다.

### mounted
- 컴포넌트의 DOM이 생성되어 삽입된 상태입니다.
- DOM 접근, 서드파티 라이브러리(차트, 지도) 초기화에 사용합니다.
- **SSR에서는 호출되지 않습니다.**
- 자식이 모두 마운트된 뒤 부모가 마운트됩니다. 전체 뷰가 렌더링된 후를 보장하려면 `nextTick`을 사용합니다.

### updated
- 상태 변경으로 DOM이 갱신된 직후 호출됩니다.
- 여기서 상태를 바꾸면 **무한 루프** 위험이 있습니다. 상태 변화에 반응할 때는 `watch`를 쓰는 편이 안전합니다.

### unmounted
- 타이머(`setInterval`), 이벤트 리스너, WebSocket 연결, 구독 등을 해제해 **메모리 누수**를 방지합니다.

```vue
<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const width = ref(window.innerWidth)
const onResize = () => (width.value = window.innerWidth)

onMounted(() => window.addEventListener('resize', onResize))
onUnmounted(() => window.removeEventListener('resize', onResize))
</script>
```

## 4. 부모-자식 훅 실행 순서

**마운트:** 부모 `beforeMount` → 자식 `beforeMount` → 자식 `mounted` → 부모 `mounted`

**업데이트:** 부모 `beforeUpdate` → 자식 `beforeUpdate` → 자식 `updated` → 부모 `updated`

**언마운트:** 부모 `beforeUnmount` → 자식 `beforeUnmount` → 자식 `unmounted` → 부모 `unmounted`

핵심은 "시작은 부모부터, 완료는 자식부터"입니다.

## 5. 기타 훅

- `onErrorCaptured`: 자손 컴포넌트의 에러를 포착합니다.
- `onRenderTracked` / `onRenderTriggered`: 개발 모드에서 렌더링 의존성 디버깅에 사용합니다.
- `onActivated` / `onDeactivated`: `<KeepAlive>`로 캐싱된 컴포넌트가 활성화·비활성화될 때 호출됩니다. 캐시된 컴포넌트는 언마운트되지 않으므로 `unmounted`가 호출되지 않습니다.
- `onServerPrefetch`: SSR 중 서버에서 데이터를 미리 가져올 때 사용합니다.

## 6. 자주 나오는 면접 질문

**Q1. API 호출은 created와 mounted 중 어디서 하나요?**
DOM이 필요 없다면 `created`(Composition API에서는 `setup` 내부)가 더 빠르게 요청을 시작할 수 있고 SSR에서도 동작합니다. DOM 의존 작업은 `mounted`에서 처리합니다. 다만 Vue 3에서는 `async setup`과 `Suspense`, 또는 `useFetch` 같은 컴포저블로 처리하는 경우도 많습니다.

**Q2. mounted에서 자식 컴포넌트 DOM에 접근할 수 있나요?**
네. 자식이 먼저 마운트되므로 가능합니다. 단, `v-if`나 비동기 컴포넌트로 아직 렌더링되지 않은 요소는 `nextTick` 이후에 접근해야 합니다.

**Q3. Vue 2와 Vue 3의 차이는?**
- 훅 이름 변경 (`destroy` → `unmount`)
- Composition API에서 `on` 접두사 함수 형태로 등록
- 한 컴포넌트에서 같은 훅을 여러 번 등록 가능
- 훅 등록은 `setup()` 실행 중 **동기적으로** 해야 함 (비동기 콜백 안에서 등록하면 동작하지 않음)

**Q4. 메모리 누수는 어떻게 방지하나요?**
`onUnmounted`에서 리스너·타이머·구독을 해제합니다. `watch`나 `watchEffect`는 `setup` 안에서 만들면 자동으로 정리됩니다.

**Q5. beforeUpdate와 watch의 차이는?**
`watch`는 특정 상태의 변경을 감시해 이전/이후 값을 제공합니다. `beforeUpdate`는 컴포넌트 전체의 DOM 업데이트 직전에 호출되며 어떤 상태가 바뀌었는지 알려주지 않습니다.

## 7. 면접 대비 요약

1. 흐름: 생성 → 마운트 → 업데이트 → 언마운트
2. DOM 접근은 `mounted`부터 가능
3. 정리 작업은 `unmounted`(필요하면 `beforeUnmount`)에서 수행
4. `updated`에서 상태 변경 금지
5. 마운트는 자식이 먼저 완료, 시작은 부모가 먼저
6. SSR에서는 `mounted` 계열 훅이 실행되지 않음
7. `KeepAlive`는 `activated` / `deactivated`를 사용

각 훅의 "이 시점에 무엇이 가능하고 무엇이 불가능한가"를 설명할 수 있으면 면접에서 충분히 답변할 수 있습니다.
