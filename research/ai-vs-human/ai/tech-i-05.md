# [Spring Boot] Test Code

## 1. 왜 테스트 코드인가?
- **회귀 방지**: 기능 추가·리팩터링 시 기존 동작이 깨졌는지 즉시 확인한다.
- **살아있는 문서**: 테스트 이름과 코드가 곧 명세 역할을 한다.
- **설계 개선**: 테스트하기 어려운 코드는 결합도가 높다는 신호다.

## 2. 테스트 피라미드
| 구분 | 범위 | 속도 | 예시 |
|---|---|---|---|
| 단위 테스트 | 클래스/메서드 | 빠름 | JUnit5 + Mockito |
| 통합 테스트 | 여러 계층·DB | 보통 | `@SpringBootTest` |
| E2E | 전체 시스템 | 느림 | RestAssured, Selenium |

단위 테스트를 가장 많이, E2E는 최소한으로 유지한다.

## 3. 핵심 어노테이션
- `@SpringBootTest`: 전체 ApplicationContext를 로드한다. 가장 무겁지만 실제 환경과 가깝다.
- `@WebMvcTest`: Controller 계층만 로드한다. `MockMvc`를 주입받고 Service는 `@MockBean`(최신 버전은 `@MockitoBean`)으로 대체한다.
- `@DataJpaTest`: JPA 관련 빈만 로드하고, 기본적으로 내장 DB를 사용하며 테스트마다 롤백한다.
- `@MockBean` / `@MockitoBean`: 스프링 컨텍스트의 빈을 Mock으로 교체한다.
- `@ExtendWith(MockitoExtension.class)`: 스프링 없이 순수 Mockito로 빠르게 테스트한다.
- `@Transactional`: 테스트 종료 후 자동 롤백한다.

## 4. 작성 패턴: Given-When-Then
```java
@WebMvcTest(UserController.class)
class UserControllerTest {
    @Autowired MockMvc mockMvc;
    @MockBean UserService userService;

    @Test
    void 사용자_조회_성공() throws Exception {
        // given
        given(userService.find(1L)).willReturn(new UserDto("kim"));
        // when & then
        mockMvc.perform(get("/users/1"))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.name").value("kim"));
    }
}
```

## 5. Mock vs Stub vs Spy
- **Stub**: 정해진 값을 반환하도록 만든 대역(상태 검증).
- **Mock**: 호출 여부·횟수를 검증하는 대역(행위 검증, `verify`).
- **Spy**: 실제 객체를 감싸 일부만 가짜로 바꾼다.

## 6. 실무 팁
- 슬라이스 테스트(`@WebMvcTest`, `@DataJpaTest`)를 우선 사용해 컨텍스트 로딩 시간을 줄인다.
- 외부 의존성(DB, 메시지 큐)은 **Testcontainers**로 실제와 유사하게 구성한다.
- 테스트는 서로 독립적이어야 하며 실행 순서에 의존하지 않는다.
- `@SpringBootTest`를 남발하면 빌드가 느려지고 컨텍스트 캐시도 깨지기 쉽다.
- 검증은 AssertJ(`assertThat`)로 가독성을 높인다.

## 7. 예상 면접 질문
1. **`@SpringBootTest`와 `@WebMvcTest`의 차이는?** → 전자는 전체 컨텍스트, 후자는 웹 계층만 로드한다.
2. **단위 테스트와 통합 테스트를 나누는 기준은?** → 외부 자원·스프링 컨텍스트 의존 여부.
3. **DB 테스트에서 데이터 격리는 어떻게 하는가?** → `@Transactional` 롤백, `@DataJpaTest`, Testcontainers.
4. **좋은 테스트의 조건은?** → 빠르고(Fast), 독립적이며(Independent), 반복 가능하고(Repeatable), 자가 검증되며(Self-validating), 적시에 작성된다(Timely) — FIRST 원칙.
