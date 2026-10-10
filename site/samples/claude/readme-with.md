# shipit

shipit은 명령 하나로 스테이징에 배포하는 사내 배포 도구입니다.

```sh
shipit deploy staging
```

## 배포 시간

사람이 수동으로 배포할 때 평균 25분이 걸렸고, shipit으로는 평균 4분이 걸렸습니다.

| 방식 | 평균 배포 시간 |
| --- | --- |
| 수동 배포 | 25분 |
| shipit | 4분 |

2026년 3분기 사내 측정 결과이며, 배포 212건을 기준으로 합니다.

## 필요 조건

- Kubernetes 1.28 이상
- kubectl 로그인

## 설치

```sh
brew install acme/tap/shipit
```

## 사용법

스테이징에 배포합니다.

```sh
shipit deploy staging
```

배포를 롤백합니다.

```sh
shipit rollback
```
