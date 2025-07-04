# 📖 GI_Agent 개발 가이드라인 (Memory Bank)

> 이 문서는 GI_Agent 프로젝트의 일관성 있는 개발을 위한 핵심 원칙과 규칙을 담고 있습니다.  
> 새로운 브랜치에서 개발을 시작하기 전, 반드시 이 문서를 숙지하십시오.

---

## 1. 🎯 프로젝트 핵심 목표

- **프로젝트명**: GI_Agent (록톤 코리아 보험중개 업무 자동화 플랫폼)
- **핵심 분야**: 에너지 산업 & 방위 산업 전문 보험중개
- **개발 비전**: AI를 활용하여 시장정보, 뉴스, 입찰공고, 고객정보 등을 체계적으로 관리하고, 전문적인 의사결정을 지원하는 플랫폼 구축

---

## 2. 🛠️ 기술 및 개발 환경

- **Frontend**: `HTML`, `CSS`, `JavaScript`
- **UI Framework**: `Bootstrap 5` (일관된 UI/UX 유지를 위해 필수)
- **Charts**: `Chart.js` (시장정보 대시보드 시각화 표준)
- **Deployment**: `GitHub Pages` (main 브랜치 자동 배포)
- **로컬 개발 환경**: `d:\AI_Project\GI_Agent`

---

## 3. 💾 데이터 처리 원칙 (매우 중요)

- **데이터 소스**: 모든 동적 콘텐츠(뉴스, 시장 데이터 등)는 **반드시 `JSON` 파일을 통해 제공**합니다.
- **구조**:
    - 뉴스 데이터: `news_clipping/news_data.json`
    - 시장 정보 데이터: `market_info/data/market_data.json`
- **원칙**: HTML 파일에 데이터를 직접 하드코딩하지 않고, JavaScript가 `fetch` API를 사용하여 JSON 파일을 비동기적으로 로드하고 화면에 렌더링하는 방식을 유지합니다. 이는 기능 확장 및 유지보수를 위함입니다.

---

## 4. 🌿 브랜치 전략 및 코드 관리

- **`main`**: 최종 배포 브랜치. 직접적인 commit을 금지합니다.
- **`develop`**: 개발 통합 브랜치. 기능 개발 완료 후 이곳으로 병합(Merge)합니다.
- **`feature/{기능명}`**: 신규 기능 개발 브랜치. `develop`에서 생성하여 개발을 진행합니다.
- **Commit**: 명확하고 의미 있는 메시지를 작성합니다.
- **Pull Request (PR)**: `develop` 브랜치로 병합하기 전, 코드 리뷰를 위해 PR을 생성하는 것을 원칙으로 합니다.

---

## 5. 🔑 API 키 및 보안

- **API 키 저장**: 모든 API 키는 `config/api_config.json` 파일 내에서 관리합니다.
- **보안**: `.gitignore`에 `config/api_config.json`를 추가하여 레포지토리에 API 키가 올라가지 않도록 합니다. (현재 설정 확인 필요)

---

## 6. 🌐 배포 규칙

- **레포지토리**: **`Public`**으로 유지되어야 GitHub Pages 사용이 가능합니다.
- **배포 주소**: `https://{username}.github.io/{repository-name}/`
- **하위 페이지 경로**: 메인 `index.html` 기준 상대 경로를 올바르게 설정해야 합니다.
  - 예: `./news_clipping/`, `./market_info/`

---

## 7. 🗂️ 현재까지 완료된 모듈 (구조 참조용)

1.  **메인 포털 (`/index.html`)**: 전체 네비게이션 허브
2.  **뉴스클리핑 (`/news_clipping/`)**: `news_data.json`을 사용한 동적 뉴스 목록
3.  **시장정보 대시보드 (`/market_info/`)**: `market_data.json`과 `Chart.js`를 사용한 탭 기반 대시보드 