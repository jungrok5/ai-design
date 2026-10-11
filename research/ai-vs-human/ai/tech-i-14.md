# Singleton Pattern – 기술 면접 대비 정리 노트

## 1. 정의
**Singleton 패턴**은 클래스의 인스턴스가 **오직 하나만 생성되도록 보장**하고, 어디서든 그 인스턴스에 **전역적으로 접근**할 수 있게 하는 생성(Creational) 디자인 패턴이다.

- 목적: 인스턴스 수 제한, 전역 접근점 제공
- 대표 사용처: 설정 관리자(Config), 로거(Logger), 커넥션 풀, 캐시, 스레드 풀, 디바이스 드라이버 접근 객체

## 2. 구현 요소
1. `private` 생성자 → 외부에서 `new` 금지
2. `static` 필드에 유일한 인스턴스 보관
3. `public static getInstance()` → 인스턴스 반환

## 3. 구현 방식 (Java 기준)

### 3.1 Eager Initialization (이른 초기화)
```java
public class Eager {
    private static final Eager INSTANCE = new Eager();
    private Eager() {}
    public static Eager getInstance() { return INSTANCE; }
}
```
- 클래스 로딩 시점에 생성 → 스레드 안전(클래스 로더가 보장)
- 단점: 사용하지 않아도 메모리 점유, 예외 처리 어려움

### 3.2 Lazy Initialization (게으른 초기화, 비안전)
```java
public static Lazy getInstance() {
    if (instance == null) instance = new Lazy();
    return instance;
}
```
- 멀티스레드에서 두 개 이상 생성될 수 있음 → **Race Condition**

### 3.3 synchronized 메서드
- `getInstance()`에 `synchronized`를 붙여 안전하게 만들 수 있으나, 매 호출마다 락 비용이 발생해 성능이 떨어진다.

### 3.4 Double-Checked Locking (DCL)
```java
public class DCL {
    private static volatile DCL instance;
    private DCL() {}
    public static DCL getInstance() {
        if (instance == null) {
            synchronized (DCL.class) {
                if (instance == null) instance = new DCL();
            }
        }
        return instance;
    }
}
```
- 생성 시점에만 락을 걸어 성능 개선
- **`volatile` 필수**: 명령어 재배치(reordering)로 인해 초기화가 끝나지 않은 객체가 노출되는 것을 방지

### 3.5 Initialization-on-demand Holder (Bill Pugh)
```java
public class Holder {
    private Holder() {}
    private static class LazyHolder {
        static final Holder INSTANCE = new Holder();
    }
    public static Holder getInstance() { return LazyHolder.INSTANCE; }
}
```
- `getInstance()` 호출 시 내부 클래스가 로딩되며 생성 → Lazy + 스레드 안전 + 락 없음
- 가장 널리 권장되는 방식 중 하나

### 3.6 Enum Singleton
```java
public enum EnumSingleton { INSTANCE; }
```
- Joshua Bloch(Effective Java)가 권장
- **직렬화·리플렉션 공격에 안전**, 구현이 간결
- 단점: 상속 불가, Lazy 로딩이 아님

## 4. 비교 표

| 방식 | Lazy | 스레드 안전 | 성능 | 직렬화/리플렉션 안전 |
|---|---|---|---|---|
| Eager | X | O | 좋음 | X |
| synchronized | O | O | 낮음 | X |
| DCL | O | O | 좋음 | X |
| Holder | O | O | 좋음 | X |
| Enum | X | O | 좋음 | O |

## 5. 깨지는 경우와 방어
- **리플렉션**: `setAccessible(true)`로 private 생성자 호출 → 생성자에서 이미 인스턴스가 있으면 예외 던지기
- **직렬화**: 역직렬화 시 새 객체 생성 → `readResolve()`에서 `INSTANCE` 반환
- **클론**: `clone()` 오버라이드 시 예외 던지기
- **멀티 클래스로더**: 클래스로더별로 인스턴스가 생성될 수 있음

## 6. 장점
- 메모리 절약, 인스턴스 생성 비용 절감
- 전역 접근으로 데이터 공유 용이
- 자원(DB 커넥션 등)의 일관된 관리

## 7. 단점 및 비판
- **전역 상태**: 숨은 의존성이 생겨 코드 추적이 어려움
- **테스트 어려움**: Mock 교체가 힘들고 테스트 간 상태 공유로 격리가 깨짐
- **SRP 위반**: 인스턴스 관리와 비즈니스 로직 책임을 동시에 가짐
- **OCP/DIP 위반 가능성**: 구체 클래스에 강하게 결합
- 멀티스레드 환경에서 내부 상태가 mutable이면 별도 동기화 필요
- 안티패턴으로 불리기도 함

## 8. Spring과의 관계
- Spring Bean의 기본 스코프는 `singleton`이지만, **컨테이너당 하나**라는 의미로 GoF Singleton과 다르다.
- 클래스 자체가 아닌 **컨테이너가 인스턴스 수를 관리**하므로 private 생성자나 static 접근이 필요 없고, DI로 주입되어 테스트가 쉽다.
- 싱글톤 Bean은 **무상태(stateless)** 로 설계해야 한다.

## 9. 면접 예상 질문
1. **Singleton 패턴이란 무엇이고 왜 사용하나요?**
   → 인스턴스를 하나로 제한하고 전역 접근점을 제공하여 자원 낭비를 막는다.
2. **DCL에서 `volatile`이 필요한 이유는?**
   → `new`는 메모리 할당 → 생성자 실행 → 참조 할당으로 이뤄지는데, 재배치로 참조가 먼저 할당되면 다른 스레드가 미완성 객체를 볼 수 있다.
3. **가장 안전한 구현 방법은?**
   → Enum 방식. 직렬화와 리플렉션에도 안전하다. 상속이 필요하거나 Lazy가 중요하면 Holder 방식.
4. **Spring의 싱글톤과 GoF 싱글톤의 차이는?**
   → 범위가 JVM 전체냐 컨테이너 단위냐의 차이이며, Spring은 DI 기반이라 결합도가 낮다.
5. **Singleton의 단점을 어떻게 보완하나요?**
   → 인터페이스를 두고 DI로 주입하여 결합도를 낮추고, 상태를 최소화하며, 테스트 시 대체 가능한 구조로 설계한다.
6. **Singleton을 깨뜨리는 방법과 방어법은?**
   → 리플렉션, 직렬화, 클론, 멀티 클래스로더. Enum 사용 또는 각각 예외/`readResolve` 처리로 방어한다.

## 10. 한 줄 요약
> Singleton은 "하나의 인스턴스 + 전역 접근"을 보장하는 패턴이다. 구현은 **Holder 또는 Enum**을 우선 고려하고, 전역 상태의 단점은 **DI 컨테이너**로 보완하는 것이 실무의 정석이다.
