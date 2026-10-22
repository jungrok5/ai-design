GitHub Actions에서 쿠버네티스 클러스터로 배포하고, 결과를 슬랙으로 알려주는 사내 배포 자동화 도구입니다.
## 목차
- [주요 기능](#주요-기능)
- [빠른 시작](#빠른-시작)
- [설정 파일 (`shipit.yaml`)](#설정-파일-shipityaml)
- [Action 입력값](#action-입력값)
- [필요한 Secrets](#필요한-secrets)
- [환경별 배포](#환경별-배포)
- [롤백](#롤백)
- [슬랙 알림](#슬랙-알림)
- [문제 해결](#문제-해결)
- [기여하기](#기여하기)
- [문의](#문의)
## 주요 기능
- **한 줄로 배포** – 워크플로에 `uses: <org>/shipit@v1` 한 단계만 추가하면 됩니다.
- **환경별 설정** – `dev` / `staging` / `prod` 마다 클러스터, 네임스페이스, 레플리카 수를 따로 지정합니다.
- **롤아웃 확인** – `kubectl rollout status`로 배포 완료까지 기다리고, 시간 안에 끝나지 않으면 실패로 처리합니다.
- **자동 롤백** – 롤아웃이 실패하면 직전 리비전으로 되돌립니다(옵션).
- **슬랙 알림** – 배포 시작·성공·실패·롤백을 채널로 보내고, 커밋·작성자·워크플로 링크를 함께 남깁니다.
- **운영 배포 보호** – `prod` 배포는 GitHub Environments의 승인 규칙과 함께 쓸 수 있습니다.
## 빠른 시작
### 1. 저장소에 설정 파일 추가
저장소 루트에 `shipit.yaml`을 만듭니다.
### 2. 워크플로 추가
### 3. Secrets 등록
저장소 **Settings → Secrets and variables → Actions**에 [필요한 Secrets](#필요한-secrets)를 등록하면 끝입니다. `main`에 푸시하면 `dev`로 배포됩니다.
## 설정 파일 (`shipit.yaml`)
| 키 | 필수 | 기본값 | 설명 |
| `app` | ✅ | – | 앱 이름. 슬랙 알림과 리소스 라벨에 쓰입니다. |
| `image` | ✅ | – | 컨테이너 이미지 저장소 경로 (태그 제외) |
| `manifests` | ✅ | – | 매니페스트 디렉터리 또는 Kustomize 디렉터리 |
| `environments.<env>.cluster` | ✅ | – | 대상 클러스터 컨텍스트 이름 |
| `environments.<env>.namespace` | ✅ | – | 대상 네임스페이스 |
| `environments.<env>.replicas` | | 매니페스트 값 | 레플리카 수 덮어쓰기 |
| `rollout.timeout` | | `5m` | 롤아웃 완료 대기 시간 |
| `rollout.auto-rollback` | | `true` | 실패 시 직전 리비전으로 자동 롤백 |
| `slack.channel` | | 웹훅 기본 채널 | 알림 채널 |
| `slack.mention-on-failure` | | – | 실패 시 멘션할 그룹 (예: `@backend-oncall`) |
## Action 입력값
| 입력 | 필수 | 기본값 | 설명 |
| `environment` | ✅ | – | `shipit.yaml`에 정의된 환경 이름 |
| `image-tag` | ✅ | – | 배포할 이미지 태그 (보통 `${{ github.sha }}`) |
| `config` | | `shipit.yaml` | 설정 파일 경로 |
| `dry-run` | | `false` | `true`면 적용 없이 변경될 내용만 출력 |
| `notify` | | `true` | `false`면 슬랙 알림을 보내지 않음 |
**출력값**
| 출력 | 설명 |
| `revision` | 배포된 Deployment 리비전 번호 |
## 필요한 Secrets
| 이름 | 설명 |
| `KUBECONFIG_DATA` | base64로 인코딩한 kubeconfig. 배포 전용 ServiceAccount 권한만 주세요. |
| `SLACK_WEBHOOK_URL` | 슬랙 Incoming Webhook URL |
kubeconfig 인코딩 예시:
> ⚠️ 개인 kubeconfig를 등록하지 마세요. 배포용 ServiceAccount 발급은 플랫폼팀에 요청하면 됩니다.
환경마다 다른 클러스터를 쓴다면 GitHub **Environments**별로 같은 이름의 Secret을 따로 등록하세요.
## 환경별 배포
| 상황 | 방법 |
| `dev` 배포 | `main` 브랜치에 푸시 |
| `staging` / `prod` 배포 | Actions 탭 → **Deploy** → **Run workflow** → 환경 선택 |
| 태그로 운영 배포 | 워크플로 트리거에 `tags: ['v*']`를 추가하고 `environment: prod` 지정 |
`prod`는 GitHub Environments에 **Required reviewers**를 걸어 두는 것을 권장합니다. 승인이 나기 전까지 shipit 단계는 실행되지 않습니다.
## 롤백
**자동 롤백** – `rollout.auto-rollback: true`(기본값)면 롤아웃 실패 시 직전 리비전으로 되돌리고 슬랙에 알립니다.
**수동 롤백** – 이전 커밋 SHA로 워크플로를 다시 실행합니다.
1. Actions 탭에서 정상이었던 배포 실행 기록을 엽니다.
2. **Re-run all jobs**를 누릅니다.
긴급하게 클러스터에서 직접 되돌려야 한다면:
> 직접 되돌린 경우 슬랙 알림이 가지 않으니 배포 채널에 꼭 공유해 주세요.
## 슬랙 알림
| 이벤트 | 표시 | 내용 |
| 배포 시작 | 🟡 | 앱, 환경, 이미지 태그, 실행한 사람 |
| 배포 성공 | 🟢 | 소요 시간, 리비전 번호 |
| 배포 실패 | 🔴 | 실패 단계, 에러 요약, 워크플로 로그 링크, 담당 그룹 멘션 |
| 롤백 완료 | ⏪ | 되돌린 리비전 번호 |
예시:
## 문제 해결
| 증상 | 원인과 해결 |
| `error: You must be logged in to the server` | `KUBECONFIG_DATA`가 비었거나 토큰이 만료됨. Secret을 다시 등록하세요. |
| `forbidden: User ... cannot patch deployments` | ServiceAccount 권한 부족. 플랫폼팀에 네임스페이스 권한을 요청하세요. |
| `rollout status timed out` | 파드가 Ready가 되지 않음. `kubectl describe pod`로 이미지 풀 실패·헬스체크 실패를 확인하세요. 필요하면 `rollout.timeout`을 늘리세요. |
| `ImagePullBackOff` | 이미지 태그가 레지스트리에 없음. 빌드·푸시 단계가 먼저 끝났는지 확인하세요. |
| 슬랙 알림이 오지 않음 | `SLACK_WEBHOOK_URL` 확인, 또는 `notify: false`로 꺼져 있지 않은지 확인하세요. |
배포 전에 결과를 미리 보려면 `dry-run: true`로 실행해 보세요.
## 기여하기
1. 이 저장소에서 브랜치를 만듭니다.
2. 변경 후 테스트를 실행합니다.
3. PR을 올리고 플랫폼팀 리뷰를 받습니다.
릴리스는 `vX.Y.Z` 태그로 하며, `v1` 같은 메이저 태그는 최신 호환 버전을 가리키도록 옮깁니다. 하위 호환이 깨지는 변경은 메이저 버전을 올려 주세요.
## 문의
- 슬랙: `#platform-help`
- 담당: 플랫폼팀
- 버그·기능 요청: 이 저장소의 Issues
