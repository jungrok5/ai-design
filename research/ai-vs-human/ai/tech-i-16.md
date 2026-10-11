# Spring MVC Framework

## 1. 개념
Spring MVC는 **Model-View-Controller 패턴**을 기반으로 한 Spring의 웹 프레임워크입니다. 서블릿 API 위에서 동작하며, **Front Controller 패턴**을 적용해 모든 요청을 `DispatcherServlet` 하나가 먼저 받습니다.

- **Model**: 화면에 전달할 데이터
- **View**: 사용자에게 보여줄 화면(JSP, Thymeleaf 등)
- **Controller**: 요청을 처리하고 Model과 View를 결정

## 2. 핵심 구성 요소
| 구성 요소 | 역할 |
|---|---|
| DispatcherServlet | 모든 요청을 받아 알맞은 컴포넌트에 넘김(Front Controller) |
| HandlerMapping | 요청 URL에 맞는 핸들러(Controller)를 찾음 |
| HandlerAdapter | 찾은 핸들러를 실제로 호출함 |
| ViewResolver | 논리 뷰 이름을 실제 View 객체로 바꿈 |
| View | 모델 데이터로 응답 화면을 렌더링 |

## 3. 요청 처리 흐름
1. 클라이언트 요청 → `DispatcherServlet`
2. `HandlerMapping`으로 핸들러 조회
3. `HandlerAdapter`로 핸들러 실행
4. Controller가 비즈니스 로직을 호출한 뒤 `ModelAndView`(또는 뷰 이름)를 반환
5. `ViewResolver`가 실제 View를 찾음
6. View가 렌더링되고 응답이 반환됨

> REST API(`@RestController`, `@ResponseBody`)에서는 ViewResolver를 거치지 않습니다. 대신 **HttpMessageConverter**가 객체를 JSON 등으로 직렬화합니다.

## 4. 주요 어노테이션
- `@Controller` / `@RestController`: 컨트롤러 등록
- `@RequestMapping`, `@GetMapping`, `@PostMapping`: URL 매핑
- `@RequestParam`, `@PathVariable`: 쿼리 파라미터와 경로 변수 바인딩
- `@RequestBody`, `@ResponseBody`: HTTP 본문과 객체 간 변환
- `@ModelAttribute`: 폼 데이터를 객체에 바인딩
- `@ExceptionHandler`, `@ControllerAdvice`: 예외를 한곳에서 처리

## 5. Filter와 Interceptor 비교
- **Filter**: 서블릿 컨테이너 단계에서 DispatcherServlet **이전**에 실행됩니다. 인코딩이나 보안 처리에 씁니다.
- **Interceptor**: Spring 컨텍스트 안에서 Controller **전후**에 실행됩니다(`preHandle`, `postHandle`, `afterCompletion`). 인증 확인이나 로깅에 씁니다.

## 6. 자주 나오는 면접 질문
**Q. DispatcherServlet의 역할은?**
모든 요청을 가장 먼저 받는 프론트 컨트롤러입니다. 공통 처리를 맡고, 요청을 적절한 핸들러에 넘긴 뒤 응답 생성까지 흐름 전체를 조율합니다.

**Q. @Controller와 @RestController의 차이는?**
`@RestController`는 `@Controller`와 `@ResponseBody`를 합친 것입니다. 반환값이 뷰가 아니라 HTTP 응답 본문으로 직렬화됩니다.

**Q. Spring MVC의 장점은?**
역할이 분리되어 있어 유지보수가 쉽습니다. 어노테이션 기반이라 개발 생산성이 높고, DI·AOP와 통합되어 테스트와 확장이 쉽습니다.

## 7. 정리
Spring MVC의 핵심은 **DispatcherServlet을 중심으로 한 요청 처리 흐름**입니다. 면접에서는 각 구성 요소의 역할과 처리 순서를 순서대로 설명할 수 있어야 합니다.
