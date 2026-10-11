# [Java] Java 8 정리

## 1. 람다 표현식
- 익명 클래스를 간결하게 표현하는 문법으로, `(인자) -> 본문` 형태입니다.
- 추상 메서드가 하나뿐인 함수형 인터페이스(`@FunctionalInterface`)의 구현체를 간단히 만듭니다.
- 대표적인 함수형 인터페이스는 `Predicate<T>`, `Function<T,R>`, `Consumer<T>`, `Supplier<T>`입니다.
- 람다가 참조하는 지역 변수는 effectively final이어야 합니다.

## 2. 메서드 참조
- `String::length`, `System.out::println`처럼 람다가 기존 메서드만 호출할 때 더 간결하게 쓸 수 있습니다.

## 3. Stream API
- 컬렉션 데이터를 선언형으로 처리합니다.
- 중간 연산(`filter`, `map`, `sorted`)은 지연 평가되고, 최종 연산(`collect`, `forEach`, `reduce`)을 만날 때 실행됩니다.
- 스트림은 한 번만 소비할 수 있고, 원본 컬렉션을 변경하지 않습니다.
- 병렬 스트림(`parallelStream()`)은 공유 상태를 건드리면 경쟁 조건이 생길 수 있으므로 주의해야 합니다.

## 4. Optional
- null 대신 값의 존재 여부를 표현하는 래퍼 클래스입니다.
- `orElse`, `orElseGet`, `ifPresent`로 안전하게 처리하고, 검사 없이 `get()`을 호출하는 것은 피합니다.

## 5. 인터페이스의 default / static 메서드
- 기존 구현체를 깨뜨리지 않고 인터페이스에 기능을 추가할 수 있습니다. 예: `List.forEach`.
- 여러 인터페이스의 default 메서드가 충돌하면 구현 클래스에서 직접 재정의해야 합니다.

## 6. 날짜/시간 API (java.time)
- `LocalDate`, `LocalDateTime`, `Duration` 등은 불변 객체이며 스레드 안전합니다.
- 가변성과 스레드 안전성 문제가 있던 기존 `Date`, `SimpleDateFormat`의 단점을 보완합니다.
