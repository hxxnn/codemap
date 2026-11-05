---
codemap: 1
skill: architecture-overview
generated_at: 2026-11-05
commit: null
sources: {package.json: ae5b4fc82dbaebc1fe8d80c1ac2975a5ef58fcb05a0e74481a1cf90fe72baad0, README.md: 20617bb945b32699044b85affe89774ed9278ec9a9586b92f1528162c250eddc, src/main.js: 9e804869935ddb2b3f3810001cc21e6b56debf2aefa9e2b6a85b5dc5ca172cd9, src/my utils.js: 305439bc482c12b23f78d0d9a2175edcaf9d6aa2a4fc8faee9e6edc7125fac8c}
---
<!-- codemap: generated file — hand edits outside a manual-edit block are replaced by /codemap refresh -->

# 아키텍처 개요

`edge-names`는 공백과 한글이 들어간 파일 이름을 다루는 아주 작은 Node.js(CommonJS) 프로젝트이며, 아래에서 세 단계로 확대하며 구조를 보여 줍니다.

## 1단계: 시스템 컨텍스트

```mermaid
flowchart LR
  u["실행하는 사람"]:::external
  s["edge-names (src/main.js)"]
  o["콘솔 출력 (stdout)"]:::external
  u -->|"node로 실행"| s
  s -->|"console.log"| o
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

사람이 `package.json`의 `main`으로 지정된 `src/main.js`를 실행하면, 프로그램은 결과를 콘솔(표준 출력)에만 씁니다. 데이터베이스나 외부 API 호출은 코드에서 발견되지 않았습니다.

## 2단계: 컨테이너

```mermaid
flowchart LR
  u["실행하는 사람"]:::external
  c["Node.js 스크립트 (src/)"]
  o["콘솔 출력 (stdout)"]:::external
  u -->|"실행"| c
  c -->|"한 줄씩 출력"| o
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

배포 단위는 `src/` 폴더의 Node.js 스크립트 하나뿐이며, 서버·워커·저장소 같은 별도 프로세스는 없습니다.

## 3단계: 컴포넌트

```mermaid
flowchart LR
  o["콘솔 출력 (stdout)"]:::external
  subgraph g["src/"]
    m["진입점 (src/main.js)"]
    ut["문자열 유틸 (src/my utils.js)"]
    ld["데이터 로더 (src/데이터 로더.js)"]
  end
  m -->|"shout()"| ut
  m -->|"loadItems()"| ld
  m -->|"console.log"| o
  classDef external fill:#E3F4F1,stroke:#0E8F83,color:#0B4F49
```

`src/main.js`가 두 모듈을 `require`로 불러와 `loadItems()`로 얻은 각 항목을 `shout()`으로 바꿔 출력하며, 두 모듈은 서로를 부르지 않습니다.

## 다루지 않은 범위

저장소의 소스 3개(`src/main.js`, `src/my utils.js`, `src/데이터 로더.js`)와 `package.json`, `README.md`를 모두 읽었습니다. 다만 `src/데이터 로더.js`는 경로에 한글이 있어 해시 안전 규칙(허용 문자 제한)을 통과하지 못해 front matter의 `sources`에서 빠져 있습니다 (확인 필요) <!-- codemap:unverified -->.
