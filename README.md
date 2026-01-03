# FastAPI SDD Project (with Spec-Kit)

이 프로젝트는 **바이브 코딩(Vibe Coding)** 트렌드에 맞춰, GitHub의 [Spec-Kit](https://github.com/github/spec-kit)을 활용한 **사양 주도 개발(Spec-Driven Development, SDD)**을 실험하고 실무에 적용하기 위한 템플릿입니다.

## 🚀 Concept
- **Agent-Centric**: Antigravity 및 최신 AI 에이전트가 읽고 실행할 수 있는 명확한 스펙(Spec)을 우선합니다.
- **Spec over Code**: 코드를 먼저 짜는 것이 아니라, `specify` CLI를 통해 `specs/` -> `plans/` -> `tasks/` 순서로 사고 과정을 기록합니다.
- **FastAPI Optimized**: Pydantic v2와 Python 3.12+의 최신 기능을 활용하여 타입 안정성과 자동 문서화(OpenAPI)를 극대화합니다.

- **Constitution (`.specify/memory/constitution.md`)**: 프로젝트의 모든 작업은 이 헌법에 정의된 Git Workflow, SDD 프로세스, Clean Architecture 원칙을 따릅니다. Agent는 작업을 시작하기 전에 반드시 이 문서를 숙지해야 합니다.

## 🛠 Tech Stack
- **Framework**: FastAPI
- **Package Manager**: uv
- **SDD Tool**: Spec-Kit (`specify` CLI)
- **Runtime**: Python 3.12+

## Quick Start

### Installation
```bash
uv sync  # or pip install -r requirements.txt
```

### Run Server
```bash
uv run uvicorn app.main:app --reload
```
> **API Check**: 서버 실행 후 다음 주소에서 엔드포인트를 확인할 수 있습니다.
> - **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
> - **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Run Tests
```bash
uv run pytest
```

## 4. 프로젝트 구조 (Clean Architecture)
이 프로젝트는 엄격한 **Clean Architecture** 구조를 따릅니다:

```
app/
├── main.py              # 애플리케이션 진입점 (Entrypoint)
├── api/                 # 프레젠테이션 계층 (라우트, 의존성 주입)
│   └── v1/
├── core/                # 핵심 유틸리티, 설정, 예외 처리
├── services/            # 애플리케이션 계층 (비즈니스 로직, 유스케이스)
├── domain/              # 도메인 계층 (엔티티, 레포지토리 인터페이스)
│   ├── models/
│   └── repository_interfaces/
└── infrastructure/      # 인프라 계층 (DB, 외부 API)
```

## 📚 문서 (Documentation)
- **상세 문서**: [docs/](docs/)
  - **[Clean Architecture Q&A](docs/clean_architecture_qna.md)**: 아키텍처 관련 질의응답.
  - **[Database Strategy](docs/database_strategy.md)**: SQLModel, Alembic, Asyncpg 사용 배경.
  - **[Database Migration Guide (Safety Manual)](docs/database_migration_guide.md)**: ⚠️ 안전한 스키마 변경을 위한 운영 매뉴얼.
- **기능 명세 (Specs)**: [specs/](specs/)
- **아키텍처 헌법**: [Constitution](.specify/memory/constitution.md)

## 🤖 AI 에이전트 가이드 (AI Agent Guide)
이 프로젝트는 AI 에이전트 친화적으로 설계되었습니다. 에이전트(또는 에이전트 역할을 하는 사람)는 다음을 필독하세요:
- **부트스트랩 프로토콜**: [agent.md](agent.md) (가장 먼저 읽으세요!)
- **헌법 (Constitution)**: [.specify/memory/constitution.md](.specify/memory/constitution.md) (최상위 규칙)

## 📜 기여 가이드 (Contributing)
모든 기여는 `agent.md`에 정의된 **Strict SDD** 워크플로우를 따라야 합니다.
1. **Branch First**: 항상 새로운 브랜치를 생성하세요.
2. **Plan First**: 먼저 계획을 제안하고 승인을 받으세요.
3. **Spec-Kit**: 가능한 경우 `spec-kit` 도구를 사용하세요.

## 📝 워크플로우 (Workflow)
1. **Specify**: 기능 명세 작성 (`specs/{branch}/spec.md`)
2. **Clarify**: 요구사항 구체화 및 질문 해결
3. **Plan**: 기술 설계 및 아키텍처 수립
4. **Tasks**: 구현 작업 단위 분해
5. **Analyze**: 기존 코드 영향도 분석
6. **Implement**: 코드 구현 및 테스트

## 🧪 테스트 (Testing)
테스트는 `pytest`를 사용합니다.

```bash
uv run pytest
```

### 테스트 전략 (DB 격리)
실제 데이터베이스(예: Supabase) 오염을 방지하기 위해 **In-Memory SQLite**를 사용합니다.
- **Run-time**: 앱은 `.env` 설정을 통해 실제 DB(PostgreSQL)에 연결합니다.
- **Test-time**: `tests/conftest.py`가 DB 의존성을 `sqlite+aiosqlite:///:memory:`로 오버라이드합니다.
- 이를 통해 어디서든 빠르고 안전하게 테스트를 수행할 수 있습니다.

> 💡 자세한 절차는 [Constitution](.specify/memory/constitution.md)을 참고하세요.


## 🚀 학습 로드맵 (To-Do)
- [x] ~~**1. Configuration**: `pydantic-settings` 및 `.env` 파일 구현.~~
- [x] ~~**2. Real Database**: InMemory를 `SQLModel` & `SQLite`로 교체 (실제: Supabase PostgreSQL).~~
- [x] ~~**3. Async Database**: Repository/Service를 `async`/`await`로 변환 (Real DB와 함께 완료).~~
- [x] ~~**4. Migrations**: `Alembic`을 이용한 데이터베이스 스키마 관리.~~
- [x] ~~**5. Dependency Injection**: `Depends`를 사용하여 `main.py` 의존성 체인 리팩토링.~~
- [x] ~~**6. Item Validation**: Item 모델에 엄격한 Pydantic validator 적용.~~
- [ ] **7. Authentication**: JWT 로그인 및 사용자 도메인 구현.

---
*Generated by Vibe Coding with Agentic Workflow.*
