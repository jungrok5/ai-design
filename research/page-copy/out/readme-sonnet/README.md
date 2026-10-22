# shipit

GitHub Actions에서 쿠버네티스 클러스터로 배포하고, 결과를 슬랙으로 알려주는 사내 배포 자동화 도구입니다.

> **TODO:** 아래 `your-org`, 버전 태그, 채널명, 입력값 이름 등은 예시입니다. 실제 값에 맞게 수정해 주세요.

## 주요 기능

- GitHub Actions 워크플로우 한 단계로 쿠버네티스에 배포
- 배포 시작 / 성공 / 실패를 슬랙 채널로 알림
- 롤아웃 완료까지 대기하고, 실패 시 워크플로우를 실패 처리
- (선택) 롤아웃 실패 시 이전 리비전으로 자동 롤백

## 동작 방식

```
git push / 수동 실행
        │
        ▼
GitHub Actions ──► shipit ──► kubectl apply / set image ──► Kubernetes
                      │
                      └──────► Slack Webhook (시작 · 성공 · 실패)
```

1. 클러스터 인증 정보로 `kubeconfig`를 구성합니다.
2. 지정한 매니페스트를 적용하거나 이미지를 교체합니다.
3. `kubectl rollout status`로 롤아웃 완료를 기다립니다.
4. 결과를 슬랙으로 전송합니다.

## 빠른 시작

### 1. 사전 준비

| 항목 | 설명 |
| --- | --- |
| 쿠버네티스 접근 권한 | 대상 네임스페이스에 배포할 수 있는 ServiceAccount 또는 kubeconfig |
| 슬랙 Incoming Webhook | 알림을 받을 채널의 Webhook URL |
| GitHub Secrets | 아래 표 참고 |

**필요한 Secrets**

| 이름 | 설명 |
| --- | --- |
| `KUBE_CONFIG` | base64로 인코딩한 kubeconfig |
| `SLACK_WEBHOOK_URL` | 슬랙 Incoming Webhook URL |

kubeconfig 인코딩 예시:

```bash
base64 -w0 ~/.kube/config
```

### 2. 워크플로우 작성

`.github/workflows/deploy.yml`

```yaml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy with shipit
        uses: your-org/shipit@v1
        with:
          kube-config: ${{ secrets.KUBE_CONFIG }}
          namespace: my-service
          manifests: k8s/
          image: registry.example.com/my-service:${{ github.sha }}
          slack-webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
          slack-channel: "#deploy"
```

## 입력값

| 이름 | 필수 | 기본값 | 설명 |
| --- | :---: | --- | --- |
| `kube-config` | O | - | base64 인코딩된 kubeconfig |
| `namespace` | O | - | 배포 대상 네임스페이스 |
| `manifests` | O | - | 적용할 매니페스트 파일 또는 디렉터리 경로 |
| `image` | | - | 교체할 컨테이너 이미지. 지정하지 않으면 매니페스트 그대로 적용 |
| `deployment` | | - | 롤아웃을 확인할 Deployment 이름 |
| `timeout` | | `300s` | 롤아웃 대기 시간 |
| `rollback-on-failure` | | `false` | 실패 시 이전 리비전으로 롤백할지 여부 |
| `slack-webhook-url` | | - | 지정하지 않으면 슬랙 알림을 보내지 않음 |
| `slack-channel` | | Webhook 기본 채널 | 알림을 보낼 채널 |

## 슬랙 알림

| 시점 | 내용 |
| --- | --- |
| 시작 | 서비스, 네임스페이스, 이미지 태그, 배포자, 커밋 링크 |
| 성공 | 위 정보 + 소요 시간 |
| 실패 | 위 정보 + 실패 원인 요약, 워크플로우 실행 링크 |

## 환경별 배포 예시

```yaml
jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - uses: your-org/shipit@v1
        with:
          kube-config: ${{ secrets.KUBE_CONFIG_STAGING }}
          namespace: my-service-staging
          manifests: k8s/overlays/staging
          slack-webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production   # 승인 필요 환경으로 설정 권장
    steps:
      - uses: actions/checkout@v4
      - uses: your-org/shipit@v1
        with:
          kube-config: ${{ secrets.KUBE_CONFIG_PROD }}
          namespace: my-service
          manifests: k8s/overlays/production
          rollback-on-failure: true
          slack-webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

## 문제 해결

**`error: You must be logged in to the server (Unauthorized)`**
kubeconfig의 토큰이 만료되었거나 인코딩이 잘못되었을 수 있습니다. `base64 -w0`로 줄바꿈 없이 다시 인코딩해 Secret을 갱신하세요.

**`error: deployment "..." exceeded its progress deadline`**
이미지 pull 실패, 리소스 부족, readinessProbe 실패가 흔한 원인입니다. `kubectl describe pod`와 `kubectl logs`로 확인하세요. 오래 걸리는 서비스라면 `timeout`을 늘려 주세요.

**슬랙 알림이 오지 않음**
`SLACK_WEBHOOK_URL` Secret이 등록되어 있는지, Webhook이 해당 채널에 연결되어 있는지 확인하세요. 포크한 저장소에서 실행한 PR 워크플로우는 Secrets에 접근할 수 없습니다.

## 보안 주의사항

- kubeconfig에는 **배포에 필요한 최소 권한**(대상 네임스페이스 한정 Role)만 부여하세요.
- 프로덕션 배포는 GitHub `environment`의 승인(Required reviewers)과 함께 사용하는 것을 권장합니다.
- Webhook URL과 kubeconfig는 반드시 GitHub Secrets에만 보관하고 로그에 출력하지 마세요.

## 개발 및 기여

```bash
git clone https://github.com/your-org/shipit.git
cd shipit
```

1. 브랜치를 만들어 변경합니다.
2. PR을 올리고 리뷰를 받습니다.
3. 머지 후 태그(`v1.x.x`)를 생성하면 릴리스됩니다.

## 문의

문제나 개선 요청은 이슈로 남기거나 슬랙 `#platform-support` 채널로 문의해 주세요.
