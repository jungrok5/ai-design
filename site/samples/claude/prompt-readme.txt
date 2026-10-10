사내 배포 도구 shipit의 README.md를 한국어로 써서 이 폴더에 저장해 줘. 알려진 사실은 다음이 전부야.
- 명령 하나(`shipit deploy staging`)로 스테이징에 배포한다
- 배포 시간: 사람이 하던 수동 배포 평균 25분, shipit 평균 4분 (2026년 3분기 사내 측정, 배포 212건)
- 필요 조건: Kubernetes 1.28 이상, kubectl 로그인
- 설치: `brew install acme/tap/shipit`
- 롤백: `shipit rollback`
