# [Java] 직렬화(Serialization)

## 1. 개념

**직렬화(Serialization)** 는 메모리에 있는 Java 객체를 바이트 스트림으로 바꾸는 과정입니다. 이렇게 바꾼 데이터는 파일에 저장하거나 네트워크로 보내거나 DB에 넣을 수 있습니다. 반대로 바이트 스트림을 다시 객체로 되돌리는 과정은 **역직렬화(Deserialization)** 라고 합니다.

- 직렬화: `ObjectOutputStream.writeObject()`
- 역직렬화: `ObjectInputStream.readObject()`

## 2. 기본 사용법

직렬화할 클래스는 `java.io.Serializable` 인터페이스를 구현해야 합니다. 이 인터페이스에는 메서드가 없습니다. JVM에 "이 클래스는 직렬화해도 된다"고 알리는 **마커 인터페이스(Marker Interface)** 입니다.

```java
public class User implements Serializable {
    private static final long serialVersionUID = 1L;
    private String name;
    private transient String password; // 직렬화 제외
}
```

## 3. 핵심 키워드

### serialVersionUID
- 직렬화한 클래스와 역직렬화할 클래스가 같은 버전인지 확인하는 **버전 식별자**입니다.
- 직접 선언하지 않으면 JVM이 클래스 구조를 바탕으로 자동 생성합니다. 이 경우 필드가 하나만 바뀌어도 값이 달라지고, 역직렬화할 때 `InvalidClassException`이 발생합니다.
- 그래서 **명시적으로 선언하는 것이 권장됩니다.**

### transient
- 직렬화 대상에서 빼고 싶은 필드에 붙입니다.
- 역직렬화하면 해당 필드는 기본값(null, 0, false)으로 채워집니다.
- 비밀번호처럼 민감한 정보나, 다시 계산할 수 있는 값에 사용합니다.

### static 필드
- static 필드는 객체가 아니라 클래스에 속하므로 **직렬화되지 않습니다.**

## 4. 직렬화 규칙

1. 부모 클래스가 `Serializable`이 아니면 부모의 필드는 직렬화되지 않습니다. 이때 부모 클래스에는 **기본 생성자**가 있어야 합니다.
2. 참조하는 객체도 모두 `Serializable`이어야 합니다. 그렇지 않으면 `NotSerializableException`이 발생합니다.
3. 역직렬화할 때 `Serializable` 클래스의 생성자는 호출되지 않습니다.

## 5. 커스텀 직렬화

- `writeObject()`와 `readObject()`를 private으로 정의하면 직렬화 방식을 직접 제어할 수 있습니다.
- `Externalizable` 인터페이스를 쓰면 `writeExternal()`과 `readExternal()`로 전체 과정을 직접 구현합니다. 이 경우 **public 기본 생성자**가 필요합니다.
- `readResolve()`를 쓰면 역직렬화 때 싱글톤이 깨지는 것을 막을 수 있습니다.

## 6. 문제점과 대안

| 문제점 | 설명 |
|---|---|
| 보안 취약점 | 신뢰할 수 없는 데이터를 역직렬화하면 원격 코드 실행(RCE) 공격에 노출될 수 있음 |
| 버전 관리 어려움 | 클래스 구조가 바뀌면 호환성이 깨짐 |
| 용량·성능 | 클래스 메타정보가 함께 저장되어 데이터가 크고 느림 |
| Java 전용 | 다른 언어와 데이터를 주고받기 어려움 |

**대안:** JSON(Jackson, Gson), Protocol Buffers, Avro처럼 언어에 독립적인 포맷을 주로 사용합니다. 『Effective Java』도 "자바 직렬화의 대안을 찾으라"고 권합니다.

## 7. 면접 예상 질문

**Q1. serialVersionUID를 선언하지 않으면 어떻게 되나요?**
JVM이 클래스 구조를 기반으로 해시값을 자동 생성합니다. 이후 클래스가 조금만 바뀌어도 UID가 달라져 역직렬화에 실패합니다.

**Q2. transient와 static의 차이는?**
둘 다 직렬화되지 않는다는 점은 같습니다. transient는 개발자가 명시적으로 제외한 인스턴스 필드입니다. static은 클래스 수준의 변수라서 처음부터 직렬화 대상이 아닙니다.

**Q3. 자바 직렬화를 실무에서 지양하는 이유는?**
역직렬화 보안 취약점, 버전 호환성 문제, 큰 용량, 자바에 종속된다는 점 때문입니다. 실무에서는 JSON이나 Protobuf를 많이 씁니다.

**Q4. Serializable과 Externalizable의 차이는?**
Serializable은 JVM이 자동으로 직렬화하고 필요하면 일부만 직접 정의합니다. Externalizable은 전체 과정을 개발자가 직접 구현하므로 성능을 더 최적화할 수 있습니다.
