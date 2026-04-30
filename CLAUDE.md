# Alpha Hunter — 프로젝트 규칙

## Project Overview
- **AI 히든젬 발굴 시스템** — 한국·미국·중국 시장에서 데이터 기반 숨은 보물 종목 발굴
- GitHub Pages: https://waterfirst.github.io/alpha-hunter/
- 저자: Nakcho Choi | Chimera AI x Alpha Hunter

## Important Rules

### 1. 개인 연금 콘텐츠 금지
- **개인 연금(pension) 관련 콘텐츠는 이 프로젝트에 포함하지 않는다.**
- pension_dashboard.py 등 연금 관련 파일은 생성·커밋하지 않는다.
- 연금 포트폴리오 제안, 퇴직연금/개인연금 잔고 등 개인 재정 정보 금지.

### 2. Chimera-AI 주간 보고서는 별도 저장소
- Chimera-AI 주간 증시 보고서는 이 저장소에 넣지 않는다.
- chimera-weekly-*.html / chimera-weekly-*.qmd 파일은 chimera-ai 저장소에서 관리.
- Chimera-AI 저장소: https://github.com/waterfirst/chimera-ai

## 기술 스택

### 필수 사항
- **R + ggplot2** — 차트 생성 (Plotly 사용 금지, 파일 용량 문제)
- **Quarto (.qmd)** — 보고서 렌더링
- `lightbox: true` — 차트 클릭 시 줌인
- `embed-resources: true` — 단일 HTML 배포
- `dev: ragg_png` — CJK 폰트 렌더링
- 폰트: `"Noto Sans CJK KR"` (시스템 폰트 직접 사용, showtext 사용 금지)

### 금지 사항
- **3자리 hex 색상 금지** — `"#aaa"` 사용 금지, 반드시 `"#aaaaaa"` 6자리 (Quarto+ragg 호환 문제)
- **showtext 사용 금지** — Quarto knitr 환경에서 충돌
- **Plotly 사용 금지** — 파일 용량 비대

### Quarto YAML 헤더 템플릿
```yaml
---
title: "종목명 (코드) 기업 분석 보고서"
subtitle: "Alpha Hunter Hidden Gem Week N — 한줄 요약"
author: "Alpha Hunter × Chimera AI"
date: "YYYY-MM-DD"
format:
  html:
    theme:
      dark: darkly
      light: flatly
    toc: true
    toc-depth: 3
    number-sections: true
    code-fold: true
    smooth-scroll: true
    embed-resources: true
    lightbox: true
knitr:
  opts_chunk:
    dev: ragg_png
    dpi: 150
execute:
  echo: false
  warning: false
  message: false
---
```

### ggplot2 다크 테마 함수
```r
kfont <- "Noto Sans CJK KR"

theme_hunter <- function(base_size = 13) {
  theme_minimal(base_size = base_size) +
    theme(
      plot.background = element_rect(fill = "#1a1a2e", color = NA),
      panel.background = element_rect(fill = "#1a1a2e", color = NA),
      panel.grid.major = element_line(color = "#2a2a4a", linewidth = 0.3),
      panel.grid.minor = element_blank(),
      text = element_text(family = kfont, color = "#e4e4ec"),
      axis.text = element_text(color = "#aaaaaa"),
      axis.title = element_text(color = "#cccccc", size = rel(0.9)),
      plot.title = element_text(color = "#f59e0b", face = "bold", size = rel(1.2)),
      plot.subtitle = element_text(color = "#888888", size = rel(0.85)),
      plot.caption = element_text(color = "#666666", size = rel(0.7)),
      legend.background = element_rect(fill = "#1a1a2e", color = NA),
      legend.text = element_text(color = "#cccccc"),
      legend.title = element_text(color = "#f59e0b"),
      strip.text = element_text(color = "#f59e0b", face = "bold")
    )
}
```

### 파일 명명 규칙
```
gems/kr_종목명_wN.qmd / .html   # 한국 히든젬
gems/us_종목명_wN.qmd / .html   # 미국 히든젬
gems/cn_종목명_wN.qmd / .html   # 중국 히든젬
gems/sp_주제_날짜.qmd / .html   # 특별판
```

### 보고서 필수 차트 (최소 7개, lightbox 활성화)
각 차트 청크에 반드시 `#| lightbox: true` 추가:
1. 주가 추이 (52주)
2. 실적 추이 (매출/영업이익)
3. 밸류에이션 비교 (동종업종)
4. 워런 버핏 해자 레이더 차트
5. 피터 린치 스토리 점수
6. 리스크 팩터 대시보드
7. 매수/목표/손절가 시나리오

### 발행 절차
```bash
# 1. alpha-hunter 레포 클론
cd /tmp && git clone https://github.com/waterfirst/alpha-hunter.git

# 2. yfinance + 웹 검색으로 종목 데이터 수집

# 3. gems/XX_종목명_wN.qmd 작성 (위 YAML 헤더 사용)

# 4. Quarto 렌더링
cd /tmp/alpha-hunter/gems
quarto render XX_종목명_wN.qmd

# 5. index.html 목차 업데이트 (NEW 태그)

# 6. portfolio.json 업데이트

# 7. git commit & push origin main

# 8. cokacdir --sendfile로 텔레그램 전송
```

## Repository Structure
```
alpha-hunter/
├── index.html          # 매거진 메인 페이지 (목차)
├── hero.png            # 스플래시 이미지
├── CLAUDE.md           # 프로젝트 규칙 (이 파일)
├── portfolio.json      # 포트폴리오 추적
├── gems/               # 히든젬 보고서
│   ├── kr_종목명_wN.qmd / .html
│   ├── us_종목명_wN.qmd / .html
│   └── sp_주제.qmd / .html
└── reports/            # 기타 보고서
```

## Related Projects
- Chimera AI: https://github.com/waterfirst/chimera-ai (매크로 분석 기반)
- Insight Lab: https://github.com/waterfirst/insight-lab
- OLED Viewing Angle: https://github.com/waterfirst/oled-viewing-angle
