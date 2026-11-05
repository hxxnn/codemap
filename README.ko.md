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

"이 프로젝트 구조를 그려줘"처럼 말로 요청해도 됩니다. 결과물은 요청한 언어로 작성됩니다.

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

마크다운 파일마다 `docs/codemap/html/<이름>.html`이 함께 만들어집니다(`--no-html`을 붙이면 만들지 않습니다). 확대·축소되는 다이어그램, 접을 수 있는 섹션, 검색, 라이트/다크 전환이 파일 하나에 들어 있습니다.

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
```

설계와 구현 계획은 [`docs/design/codemap-design.md`](docs/design/codemap-design.md), [`docs/superpowers/plans/2026-11-05-codemap-plugin.md`](docs/superpowers/plans/2026-11-05-codemap-plugin.md)에 있습니다.

## 라이선스

MIT — [LICENSE](LICENSE) 참고.
