shipit은 GitHub Actions 워크플로에서 쿠버네티스 클러스터로 애플리케이션을 배포하고, 배포 결과를 슬랙 채널에 알리는 사내 배포 도구입니다.
> [TODO] 이 문서의 입력값 이름, 기본값, 메시지 형식은 초안입니다. 실제 구현(`action.yml`)과 맞춰 수정해야 합니다.
## 동작 방식
shipit은 이미지를 빌드하지 않습니다. 이미지 빌드와 레지스트리 push는 shipit 앞 단계에서 끝나 있어야 합니다.
## 사전 준비
| 항목 | 설명 |
| kubeconfig | 대상 클러스터에 접근할 수 있는 kubeconfig. 저장소 시크릿 `KUBECONFIG`에 base64로 인코딩해 넣습니다. |
| 서비스 계정 권한 | 대상 네임스페이스의 Deployment에 대한 `get`, `list`, `patch`, `update` 권한 |
| 슬랙 웹훅 URL | 알림 받을 채널의 Incoming Webhook URL. 저장소 시크릿 `SLACK_WEBHOOK_URL`에 넣습니다. |
| 컨테이너 이미지 | 레지스트리에 push된 이미지와 태그 |
kubeconfig 시크릿은 다음 명령으로 만듭니다.
## 사용법
워크플로 파일에 shipit 단계를 추가합니다. 아래 예시는 `main` 브랜치에 push하면 스테이징 클러스터에 배포합니다.
## 입력값
| 이름 | 필수 | 기본값 | 설명 |
| `kubeconfig` | 예 | | base64로 인코딩한 kubeconfig |
| `namespace` | 예 | | 배포할 네임스페이스 |
| `deployment` | 예 | | 이미지를 교체할 Deployment 이름 |
| `image` | 예 | | 새 이미지 전체 경로와 태그 |
| `container` | 아니요 | Deployment의 첫 번째 컨테이너 | 이미지를 교체할 컨테이너 이름 |
| `slack-webhook-url` | 아니요 | | 비워 두면 슬랙 알림을 보내지 않습니다. |
| `slack-mention` | 아니요 | | 실패 알림에 붙일 멘션. 예: `<!subteam^S0123ABCD>` |
| `timeout` | 아니요 | `300` | 롤아웃 완료를 기다리는 시간(초) |
| `rollback-on-failure` | 아니요 | `true` | 롤아웃이 실패하거나 시간이 초과되면 이전 리비전으로 되돌립니다. |
| `dry-run` | 아니요 | `false` | 클러스터를 바꾸지 않고 적용될 변경만 로그에 출력합니다. |
## 출력값
| 이름 | 설명 |
| `status` | `success`, `failed`, `rolled-back` 중 하나 |
| `revision` | 배포 후 Deployment의 리비전 번호 |
| `duration` | 배포에 걸린 시간(초) |
다음 단계에서 `steps.<id>.outputs.status`로 결과를 읽을 수 있습니다.
## 슬랙 알림
shipit은 배포 한 건에 메시지를 두 번 보냅니다. 시작할 때 한 번, 끝났을 때 한 번입니다. 각 메시지에는 다음 정보가 들어갑니다.
- 저장소와 Deployment 이름, 네임스페이스
- 커밋 SHA와 커밋 메시지 첫 줄
- 워크플로를 실행한 GitHub 사용자
- 종료 메시지에만: 결과, 소요 시간, 워크플로 실행 로그 링크
실패 메시지에는 `slack-mention`에 지정한 사용자나 그룹을 멘션합니다.
## 여러 환경에 배포하기
GitHub Environments로 환경마다 시크릿을 분리하고, 운영 배포에 승인 단계를 둡니다.
`production` 환경에 Required reviewers를 설정하면 스테이징 배포가 끝난 뒤 승인을 받아야 운영 배포가 시작됩니다.
## 제약 사항
- Deployment 리소스만 지원합니다. StatefulSet, DaemonSet, Helm 릴리스는 지원하지 않습니다.
- 한 번에 Deployment 하나의 이미지만 바꿉니다. ConfigMap이나 Service 같은 다른 리소스 변경은 별도 단계에서 적용해야 합니다.
- 롤백은 Deployment 리비전 기준입니다. DB 마이그레이션처럼 클러스터 밖에서 일어난 변경은 되돌리지 않습니다.
- 같은 Deployment에 두 워크플로가 동시에 배포하면 나중에 끝난 쪽이 남습니다. 워크플로에 `concurrency`를 설정해 막습니다.
## 문제 해결
| 증상 | 원인과 조치 |
| `error: You must be logged in to the server (Unauthorized)` | kubeconfig의 토큰이 만료되었습니다. 시크릿 `KUBECONFIG`를 새 kubeconfig로 교체합니다. |
| `deployments.apps "..." is forbidden` | 서비스 계정에 대상 네임스페이스 권한이 없습니다. 사전 준비의 권한 목록을 확인합니다. |
| 롤아웃이 `timeout`까지 끝나지 않음 | 새 파드가 Ready가 되지 않았습니다. `kubectl describe pod`와 파드 로그에서 이미지 pull 실패, readiness probe 실패를 확인합니다. 정상적으로 오래 걸리는 서비스라면 `timeout`을 늘립니다. |
| 슬랙 알림이 오지 않음 | 웹훅 URL이 비었거나 채널이 보관 처리되었습니다. 워크플로 로그의 shipit 단계에서 슬랙 응답 코드를 확인합니다. |
## 문의
- 담당 팀: [TODO: 팀 이름]
- 슬랙 채널: [TODO: #채널]
- 버그와 기능 요청: 이 저장소의 Issues
