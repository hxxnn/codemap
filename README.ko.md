# codemap

> 어떤 코드베이스든 아키텍처 다이어그램, 의존성 그래프, 마인드맵, 실행 흐름, 온보딩 가이드로 바꿔 줍니다. **"이렇게 만들었다"를 다른 사람에게 설명**할 때 쓰세요.

[English README](README.md)

`codemap`은 Claude Code용 플러그인입니다. Claude가 코드를 직접 읽고, Mermaid 다이어그램과 설명 문서를 `docs/codemap/`에 만듭니다(원하면 인터랙티브 HTML로도). 플러그인 외에 설치할 것은 없고, Claude가 읽을 수 있는 언어라면 모두 사용할 수 있습니다.

## 설치

Claude Code에서:

```
/plugin marketplace add hxxnn/codemap
/plugin install codemap@codemap
```

## 업데이트

설치한 플러그인은 자동 업데이트를 켜지 않으면 저절로 바뀌지 않습니다. `/plugin` → **Marketplaces** → `codemap` → **Enable auto-update**로 켜거나, 직접 업데이트한 뒤 Claude Code를 재시작하세요.

```
/plugin marketplace update codemap
/plugin install codemap@codemap
```

터미널에서는 `claude plugin update codemap@codemap`으로도 됩니다. 이 플러그인에는 고정된 버전 번호가 없어서, `main`에 새 커밋이 올라가면 업데이트하는 사람에게는 모두 새 버전으로 인식됩니다.

## 사용법

프로젝트를 Claude Code로 열고 실행합니다.

```
/codemap
```

하나만 고를 수도 있습니다. HTML 페이지는 기본으로 함께 만들어지고, 마크다운만 원하면 `--no-html`을 붙입니다.

```
/codemap architecture --no-html
/codemap deps
/codemap mindmap
/codemap sequence
/codemap doc
/codemap present
/codemap refresh
```

"이 프로젝트 구조를 그려줘"처럼 말로 요청해도 됩니다. 결과물은 기본적으로 한국어로 작성됩니다. 다른 언어가 필요하면 "영어로"처럼 명시해서 요청하세요.

## 클라우드 세션에서 쓰기 (claude.ai/code, 모바일, `--cloud`)

클라우드 세션에서는 마켓플레이스 플러그인을 설치할 수 없습니다(`/plugin` 명령이 없습니다). 대신 저장소에 커밋된 `.claude/` 폴더는 불러옵니다. 아래 스크립트가 codemap을 프로젝트의 `.claude/` 폴더로 복사해 줍니다.

```
git clone https://github.com/hxxnn/codemap
python3 codemap/scripts/install_into_project.py /path/to/your/project
```

그다음 프로젝트의 `.claude/` 폴더를 커밋하고 push하세요. 그 저장소의 클라우드 세션에서 `/codemap`과 스킬이 플러그인과 똑같이 동작합니다(스킬 이름 앞에 `codemap:`이 붙지 않는 점만 다릅니다).

- 업데이트하려면 `codemap`을 최신으로 받아서 스크립트를 다시 실행하세요. 직접 수정한 파일은 덮어쓰지 않고, 충돌이라고 알리며 아무것도 쓰지 않습니다(`--force`를 붙이면 덮어씁니다).
- 한 프로젝트에서는 플러그인과 이 복사본 중 하나만 쓰세요. 둘 다 쓰면 스킬이 두 번씩 보입니다.

## 만들어지는 것

| 명령 | 스킬 | 결과물 (`docs/codemap/`) |
|---|---|---|
| `/codemap architecture` | `architecture-overview` | `architecture.md` — 시스템 → 컨테이너 → 컴포넌트 순으로 확대하는 C4 방식 |
| `/codemap deps` | `dependency-graph` | `dependency-graph.md` — 실제 import 기반 그래프, 순환 의존 표시 |
| `/codemap mindmap` | `mindmap` | `mindmap.md` — 폴더와 기능을 하나의 마인드맵으로 |
| `/codemap sequence` | `sequence-flow` | `sequence-flow.md` — 코드를 따라가며 그린 실행 흐름 2~3개 |
| `/codemap doc` | `design-doc` | `design-doc.md` — 설계 개요, 핵심 선택, "이 순서로 읽으세요" 가이드 |
| `/codemap present` | `present` | `present.md` — 다른 결과물로 만든 5~7장 발표 개요 |
| `/codemap refresh` | `codemap-refresh` | 코드가 바뀐 파일만 갱신하고, 직접 수정한 부분은 보존 |

마크다운 파일마다 `docs/codemap/html/<이름>.html`이 함께 만들어집니다(`--no-html`을 붙이면 만들지 않습니다). 목차 사이드바, 색 범례, 줄어들지 않고 스크롤되는 확대·축소 다이어그램, 접을 수 있는 섹션, 검색, 라이트/다크 전환, 인쇄용 레이아웃이 파일 하나에 들어 있습니다. 발표 개요(`present.html`)에는 슬라이드 모드(방향키로 이동, `Esc`로 종료)가 있습니다. 글꼴은 버전을 고정해 CDN에서 불러오는 Pretendard이고, 오프라인에서는 시스템 글꼴로 대체되며 다이어그램은 원본과 안내 문구로 보입니다.

## 신뢰성

- 결과물에 나오는 파일과 모듈은 Claude가 실제로 읽은 것입니다. 확인하지 못한 내용은 "추정"으로 표시하고 `<!-- codemap:unverified -->` 마커를 붙입니다.
- 모든 파일 끝에는 읽지 못한 범위를 적은 "다루지 않은 범위"가 있습니다(큰 저장소는 진입점에서 바깥쪽으로 읽습니다).
- `<!-- codemap:manual-start -->`와 `<!-- codemap:manual-end -->` 사이는 사용자 영역이라 `refresh`가 덮어쓰지 않습니다.
- 이미 있는 `docs/codemap/` 파일은 묻지 않고 덮어쓰지 않습니다. 단 `refresh`는 예외입니다. 갱신을 요청하셨기 때문이며, 직접 수정한 블록은 보존합니다. 블록 밖에서 고친 내용은 refresh 때 바뀝니다.

## 예시

이 저장소의 작은 샘플 프로젝트로 만든 결과물입니다.

- [`examples/python-todo-api/docs/codemap/`](examples/python-todo-api/docs/codemap/)
- [`examples/ts-notes-cli/docs/codemap/`](examples/ts-notes-cli/docs/codemap/)
- [`examples/edge-names/docs/codemap/`](examples/edge-names/docs/codemap/) — 공백과 한글이 들어간 파일 이름

## 디자인 바꾸기

| 바꾸고 싶은 것 | 고칠 파일 |
|---|---|
| HTML의 색, 레이아웃, 글꼴, 조작 버튼 | `skills/_shared/html-template.html` |
| Mermaid 스타일과 라벨 규칙 | `skills/_shared/mermaid-rules.md` |
| 언어, 파일 위치, 메타데이터 | `skills/_shared/language-and-output.md` |
| 각 문서에 담기는 내용 | `skills/<이름>/SKILL.md` |

## 개발

로컬 폴더로 플러그인을 시험해 볼 수 있습니다.

```
claude --plugin-dir /path/to/codemap
```

생성된 결과물을 원본 프로젝트와 대조해 검사합니다(언급된 경로가 모두 존재해야 하고, 다이어그램이 렌더링되어야 합니다).

```
python3 scripts/check_output.py <프로젝트_폴더> <프로젝트_폴더>/docs/codemap --render
pytest scripts/tests
python3 scripts/rebuild_example_html.py   # 예시 HTML 페이지에 템플릿을 다시 적용
node scripts/browser_check.js <page.html> [--deck] [--offline]   # 실제 브라우저로 페이지 검사 (Playwright 필요)
```

설계와 구현 계획은 [`docs/design/codemap-design.md`](docs/design/codemap-design.md), [`docs/superpowers/plans/2026-11-05-codemap-plugin.md`](docs/superpowers/plans/2026-11-05-codemap-plugin.md)에 있습니다.

## 라이선스

MIT — [LICENSE](LICENSE) 참고.
