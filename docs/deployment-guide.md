# 배포 가이드 (Deployment Guide)

이 문서는 FastAPI 애플리케이션을 **Render**에 배포하는 방법과 **GitHub Actions**를 통한 자동 배포(CD) 파이프라인에 대해 설명합니다.

## 🚀 배포 아키텍처

우리는 **Render의 Source Deployment (소스 기반 배포)** 방식을 사용합니다.

- **플랫폼**: [Render](https://render.com)
- **방식**: GitHub Repository 연동 -> `Dockerfile` 감지 -> Render 자체 빌드
- **자동화**: GitHub Actions (`deploy.yml`) -> Render Deploy Hook 호출

### 💡 왜 Docker Registry(GHCR) 이미지를 직접 쓰지 않나요?
원래는 GitHub Actions에서 Docker 이미지를 빌드하고, Render는 그 이미지를 가져다 쓰는(Pull) 방식이 더 이상적입니다 ("Build Once, Deploy Anywhere").

하지만 **Render Free Tier (무료 플랜)**에서는 다음과 같은 제약이 있어 **소스 기반 배포**가 더 효율적이라고 판단했습니다:
1.  **Private Registry 인증 복잡성**: GHCR 같은 외부 레지스트리의 Private 이미지를 가져오려면 별도의 유료 기능이나 복잡한 인증 설정이 필요합니다.
2.  **Public 이미지 강제**: 무료로 쉽게 쓰려면 이미지를 Public으로 열어야 하는데, 보안상 좋지 않습니다.
3.  **관리 효율성**: Render가 코드를 가져가서 직접 빌드하게 하면, 별도의 레지스트리 관리 없이 `Dockerfile` 하나만으로 배포가 가능합니다.

---

## 🛠️ 설정 방법 (Setup)

### 1. Render Web Service 생성
1.  Render 대시보드 [New +] -> [Web Service] 클릭.
2.  `Build and deploy from a Git repository` 선택.
3.  이 저장소(Repository) 연결.
4.  **Settings**:
    -   **Runtime**: Docker (자동 감지됨)
    -   **Instance Type**: Free
    -   **Environment Variables**:
        -   `DATABASE_URL`: Supabase Connection String (`user` 부분에 `app_user.project_id` 형식 사용 필수!)
        -   `SECRET_KEY`: 임의의 긴 문자열 (JWT 서명용)
        -   `PORT`: `8000`

### 2. Deploy Hook 설정 (CD 연동)
GitHub에 코드가 푸시되었을 때 Render에게 "배포해!"라고 알려주기 위한 설정입니다.

1.  **Render**: Settings -> `Deploy Hook` URL 복사.
2.  **GitHub**: Settings -> Secrets and variables -> Actions -> `New repository secret`
    -   **Name**: `RENDER_DEPLOY_HOOK_URL`
    -   **Value**: (복사한 URL 붙여넣기)

---

## 🤖 GitHub Actions 워크플로우
`.github/workflows/deploy.yml` 파일은 다음과 같이 동작합니다:

1.  `main` 브랜치에 코드가 푸시됨.
2.  Action이 실행되어 `RENDER_DEPLOY_HOOK_URL`로 `POST` 요청을 보냄.
3.  Render가 신호를 받고 최신 코드를 당겨와(Pull) 빌드 및 배포 시작.

```yaml
# deploy.yml 핵심 부분
- name: Trigger Render Deploy
  if: success() && env.RENDER_DEPLOY_HOOK_URL != ''
  run: |
    curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK_URL }}"
```
