# Alpha Hunter — AI 히든젬 발굴 시스템

<context>
한국·미국·중국 시장에서 데이터 기반으로 숨은 보물 종목을 발굴하는 AI 주간 리서치 시스템.
GitHub Pages: https://waterfirst.github.io/alpha-hunter/
저자: Nakcho Choi | Chimera AI x Alpha Hunter

발행 스케줄:
- 화요일 19:00: 한국 히든젬
- 목요일 19:00: 미국 히든젬
- 금요일 19:00: 중국 히든젬
- 토요일 19:00: 주간 종합
</context>

<instructions>

## 콘텐츠 범위

이 저장소는 종목 발굴 리서치 보고서만 포함한다.

개인 재정(연금, 퇴직금, 재무설계 등) 콘텐츠는 이 프로젝트의 범위 밖이다.
pension 관련 파일이 발견되면 삭제한다.

Chimera-AI 주간 증시 보고서는 별도 저장소(https://github.com/waterfirst/chimera-ai)에서 관리한다.
chimera-weekly-*.html/qmd 파일은 이 저장소에 넣지 않는다.

모든 보고서에 면책 문구를 포함한다:
"이 프로젝트는 가상 투자 시뮬레이션 목적으로 작성되었습니다. 실제 투자 권유가 아닙니다."

</instructions>

<technical_stack>

## 기술 스택

R + ggplot2로 차트를 생성한다. Plotly는 파일 용량이 비대해지므로 사용하지 않는다.
Quarto (.qmd)로 보고서를 렌더링하며, 아래 설정을 따른다:

- `lightbox: true` — 차트를 클릭하면 줌인할 수 있어서 독자의 데이터 탐색 경험이 향상된다
- `embed-resources: true` — 단일 HTML로 배포
- `dev: ragg_png` — ragg 디바이스가 CJK 폰트를 정상 렌더링한다
- 폰트: `"Noto Sans CJK KR"` 시스템 폰트를 직접 사용한다. showtext는 Quarto knitr에서 grid.Call 충돌을 일으킨다.
- 색상: 6자리 hex만 사용한다 (`"#aaaaaa"`). 3자리(`"#aaa"`)는 에러를 발생시킨다.

</technical_stack>

<quarto_template>

## Quarto YAML 헤더 템플릿

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

</quarto_template>

<chart_theme>

## ggplot2 다크 테마

각 차트 청크에 `#| lightbox: true`를 추가한다.

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

</chart_theme>

<report_structure>

## 보고서 구조

파일명: `gems/XX_종목명_wN.qmd` (XX = kr/us/cn, N = 주차)

### 필수 차트 (최소 7개, 모두 `#| lightbox: true`)
1. 주가 추이 (52주)
2. 실적 추이 (매출/영업이익)
3. 밸류에이션 비교 (동종업종)
4. 워런 버핏 해자 레이더 차트
5. 피터 린치 스토리 점수
6. 리스크 팩터 대시보드
7. 매수/목표/손절가 시나리오

### 스크리닝 기준
- 매출성장 >20%, 영업이익률 >15%, Strong Buy 컨센서스
- 한국: 시총 5000억~10조 | 미국: $1B~$20B | 중국: $2B~$30B
- 독점기술, 해자(moat), 산업 트렌드 연결
- 카탈리스트(실적발표, 신제품, M&A, 정책 수혜) 확인

</report_structure>

<publishing_workflow>

## 발행 절차

```bash
# 1. 레포 클론
cd /tmp && git clone https://github.com/waterfirst/alpha-hunter.git

# 2. yfinance + 웹 검색으로 종목 데이터 수집

# 3. gems/XX_종목명_wN.qmd 작성 (위 YAML 헤더 + theme_hunter() 사용)

# 4. 렌더링
cd /tmp/alpha-hunter/gems && quarto render XX_종목명_wN.qmd

# 5. index.html 목차 업데이트, portfolio.json 갱신

# 6. 커밋 & 푸시
git add gems/ index.html portfolio.json
git commit -m "feat: XX_종목명 Week N 히든젬 보고서"
git push origin main

# 7. 텔레그램 전송
```

</publishing_workflow>

<investigate_before_answering>
코드를 수정하기 전에 반드시 해당 파일을 읽어라.
열지 않은 파일의 내용을 추측하지 말고, 실제 코드를 확인한 뒤 답변한다.
기존 gems/ 폴더의 보고서 스타일을 확인한 뒤 새 보고서를 작성한다.
yfinance에서 데이터를 가져올 수 없으면, 가져올 수 없다고 알리고 웹 검색 데이터로 대체한다. 데이터를 지어내지 않는다.
</investigate_before_answering>

<avoid_overengineering>
요청된 변경만 수행한다.
종목 분석에 집중하고, 불필요한 매크로 분석이나 포트폴리오 이론을 추가하지 않는다.
스크리닝 조건을 충족하는 종목이 없으면 "이번 주 조건 충족 종목 없음"으로 보고한다. 조건을 완화하여 억지로 종목을 선정하지 않는다.
</avoid_overengineering>

<frontend_aesthetics>
index.html을 수정할 때, 기존 매거진의 다크 테마(#08080f 배경, #f59e0b 액센트)와 카드 레이아웃을 유지한다.
나라별 태그 색상(t-kr: #c7254e, t-us: #3b82f6, t-cn: #dc2626)을 일관되게 사용한다.
</frontend_aesthetics>

## Repository Structure

```
alpha-hunter/
├── index.html          # 매거진 메인 페이지
├── hero.png            # 스플래시 이미지
├── CLAUDE.md           # 프로젝트 규칙 (이 파일)
├── portfolio.json      # 포트폴리오 추적
├── gems/               # 히든젬 보고서 (.qmd + .html)
└── reports/            # 기타 보고서
```

## Related Projects
- Chimera AI: https://github.com/waterfirst/chimera-ai
- Insight Lab: https://github.com/waterfirst/insight-lab
- OLED Viewing Angle: https://github.com/waterfirst/oled-viewing-angle
