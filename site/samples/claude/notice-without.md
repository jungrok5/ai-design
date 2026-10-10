# shipit 출시: 명령 하나로 스테이징 배포

스테이징 배포를 위한 사내 배포 도구 **shipit**을 출시했습니다. 이제 명령 하나로 스테이징에 배포할 수 있습니다.

```bash
shipit deploy staging
```

## 얼마나 빨라졌나요?

2026년 3분기 사내 측정 결과(배포 212건 기준), 평균 배포 시간은 다음과 같이 줄었습니다.

| 방식 | 평균 배포 시간 |
| --- | --- |
| 수동 배포 | 25분 |
| shipit | 4분 |

## 사용 조건

- Kubernetes 1.28 이상
- kubectl 로그인 상태

## 설치

```bash
brew install acme/tap/shipit
```

## 롤백

배포에 문제가 생기면 다음 명령으로 되돌릴 수 있습니다.

```bash
shipit rollback
```

## 문의

사용 중 궁금한 점이 있으면 **#platform** 채널로 문의해 주세요.
