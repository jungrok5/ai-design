# shipit 출시: 명령 하나로 스테이징 배포

shipit은 스테이징 배포를 명령 하나로 실행하는 사내 배포 도구입니다. 오늘부터 사용할 수 있습니다.

```bash
shipit deploy staging
```

## 배포 시간

2026년 3분기에 사내에서 배포 212건을 측정했습니다. 수동 배포는 평균 25분, shipit 배포는 평균 4분이 걸렸습니다.

| 방식 | 평균 배포 시간 |
| --- | --- |
| 수동 | 25분 |
| shipit | 4분 |

## 사용 조건

- Kubernetes 1.28 이상
- kubectl 로그인 완료

## 설치

```bash
brew install acme/tap/shipit
```

## 롤백

배포를 되돌릴 때는 다음 명령을 실행합니다.

```bash
shipit rollback
```

## 문의

사용 중 막히는 부분이나 질문은 #platform 채널에 남겨 주세요.
