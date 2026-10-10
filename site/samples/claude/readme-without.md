# shipit

명령 하나로 스테이징에 배포하는 사내 배포 도구입니다.

```bash
shipit deploy staging
```

## 왜 shipit인가

수동 배포는 평균 25분이 걸렸지만, shipit은 평균 4분이면 끝납니다.

| 방식 | 평균 배포 시간 |
| --- | --- |
| 수동 배포 | 25분 |
| shipit | 4분 |

> 2026년 3분기 사내 측정 기준 (배포 212건)

## 필요 조건

- Kubernetes 1.28 이상
- kubectl 로그인

## 설치

```bash
brew install acme/tap/shipit
```

## 사용법

### 스테이징 배포

```bash
shipit deploy staging
```

### 롤백

```bash
shipit rollback
```
