# 기여하기

React는 Meta에서 처음 만든 오픈 소스 프로젝트입니다. 이 문서는 React 개발에 참여하는 과정을 설명합니다. 아래 내용을 읽으면 기여 절차를 이해하고, 버그 수정과 개선 사항을 어떻게 제안하고 빌드하고 테스트하는지 알 수 있습니다.

## 행동 강령 {/*code-of-conduct*/}

React는 [Contributor Covenant](https://www.contributor-covenant.org/)를 행동 강령으로 채택했습니다. 프로젝트에 참여하는 모든 사람은 이 강령을 지켜야 합니다. 전문을 읽어 보면 어떤 행동이 허용되고 어떤 행동이 허용되지 않는지 알 수 있습니다.

## 공개된 개발 {/*open-development*/}

React의 모든 작업은 [GitHub](https://github.com/facebook/react)에서 공개적으로 진행됩니다. 핵심 팀원이 보낸 Pull Request든 외부 기여자가 보낸 Pull Request든 같은 리뷰 절차를 거칩니다.

## 시맨틱 버전 관리 {/*semantic-versioning*/}

React는 [시맨틱 버전 관리](https://semver.org/lang/ko/)를 따릅니다.

- **패치 버전**: 중요한 버그 수정을 배포합니다.
- **마이너 버전**: 새로운 기능을 배포합니다.
- **메이저 버전**: 호환되지 않는 변경 사항을 배포합니다.

호환되지 않는 변경을 할 때는 사용자가 다가올 변경을 미리 알고 코드를 옮길 수 있도록, 마이너 버전에서 먼저 지원 중단 경고를 표시합니다. 중요한 변경 사항은 [블로그](/blog)와 변경 로그 파일에 기록됩니다.

## 브랜치 구성 {/*branch-organization*/}

변경 사항은 [`main` 브랜치](https://github.com/facebook/react/tree/main)로 직접 보내세요. 출시되지 않은 기능이나 호환되지 않는 기능을 위한 별도 브랜치는 따로 두지 않습니다. 대신 `main` 브랜치가 항상 테스트를 통과하는 상태를 유지하도록 노력하고 있습니다.

`main` 브랜치에 포함된 코드는 언제든 최신 안정 버전과 함께 배포될 수 있어야 합니다.

### 기능 플래그 {/*feature-flags*/}

`main` 브랜치를 배포 가능한 상태로 유지하기 위해 동작을 바꾸는 변경 사항은 기능 플래그 뒤에 두는 경우가 많습니다. 기능 플래그는 [`packages/shared/ReactFeatureFlags.js`](https://github.com/facebook/react/blob/main/packages/shared/ReactFeatureFlags.js)에 정의되어 있습니다. React의 일부 빌드에서는 특정 기능 플래그가 켜져 있을 수도 있습니다.

## 버그 {/*bugs*/}

### 알려진 이슈를 찾는 방법 {/*where-to-find-known-issues*/}

공개된 버그는 [GitHub Issues](https://github.com/facebook/react/issues)에서 관리합니다. 수정 중인 변경 사항도 지켜보고 있다가 내부 수정이 진행되고 있다면 분명히 알리겠습니다. 새 이슈를 등록하기 전에 같은 문제가 이미 보고되지 않았는지 확인해 주세요.

### 새 이슈 보고하기 {/*reporting-new-issues*/}

버그를 빨리 고치려면 재현 가능한 최소한의 테스트 케이스가 가장 큰 도움이 됩니다. [템플릿](https://codesandbox.io/s/new)을 사용해 시작해 보세요.

### 보안 버그 {/*security-bugs*/}

Meta는 보안 버그를 안전하게 공개할 수 있도록 [버그 바운티 프로그램](https://www.facebook.com/whitehat/)을 운영합니다. 이런 경우에는 공개 이슈를 등록하지 말고 해당 페이지에 안내된 절차를 따라 주세요.

## 연락 방법 {/*how-to-get-in-touch*/}

- [커뮤니티 페이지](/community)에서 React 사용자와 개발자를 만날 수 있습니다.
- 도움이 필요하면 각 커뮤니티의 토론 포럼을 이용하세요.

## 변경 제안하기 {/*proposing-a-change*/}

공개 API를 변경하거나 구현을 크게 바꾸려면 먼저 [이슈를 등록](https://github.com/facebook/react/issues/new)하는 것을 권장합니다. 그래야 작업을 시작하기 전에 제안에 대해 합의할 수 있습니다.

버그를 수정하는 정도라면 바로 Pull Request를 보내도 괜찮습니다. 다만 무엇을 고치는지 자세히 설명하는 이슈를 함께 등록해 두면 좋습니다. 특정 수정이 받아들여지지 않더라도 이슈는 계속 추적할 수 있기 때문입니다.

## 첫 Pull Request {/*your-first-pull-request*/}

첫 Pull Request를 준비하고 있나요? 아래 무료 강좌에서 기여 방법을 배울 수 있습니다.

**[How to Contribute to an Open Source Project on GitHub](https://app.egghead.io/playlists/how-to-contribute-to-an-open-source-project-on-github)**

처음 시작할 때는 [good first issue](https://github.com/facebook/react/issues?q=is:open+is:issue+label:%22good+first+issue%22) 라벨이 붙은 이슈를 살펴보세요. 범위가 비교적 좁아 처음 기여하기에 알맞은 버그들입니다.

이슈를 해결하기로 했다면 먼저 댓글 내역을 확인해 다른 사람이 이미 작업하고 있지 않은지 살펴보세요. 아무도 맡지 않았다면 작업하겠다고 댓글을 남겨 주세요. 다른 사람과 작업이 겹치지 않게 하기 위해서입니다.

누군가 맡겠다고 했지만 2주 넘게 소식이 없다면 이어받아도 괜찮습니다. 이때도 댓글을 남겨 주세요.

## Pull Request 보내기 {/*sending-a-pull-request*/}

핵심 팀이 Pull Request를 계속 확인합니다. 팀원이 Pull Request를 리뷰한 뒤 병합하거나, 변경을 요청하거나, 이유를 설명하고 닫습니다. API 변경은 Meta 내부 사용 사례에 맞게 조정해야 할 수도 있어 시간이 더 걸릴 수 있습니다. 진행 상황은 꾸준히 알리겠습니다.

**Pull Request를 보내기 전에** 다음을 확인하세요.

1. [저장소](https://github.com/facebook/react)를 포크하고 `main`에서 브랜치를 만듭니다.
2. 저장소 루트에서 `yarn`을 실행합니다.
3. 버그를 고쳤거나 테스트가 필요한 코드를 추가했다면 테스트를 추가합니다.
4. 테스트가 통과하는지 확인합니다(`yarn test`). 개발 중에는 `yarn test --watch TestName`이 편리합니다.
5. `yarn test --prod`로 프로덕션 환경에서도 테스트합니다.
6. 디버거가 필요하면 `yarn test --debug --watch TestName`을 실행한 뒤 `chrome://inspect`를 열고 "Inspect"를 누릅니다.
7. [Prettier](https://prettier.io/)로 코드를 정리합니다(`yarn prettier`).
8. 린트 검사를 통과하는지 확인합니다(`yarn lint`). 변경한 파일만 검사하려면 `yarn linc`를 사용하세요.
9. [Flow](https://flow.org/) 타입 검사를 실행합니다(`yarn flow`).
10. 아직 하지 않았다면 CLA에 서명합니다.

### 기여자 라이선스 동의(CLA) {/*contributor-license-agreement-cla*/}

Pull Request를 받으려면 Contributor License Agreement(CLA)에 서명해야 합니다. 한 번만 서명하면 되므로 다른 Meta 오픈 소스 프로젝트에서 이미 서명했다면 다시 할 필요가 없습니다. 처음 Pull Request를 보낸다면 CLA에 서명했다는 사실을 알려 주세요. GitHub 사용자 이름을 기준으로 확인합니다.

**[CLA에 서명하기](https://code.facebook.com/cla)**

## 기여에 필요한 사전 준비 {/*contribution-prerequisites*/}

- [Node](https://nodejs.org) LTS 버전과 [Yarn](https://yarnpkg.com/en/) v1.2.0 이상을 설치합니다.
- [JDK](https://www.oracle.com/technetwork/java/javase/downloads/index.html)를 설치합니다.
- `gcc`가 설치되어 있어야 하며, 필요하면 컴파일러를 설치합니다. 일부 의존성은 컴파일 단계가 필요할 수 있습니다. macOS에서는 Xcode Command Line Tools가 이를 처리합니다. Ubuntu에서는 `apt-get install build-essential`로 필요한 패키지를 설치할 수 있으며, 다른 Linux 배포판에서도 비슷한 명령어를 쓰면 됩니다. Windows에서는 추가 단계가 필요하므로 [`node-gyp` 설치 안내](https://github.com/nodejs/node-gyp#installation)를 참고하세요.
- Git 사용에 익숙해야 합니다.

## 개발 워크플로우 {/*development-workflow*/}

React 저장소를 클론한 뒤 `yarn`으로 의존성을 설치하면 다음 명령어를 사용할 수 있습니다.

- `yarn lint`: 코드 스타일을 검사합니다.
- `yarn linc`: `yarn lint`와 같지만 브랜치에서 변경된 파일만 검사하므로 더 빠릅니다.
- `yarn test`: 전체 테스트를 실행합니다.
- `yarn test --watch`: 대화형 감시 모드로 테스트를 실행합니다.
- `yarn test --prod`: 프로덕션 환경에서 테스트를 실행합니다.
- `yarn test <pattern>`: 파일 이름이 패턴과 일치하는 테스트만 실행합니다.
- `yarn debug-test`: `yarn test`와 같지만 디버거를 사용할 수 있습니다. `chrome://inspect`를 열고 "Inspect"를 누르세요.
- `yarn flow`: [Flow](https://flow.org/) 타입 검사를 실행합니다.
- `yarn build`: 모든 패키지를 포함한 `build` 폴더를 만듭니다.
- `yarn prettier`: 변경된 파일을 Prettier로 정리합니다.

변경 사항이 문제를 일으키지 않는지 확인하려면 `yarn test` 또는 위의 변형 명령어를 사용하세요. 직접 만든 프로젝트에서 React 빌드를 사용해 보는 것도 좋습니다.

먼저 `yarn build`를 실행합니다. 그러면 `build` 폴더에 미리 빌드된 번들이 만들어지고 `build/node_modules`에 npm 패키지가 준비됩니다.

변경 사항을 기존 React 프로젝트에서 시험해 보려면 `build/node_modules/react/umd/react.development.js`, `build/node_modules/react-dom/umd/react-dom.development.js` 등의 빌드 파일을 프로젝트의 HTML 파일에 복사해 테스트하면 됩니다.

npm으로 설치한 React를 로컬 빌드로 바꾸려면 [`yarn link`](https://yarnpkg.com/lang/en/docs/cli/link/)를 사용하세요.

```bash
cd ~/path_to_your_react_clone/
yarn build react/index,react/jsx,react-dom/index,scheduler --type=NODE

cd build/node_modules/react
yarn link
cd build/node_modules/react-dom
yarn link

cd ~/path/to/your/project
yarn link react react-dom
```

React 폴더에서 `yarn build`를 실행할 때마다 프로젝트의 `node_modules`에 최신 버전이 반영됩니다. 그런 다음 프로젝트를 다시 빌드해서 변경 사항을 확인할 수 있습니다.

Pull Request에는 새 기능에 대한 단위 테스트를 함께 포함해 주세요. 그래야 이후 변경으로 코드가 깨지는 일을 막을 수 있습니다.

## 스타일 가이드 {/*style-guide*/}

[Prettier](https://prettier.io/)라는 자동 코드 포매터를 사용합니다. 코드를 변경한 뒤에는 `yarn prettier`를 실행하세요.

린터는 코드에서 문제가 될 수 있는 부분을 대부분 찾아냅니다. `yarn linc`로 코드 스타일 상태를 확인할 수 있습니다.

다만 린터가 잡아내지 못하는 스타일도 있습니다. 확실하지 않은 부분은 [Airbnb 스타일 가이드](https://github.com/airbnb/javascript)를 참고하세요.

## 의견 요청(RFC) {/*request-for-comments-rfc*/}

버그 수정이나 문서 개선 같은 변경은 일반적인 GitHub Pull Request 워크플로우로 제안하고 리뷰할 수 있습니다.

하지만 규모가 큰 변경은 설계 과정을 거쳐 React 핵심 팀의 합의를 얻는 것이 좋습니다. 이처럼 "RFC"(의견 요청) 절차는 새 기능이 프로젝트에 들어가는 과정을 일관되고 체계적으로 관리하기 위한 것입니다. [RFC 저장소](https://github.com/reactjs/rfcs)를 방문해 기여해 보세요.

## 라이선스 {/*license*/}

React에 기여하면 기여한 내용에 MIT 라이선스가 적용되는 데 동의하는 것으로 간주합니다.

## 다음 단계 {/*what-next*/}

[코드베이스 개요](/learn/codebase-overview)를 읽으면 React 코드베이스가 어떻게 구성되어 있는지 알 수 있습니다.
