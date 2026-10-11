# React & Spring Boot 연동하여 환경 구축하기

> 기술 면접 대비 정리 노트

---

## 1. 개요

React(프론트엔드)와 Spring Boot(백엔드)를 함께 쓰는 구조는 **SPA + REST API** 방식의 대표적인 예입니다. React는 화면 렌더링과 사용자 상호작용을 맡고, Spring Boot는 비즈니스 로직, DB 접근, 인증을 맡아 JSON으로 데이터를 주고받습니다.

연동할 때 핵심은 다음 세 가지입니다.

1. 개발 환경에서 **서로 다른 포트(Origin)** 사이의 통신 문제(CORS) 해결하기
2. 배포 시 **하나로 합칠지, 따로 배포할지** 결정하기
3. SPA의 **클라이언트 라우팅**과 서버 라우팅 사이의 충돌 처리하기

---

## 2. 프로젝트 구조 예시

```
my-app/
├── backend/            # Spring Boot (Gradle)
│   └── src/main/java/...
│   └── src/main/resources/static/   # (통합 배포 시) React 빌드 결과물
└── frontend/           # React (Vite)
    ├── src/
    └── vite.config.js
```

- 개발 시에는 React 개발 서버(`localhost:5173`)와 Spring Boot(`localhost:8080`)를 **각각 실행**합니다.
- 운영 환경에서는 ① React 빌드 결과물을 Spring Boot에 포함해 하나의 JAR로 배포하거나, ② Nginx/CDN과 API 서버로 **분리 배포**합니다.

---

## 3. 개발 환경의 CORS 문제와 해결법

### 3-1. CORS란?
**CORS(Cross-Origin Resource Sharing)**는 브라우저의 **Same-Origin Policy** 때문에 생기는 제약을 서버가 허용하는 메커니즘입니다. Origin은 **프로토콜 + 호스트 + 포트**로 결정되므로, `localhost:5173`과 `localhost:8080`은 서로 다른 Origin입니다.

- 브라우저가 막는 것이지 서버가 요청을 거부하는 것이 아닙니다. 서버는 응답을 보내지만 브라우저가 응답을 차단합니다.
- `PUT`, `DELETE` 요청이나 `Content-Type: application/json` 같은 요청은 본 요청 전에 **Preflight(OPTIONS)** 요청이 먼저 갑니다.

### 3-2. 해결 방법 ① 프론트엔드 프록시 (개발용으로 권장)

```js
// vite.config.js
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },
});
```

- 브라우저는 같은 Origin(5173)에 요청하고, 개발 서버가 8080으로 **대신 전달**합니다. 그래서 CORS 자체가 발생하지 않습니다.
- CRA에서는 `package.json`의 `"proxy"` 필드나 `setupProxy.js`를 사용합니다.

### 3-3. 해결 방법 ② 백엔드 CORS 설정

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
                .allowedOrigins("http://localhost:5173")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowCredentials(true);
    }
}
```

- `allowCredentials(true)`와 `allowedOrigins("*")`는 **함께 쓸 수 없습니다**. 와일드카드가 필요하다면 `allowedOriginPatterns`를 사용합니다.
- **Spring Security**를 쓴다면 `http.cors(Customizer.withDefaults())`로 Security 필터 체인에서도 CORS를 활성화해야 합니다. 그렇지 않으면 Preflight 요청이 인증 필터에서 막힐 수 있습니다.

---

## 4. 빌드 통합 (단일 JAR 배포)

Gradle 빌드 시 React를 빌드하고, 그 결과물을 `static` 폴더로 복사합니다.

```groovy
def frontendDir = "$projectDir/../frontend"

task npmInstall(type: Exec) {
    workingDir frontendDir
    commandLine 'npm', 'ci'
}

task buildReact(type: Exec, dependsOn: npmInstall) {
    workingDir frontendDir
    commandLine 'npm', 'run', 'build'
}

task copyReact(type: Copy, dependsOn: buildReact) {
    from "$frontendDir/dist"
    into "$buildDir/resources/main/static"
}

processResources.dependsOn copyReact
```

- Spring Boot는 `classpath:/static`에 있는 파일을 **정적 리소스로 자동 서빙**합니다.
- 실무에서는 `com.github.node-gradle.node` 플러그인으로 Node 버전까지 고정해 빌드 재현성을 확보하기도 합니다.
- 장점: 배포 단위가 하나이고 같은 Origin이라 CORS가 필요 없습니다.
- 단점: 프론트만 수정해도 백엔드 전체를 다시 배포해야 하고, 정적 파일 캐싱/CDN 활용이 불리합니다.

---

## 5. SPA 라우팅 문제 (새로고침 시 404)

React Router의 `/users/1` 같은 경로는 **클라이언트에만 존재**합니다. 사용자가 이 주소에서 새로고침하면 서버에 해당 매핑이 없어 404가 발생합니다.

```java
@Controller
public class SpaController {
    @GetMapping(value = {"/{path:[^\\.]*}", "/**/{path:[^\\.]*}"})
    public String forward() {
        return "forward:/index.html";
    }
}
```

- 확장자가 없는 경로를 모두 `index.html`로 forward하면 React Router가 라우팅을 이어받습니다.
- `/api/**`는 `@RestController`가 더 구체적으로 매핑되므로 우선 처리됩니다. 다만 경로 패턴이 겹치지 않도록 API 경로에 **`/api` prefix를 두는 것**이 좋습니다.
- Spring Boot 3(PathPatternParser)에서는 `/**/{path}`처럼 `**` 뒤에 패턴이 오는 형식이 제한되므로, `ErrorController`나 `ResourceResolver`를 커스터마이징하는 방식도 함께 알아두면 좋습니다.
- 분리 배포 시 Nginx에서는 `try_files $uri /index.html;`로 처리합니다.

---

## 6. 배포 전략 비교

| 구분 | 통합 배포 (단일 JAR) | 분리 배포 (Nginx/CDN + API) |
|---|---|---|
| 구성 복잡도 | 낮음 | 높음 |
| CORS | 불필요 (Same Origin) | 리버스 프록시로 회피하거나 CORS 설정 필요 |
| 독립 배포 | 불가 | 가능 |
| 확장성/캐싱 | 제한적 | CDN, 정적 캐싱에 유리 |
| 적합한 경우 | 소규모, 사이드 프로젝트 | 팀 분리, 트래픽이 많은 서비스 |

---

## 7. 환경 변수 관리

- React(Vite): `.env.development`, `.env.production`에 `VITE_API_URL`을 정의하고 `import.meta.env.VITE_API_URL`로 사용합니다. **빌드 시점에 값이 박히므로** 비밀 키를 넣으면 안 됩니다.
- Spring Boot: `application-{profile}.yml`과 `spring.profiles.active`로 환경을 분리합니다.

---

## 8. 예상 면접 질문

**Q1. CORS 에러는 왜 발생하고, 어떻게 해결했나요?**
> 브라우저의 Same-Origin Policy 때문에 발생합니다. 개발 환경에서는 Vite 프록시로 같은 Origin처럼 요청해 회피했고, 운영 환경에서는 같은 도메인 아래 리버스 프록시를 두거나 Spring의 `CorsRegistry`와 Security의 `cors()` 설정으로 허용할 Origin을 명시했습니다.

**Q2. 프록시 설정을 하면 운영 환경에서도 동작하나요?**
> 아닙니다. Vite 프록시는 **개발 서버 기능**이라 빌드 결과물에는 포함되지 않습니다. 운영 환경에서는 Nginx 리버스 프록시나 통합 배포로 따로 해결해야 합니다.

**Q3. SPA에서 새로고침하면 404가 나는 이유는?**
> 클라이언트 라우트는 서버에 매핑이 없기 때문입니다. API가 아닌 경로는 모두 `index.html`로 forward하도록 처리합니다.

**Q4. 통합 배포와 분리 배포 중 무엇을 선택하겠습니까?**
> 팀 규모, 배포 주기, 트래픽에 따라 다릅니다. 초기에는 통합 배포로 단순하게 시작하고, 프론트와 백엔드의 배포 주기가 달라지거나 CDN이 필요해지면 분리합니다.

**Q5. 인증은 어떻게 연동하나요?**
> 세션 쿠키 방식이라면 `credentials: 'include'`(axios는 `withCredentials: true`)와 서버의 `allowCredentials(true)`가 필요하고, 쿠키의 `SameSite` 속성도 고려해야 합니다. JWT 방식이라면 `Authorization` 헤더를 허용 헤더에 추가하고, 토큰 저장 위치(메모리 / HttpOnly 쿠키)에 따른 XSS·CSRF 트레이드오프를 설명할 수 있어야 합니다.

---

## 9. 핵심 요약

- **개발 환경**: 두 서버를 따로 실행하고, **프록시로 CORS를 회피**합니다.
- **CORS의 본질**: 브라우저 정책이므로 서버가 응답 헤더로 허용하고, Security를 쓰면 필터 체인 설정까지 필요합니다.
- **통합 배포**: React 빌드 결과물을 `static`에 넣고, SPA 경로는 `index.html`로 forward합니다.
- **분리 배포**: Nginx의 `try_files`와 리버스 프록시를 사용하고, 독립 배포와 캐싱에 유리합니다.
