# relation-map 설계 (2026-11-12)

## 목적
개발 중인 폴더의 파일들을 **코드에서 확인되는 관계**로 연결해, 한 화면에서 전체를 훑고(전체화면), 파일 하나에 마우스를 올리면 그 파일과 직접 연결된 파일이 함께 강조되게 한다. 만든 구조를 다른 사람에게 이해시키고 설명하는 것이 목적이다(codemap의 기존 목적과 같다).

## 확정된 결정
- 연관 기준: import/require/use로 실제 확인되는 관계만. 테스트→소스 import는 같은 선이되 종류(`test`)로 구분. 기능/역할 묶음 같은 모델 해석은 이번 범위 밖.
- 방식: 새 스킬 + 공유 `codemap.js`가 SVG로 그림. 외부 라이브러리를 추가하지 않는다. 기존 `dependency-graph`(Mermaid)는 유지한다.
- 강조 범위: 직접 연결(1단계)만. 2단계 이상 토글은 범위 밖(YAGNI).

## 1. 스킬과 산출물
- 이름 `relation-map`, 호출 `/codemap relations`. 기본 3종에는 넣지 않고 `all`에 포함(`all` = 7종).
- 산출물: `docs/codemap/relation-map.md`(원본)와 `docs/codemap/html/relation-map.html`.
  - `.md`는 기존 계약(front matter, 한 줄 `sources`, `codemap:manual-start/end`, "다루지 않은 범위")을 따른다.
  - 본문은 Mermaid 대신 파일 표: `파일 | 한 줄 역할 | 이 파일이 쓰는 파일 | 이 파일을 쓰는 파일`. 이 표가 HTML 그래프의 데이터 원본이다. 아래에 많이 쓰이는 파일(허브)과 순환 의존 요약.
- 근거 규칙은 `dependency-graph`와 같다: 실제로 읽은 import 문만 연결, 외부 패키지 제외. 동적 import/리플렉션은 선으로 긋지 않고 "(추정)"과 `<!-- codemap:unverified -->`로만 남긴다.
- `--no-html`이면 문서만 만들고 인터랙티브 화면이 빠졌음을 알린다.

## 2. HTML 데이터 형식과 화면 동작
모델은 평범한 HTML 목록만 쓴다(`<script>`, 이벤트 핸들러 금지, 본문 텍스트 이스케이프).

```html
<ul class="cm-graph">
  <li id="g1" data-group="app/api" data-kind="source">
    <code>app/api/routes.py</code> 요청을 받아 서비스로 넘김
    <ul><li data-to="g2"></li><li data-to="g5"></li></ul>
  </li>
</ul>
```

- 선은 "쓰는 쪽 → 쓰이는 쪽" 한 방향만 적는다. 역방향은 JS가 계산한다.
- `data-kind` 값: `source`, `test`, `unverified`(점선).
- 이 `<ul>`은 JS를 쓸 수 없거나 인쇄할 때의 폴백으로 남는다.

`codemap.js`(공유 자산)가 하는 일:
- `ul.cm-graph`를 SVG 그래프로 바꾼다. `data-group`(폴더)마다 상자를 두고 안에 파일을 세로로 나열, 상자는 격자 배치, 선은 곡선.
- 마우스를 올리면 직접 연결된 파일(쓰는 쪽/쓰이는 쪽)만 켜고 나머지는 흐리게. 두 방향은 색으로 구분.
- 클릭하면 선택 고정, 다시 클릭 또는 `Esc`로 해제. 키보드 포커스와 터치(탭)도 동일하게 동작.
- 선택 시 옆 패널에 경로, 한 줄 역할, 쓰는 파일/쓰이는 파일 목록.
- 전체화면 버튼: 브라우저 전체화면 기능을 먼저 시도하고, 막히면 화면 전체를 덮는 방식으로 대체. `Esc`로 종료. 확대/축소/맞춤과 드래그 이동은 기존 줌 컨트롤을 재사용.
- 파일이 많으면(예: 80개 이상) 폴더 상자를 접은 상태로 시작. 접힌 상자 사이는 연결 개수로 합쳐 보여 주고, 클릭하면 펼친다.
- 색과 글꼴은 기존 CSS 토큰을 사용해 다크 모드와 인쇄 폭을 따른다. 자산 첫 줄 버전 표시(`/* codemap html assets vN */`)를 올린다.

## 3. 검증과 변경 범위
변경 파일:
- 신규: `skills/relation-map/SKILL.md`
- 수정: `commands/codemap.md`, `skills/_shared/assets/codemap.js`, `skills/_shared/assets/codemap.css`, `scripts/check_output.py`(+`scripts/tests/`), `scripts/browser_check.js`, `scripts/install_into_project.py`, `scripts/rebuild_example_html.py`(필요 시), README 두 개, `index.html`, `CLAUDE.md`
- 예시: 기존 예시 3개(`python-todo-api`, `ts-notes-cli`, `edge-names`)에서 `/codemap relations`를 실제로 돌려 산출물 생성.

검사기 규칙(TDD, 실패하는 테스트부터):
- `data-to`가 가리키는 id가 존재, id 중복 없음, 자기 자신으로 가는 선 없음.
- 노드 `<code>` 경로가 저장소에 실제로 존재.
- `.md` 파일 표와 HTML 그래프의 연결이 일치.
- `<script>`, 이벤트 핸들러, 외부 링크 없음.
- 정상 페이지는 통과, 일부러 고장 낸 페이지는 실패함을 함께 확인.

브라우저 검사: hover 강조(직접 연결만 켜짐, 나머지 흐림), 클릭 고정과 `Esc` 해제, 전체화면 진입/종료, 접힌 상자 펼침, 다크 모드와 인쇄 폭, 합성 600파일 그래프의 배치와 반응 속도.

## 진행 순서
1. 데이터 형식과 검사기 테스트 작성 → 실패 확인 → 구현.
2. 공유 JS/CSS 구현, 손으로 만든 샘플 HTML로 브라우저 검사 통과.
3. `SKILL.md`와 명령 연결.
4. 예시 프로젝트에서 모델이 지침을 실제로 따르는지 실행으로 확인(한 프로젝트씩), 검사 2~4단계 적용.
5. 문서와 갤러리 갱신.
6. 작업 브랜치에 커밋/push. PR은 요청 시에만.

## 알려진 위험과 미확인
- 이 클라우드 환경에서 모델 실행 검증(`claude -p ... --plugin-dir`)이 가능한지 미확인. 불가하면 "검사기와 브라우저 검사까지 통과, 모델의 지침 준수는 미확인"으로 구분해 보고한다.
- 그래프 배치 알고리즘은 직접 구현한다. 큰 그래프에서 읽기 어려우면 접힘 기준값을 조정한다.
- `all`이 6종에서 7종으로 늘어 실행 시간이 길어진다(사용 한도 주의, 한 프로젝트씩 순서대로).
