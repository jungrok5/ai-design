GitHub Actions에서 Kubernetes 클러스터로 애플리케이션을 배포하고, 배포 결과를 Slack으로 알려주는 사내 배포 자동화 도구입니다.
## 주요 기능
- GitHub Actions 워크플로우의 한 단계로 실행되어, 앞 단계에서 빌드한 이미지를 배포합니다.
- 지정한 네임스페이스의 Deployment에 새 이미지를 롤아웃하고, 상태가 정상이 될 때까지 기다립니다.
- 배포 시작, 성공, 실패, 롤백을 지정한 Slack 채널로 알립니다.
- `dev`, `staging`, `prod` 등 환경마다 클러스터, 네임스페이스, 알림 채널을 따로 설정합니다.
## 동작 흐름
## 요구 사항
- GitHub Actions 러너에서 대상 Kubernetes 클러스터에 접근할 수 있어야 합니다.
- 대상 Deployment에 대한 `get`, `patch`, `watch` 권한이 있는 ServiceAccount 또는 kubeconfig가 필요합니다.
- Slack Incoming Webhook URL 또는 Slack Bot 토큰이 필요합니다.
## 설치
GitHub Actions에서는 별도 설치 없이 아래 Action을 사용합니다.
로컬에서 직접 실행하려면:
## 사용법
### 기본 배포
### CLI 옵션
| 옵션 | 필수 | 기본값 | 설명 |
| `--env` | O | - | 배포 대상 환경 (설정 파일의 키) |
| `--image` | O | - | 배포할 이미지와 태그 |
| `--timeout` | | `5m` | rollout 완료를 기다리는 최대 시간 |
| `--no-slack` | | `false` | Slack 알림을 보내지 않음 |
| `--dry-run` | | `false` | 실제 변경 없이 대상과 명령만 출력 |
### 설정 파일
리포지토리 루트의 `shipit.yaml`에 환경별 대상을 정의합니다.
| 키 | 설명 |
| `namespace` | 대상 네임스페이스 |
| `deployment` | 이미지를 갱신할 Deployment 이름 |
| `container` | 여러 컨테이너가 있을 때 갱신할 컨테이너 이름 (선택) |
| `slack_channel` | 알림을 보낼 채널 |
| `require_approval` | `true`면 GitHub Environment 승인 후에만 배포 (선택) |
## Slack 알림
배포 단계마다 다음 정보가 포함된 메시지를 보냅니다.
- 환경, 애플리케이션 이름, 이미지 태그
- 실행자와 GitHub Actions 실행 링크
- 결과 (`started`, `succeeded`, `failed`, `rolled back`)
- 실패 시 마지막 오류 메시지
## 실패와 롤백
- rollout이 `--timeout` 안에 끝나지 않으면 실패로 처리하고 Slack에 알립니다.
- 실패 시 직전 ReplicaSet으로 롤백을 시도합니다. 롤백 결과도 알림에 포함됩니다.
- 롤백 자체가 실패하면 job을 실패로 끝내고, 수동 개입이 필요하다는 메시지를 보냅니다.
## 보안 주의 사항
- kubeconfig와 Slack 웹훅 URL은 반드시 GitHub Secrets에 저장하고, 로그에 출력하지 않습니다.
- 운영 환경(`prod`)은 GitHub Environment의 보호 규칙(승인자 지정)과 함께 사용하는 것을 권장합니다.
- ServiceAccount에는 대상 Deployment에 필요한 최소 권한만 부여합니다.
## 개발
기여 방법과 코드 리뷰 규칙은 사내 위키의 개발 가이드를 참고하세요.
## 문의
- 이슈: 이 리포지토리의 Issues
- 채널: Slack `#platform-help` <!-- 실제 채널로 수정 -->
> 이 문서는 초안이며, 코드가 아니라 요구 사항을 기준으로 작성했습니다. `<org>`, `<app>`, 채널 이름, CLI 옵션과 기본값은 코드와 대조해 수정해야 합니다.
