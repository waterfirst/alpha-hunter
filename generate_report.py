#!/usr/bin/env python3
"""Alpha Hunter - 프로페셔널 투자 리포트 생성기"""

from PIL import Image, ImageDraw, ImageFont
import os, json, math

W, H = 1080, 3400
OUT_DIR = "/home/ubuntu/.cokacdir/workspace/cp7jpheo/alpha_hunter"

def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumSquareR.ttf",
        "/usr/share/fonts/truetype/nanum/NanumSquareB.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumSquare.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def gradient(draw, c1, c2, h=H):
    for y in range(h):
        r = int(c1[0]+(c2[0]-c1[0])*y/h)
        g = int(c1[1]+(c2[1]-c1[1])*y/h)
        b = int(c1[2]+(c2[2]-c1[2])*y/h)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

def ctext(draw, t, y, f, c):
    bb = draw.textbbox((0,0), t, font=f)
    draw.text(((W-(bb[2]-bb[0]))//2, y), t, font=f, fill=c)

def rbox(draw, x1, y1, x2, y2, r=16, fill=None, outline=None, width=1):
    draw.rounded_rectangle([x1,y1,x2,y2], radius=r, fill=fill, outline=outline, width=width)

def badge(draw, x, y, text, bg, fg=(255,255,255)):
    f = font(20, True)
    bb = draw.textbbox((0,0), text, font=f)
    tw = bb[2]-bb[0]
    rbox(draw, x, y, x+tw+24, y+32, r=10, fill=bg)
    draw.text((x+12, y+4), text, font=f, fill=fg)
    return tw+34

def progress_bar(draw, x, y, w, h, pct, fg, bg=(35,40,60)):
    rbox(draw, x, y, x+w, y+h, r=h//2, fill=bg)
    fw = max(h, int(w*min(max(pct,0),1)))
    rbox(draw, x, y, x+fw, y+h, r=h//2, fill=fg)

def draw_mini_chart(draw, x, y, w, h, data, color):
    """간단한 스파크라인 차트"""
    if not data or len(data) < 2:
        return
    mn, mx = min(data), max(data)
    rng = mx - mn if mx != mn else 1
    points = []
    for i, v in enumerate(data):
        px = x + int(i * w / (len(data)-1))
        py = y + h - int((v - mn) / rng * h)
        points.append((px, py))
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=color, width=2)
    # 마지막 점 강조
    lx, ly = points[-1]
    draw.ellipse([lx-4, ly-4, lx+4, ly+4], fill=color)

# ──────────────────────────────────────
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)
gradient(draw, (8, 12, 25), (15, 20, 40))

y = 30

# ═══ HEADER ═══
rbox(draw, 30, y, W-30, y+160, r=20, fill=(12, 20, 42), outline=(40, 80, 160), width=2)

# 로고 텍스트
draw.text((60, y+15), "ALPHA", font=font(56, True), fill=(60, 140, 255))
draw.text((280, y+15), "HUNTER", font=font(56, True), fill=(255, 255, 255))
draw.text((60, y+80), "Virtual Investment Research Report", font=font(26), fill=(100, 140, 200))
draw.text((60, y+115), "2026-04-02 | Portfolio Inception | Day 1", font=font(22), fill=(80, 110, 160))

# 뱃지들
bx = 600
badge(draw, bx, y+90, "LIVE", (200, 50, 50))
bx += 70
badge(draw, bx, y+90, "2 POSITIONS", (40, 100, 160))
bx += 160
badge(draw, bx, y+90, "$100K", (40, 120, 80))

y += 190

# ═══ PORTFOLIO OVERVIEW ═══
rbox(draw, 30, y, W-30, y+200, r=20, fill=(12, 22, 45), outline=(50, 90, 150))
draw.text((60, y+15), "PORTFOLIO OVERVIEW", font=font(24, True), fill=(80, 150, 255))
draw.line([(60, y+48), (W-60, y+48)], fill=(30, 60, 100))

# 총 자산
draw.text((60, y+60), "Total Value", font=font(20), fill=(100, 130, 170))
draw.text((60, y+85), "$100,000", font=font(48, True), fill=(255, 255, 255))

# 현금
draw.text((380, y+60), "Cash", font=font(20), fill=(100, 130, 170))
draw.text((380, y+85), "$14,020", font=font(36, True), fill=(100, 200, 160))
draw.text((380, y+130), "14.0%", font=font(22), fill=(80, 160, 130))

# 투자금
draw.text((600, y+60), "Invested", font=font(20), fill=(100, 130, 170))
draw.text((600, y+85), "$85,980", font=font(36, True), fill=(200, 180, 255))
draw.text((600, y+130), "86.0%", font=font(22), fill=(160, 140, 220))

# 배분 바
draw.text((60, y+160), "Allocation", font=font(18), fill=(80, 110, 150))
# AROC 50%, HPSP 36%, Cash 14%
rbox(draw, 200, y+158, W-60, y+180, r=8, fill=(30, 40, 60))
aroc_w = int((W-260) * 0.50)
hpsp_w = int((W-260) * 0.36)
cash_w = (W-260) - aroc_w - hpsp_w
rbox(draw, 200, y+158, 200+aroc_w, y+180, r=8, fill=(40, 140, 100))
rbox(draw, 200+aroc_w, y+158, 200+aroc_w+hpsp_w, y+180, r=8, fill=(120, 80, 200))
rbox(draw, 200+aroc_w+hpsp_w, y+158, W-60, y+180, r=8, fill=(60, 80, 60))

y += 220

# ═══ POSITION 1: AROC ═══
card_h = 880
rbox(draw, 30, y, W-30, y+card_h, r=20, fill=(10, 22, 40), outline=(50, 140, 100), width=2)

# 헤더
rbox(draw, 30, y, W-30, y+70, r=20, fill=(25, 60, 45))
# 하단 라운드 제거용
draw.rectangle([30, y+50, W-30, y+70], fill=(25, 60, 45))

draw.text((60, y+18), "AROC", font=font(36, True), fill=(100, 255, 160))
draw.text((210, y+25), "Archrock Inc.", font=font(28), fill=(200, 240, 210))
badge(draw, W-200, y+20, "STRONG BUY", (30, 120, 60))

cy = y + 85

# 기본 정보
draw.text((60, cy), "NYSE | Energy — Midstream Natural Gas Compression", font=font(20), fill=(100, 150, 140))
cy += 35

# 가격 블록
rbox(draw, 60, cy, 340, cy+110, r=12, fill=(15, 35, 30))
draw.text((80, cy+10), "Entry Price", font=font(18), fill=(80, 120, 110))
draw.text((80, cy+35), "$35.70", font=font(42, True), fill=(255, 255, 255))
draw.text((80, cy+82), "1,400 shares = $49,980", font=font(18), fill=(100, 150, 130))

rbox(draw, 360, cy, 540, cy+110, r=12, fill=(15, 40, 30))
draw.text((380, cy+10), "Target", font=font(18), fill=(80, 120, 110))
draw.text((380, cy+35), "$39.00", font=font(34, True), fill=(100, 255, 160))
draw.text((380, cy+75), "+9.2%", font=font(22, True), fill=(80, 200, 130))

rbox(draw, 560, cy, 740, cy+110, r=12, fill=(40, 20, 20))
draw.text((580, cy+10), "Stop Loss", font=font(18), fill=(150, 90, 90))
draw.text((580, cy+35), "$30.00", font=font(34, True), fill=(255, 120, 120))
draw.text((580, cy+75), "-16.0%", font=font(22, True), fill=(220, 90, 90))

rbox(draw, 760, cy, W-60, cy+110, r=12, fill=(20, 25, 45))
draw.text((780, cy+10), "Div Yield", font=font(18), fill=(100, 120, 160))
draw.text((780, cy+35), "2.4%", font=font(34, True), fill=(200, 180, 255))
draw.text((780, cy+75), "$0.88/yr", font=font(20), fill=(140, 130, 190))

cy += 130

# 펀더멘탈
draw.text((60, cy), "FUNDAMENTALS", font=font(20, True), fill=(80, 150, 255))
draw.line([(60, cy+28), (W-60, cy+28)], fill=(30, 60, 80))
cy += 38

items = [
    ("Market Cap", "$6.2B", (180,200,230)),
    ("P/E (TTM)", "19.5x", (180,200,230)),
    ("Fwd P/E", "18.9x", (180,200,230)),
    ("EPS", "$1.83", (180,200,230)),
    ("Rev '25", "$1.49B", (100,220,160)),
    ("Rev Growth", "+28.7%", (100,220,160)),
    ("EBITDA '25", "$900.9M", (100,220,160)),
    ("EBITDA Gr.", "+51%", (100,220,160)),
]

col = 0
row_y = cy
for label, val, vc in items:
    x = 60 + col * 250
    draw.text((x, row_y), label, font=font(18), fill=(90, 120, 150))
    draw.text((x, row_y+22), val, font=font(24, True), fill=vc)
    col += 1
    if col >= 4:
        col = 0
        row_y += 55

cy = row_y + 55

# 52주 레인지
draw.text((60, cy), "52-Week Range", font=font(18), fill=(90, 120, 150))
draw.text((60, cy+22), "$20.12", font=font(18), fill=(200, 120, 120))
progress_bar(draw, 150, cy+24, 700, 16, (35.70-20.12)/(37.73-20.12), (50, 160, 110))
mx = 150 + int(700 * (35.70-20.12)/(37.73-20.12))
draw.ellipse([mx-6, cy+21, mx+6, cy+43], fill=(100, 255, 160))
draw.text((870, cy+22), "$37.73", font=font(18), fill=(100, 200, 140))
cy += 50

# 애널리스트
draw.text((60, cy), "ANALYST TARGETS", font=font(20, True), fill=(80, 150, 255))
draw.line([(60, cy+28), (W-60, cy+28)], fill=(30, 60, 80))
cy += 38

targets = [("Citigroup", "$40", "Buy"), ("Mizuho", "$38", "Outperform"),
           ("RBC Capital", "$40", "Buy"), ("Stifel", "$40", "Buy"),
           ("Raymond James", "$40", "Buy")]
for i, (firm, tgt, rating) in enumerate(targets):
    x = 60 + (i % 3) * 320
    ry = cy + (i // 3) * 35
    draw.text((x, ry), f"{firm}: {tgt}", font=font(20), fill=(160, 180, 210))
    badge(draw, x + 200, ry-2, rating, (30, 90, 50))

cy += 85

# Thesis
draw.text((60, cy), "INVESTMENT THESIS", font=font(20, True), fill=(80, 150, 255))
cy += 30
thesis_lines = [
    "LNG 수출 16.7Bcf/day 확대 → 천연가스 압축 수요 구조적 증가",
    "Q4'25 EPS $0.69 (컨센서스 77% 상회), FY26 EBITDA $890M 가이던스",
    "85% 가동률 확보, 2027년까지 고객 계약 연장 완료",
    "배당 16% 인상 + 자사주 매입 완료 → 주주환원 강화",
]
for line in thesis_lines:
    draw.text((80, cy), f"  {line}", font=font(19), fill=(150, 180, 200))
    cy += 28

cy += 10
# Risks
draw.text((60, cy), "KEY RISKS", font=font(20, True), fill=(255, 130, 100))
cy += 30
risks = [
    "부채 $2.4B (레버리지 2.7x) — 금리 상승 시 리파이낸싱 리스크",
    "천연가스 가격 급락 시 고객사 투자 축소 가능",
    "FCF 대비 배당 커버리지 여유 부족",
]
for line in risks:
    draw.text((80, cy), f"  {line}", font=font(19), fill=(200, 140, 130))
    cy += 28

y += card_h + 20

# ═══ POSITION 2: HPSP ═══
card_h2 = 920
rbox(draw, 30, y, W-30, y+card_h2, r=20, fill=(10, 15, 35), outline=(120, 80, 200), width=2)

# 헤더
rbox(draw, 30, y, W-30, y+70, r=20, fill=(40, 25, 65))
draw.rectangle([30, y+50, W-30, y+70], fill=(40, 25, 65))

draw.text((60, y+18), "403870", font=font(36, True), fill=(180, 140, 255))
draw.text((240, y+25), "HPSP Co., Ltd.", font=font(28), fill=(210, 200, 240))
badge(draw, W-200, y+20, "STRONG BUY", (80, 40, 140))

cy = y + 85
draw.text((60, cy), "KOSDAQ | Semiconductor Equipment — High-Pressure Annealing", font=font(20), fill=(130, 120, 170))
cy += 35

# 가격 블록
rbox(draw, 60, cy, 340, cy+110, r=12, fill=(20, 15, 40))
draw.text((80, cy+10), "Entry Price", font=font(18), fill=(110, 100, 150))
draw.text((80, cy+35), "50,400", font=font(42, True), fill=(255, 255, 255))
draw.text((295, cy+55), "KRW", font=font(18), fill=(130, 120, 160))
draw.text((80, cy+82), "1,000 shares = $36,000", font=font(18), fill=(120, 110, 160))

rbox(draw, 360, cy, 540, cy+110, r=12, fill=(20, 20, 45))
draw.text((380, cy+10), "Target", font=font(18), fill=(110, 100, 150))
draw.text((380, cy+35), "70,000", font=font(34, True), fill=(140, 200, 255))
draw.text((380, cy+75), "+38.9%", font=font(22, True), fill=(100, 180, 230))

rbox(draw, 560, cy, 740, cy+110, r=12, fill=(40, 15, 25))
draw.text((580, cy+10), "Stop Loss", font=font(18), fill=(150, 90, 90))
draw.text((580, cy+35), "40,000", font=font(34, True), fill=(255, 120, 120))
draw.text((580, cy+75), "-20.6%", font=font(22, True), fill=(220, 90, 90))

rbox(draw, 760, cy, W-60, cy+110, r=12, fill=(20, 20, 35))
draw.text((780, cy+10), "Margin", font=font(18), fill=(110, 100, 150))
draw.text((780, cy+35), "51.8%", font=font(34, True), fill=(200, 180, 255))
draw.text((780, cy+75), "Op. Margin", font=font(18), fill=(130, 120, 160))

cy += 130

# 펀더멘탈
draw.text((60, cy), "FUNDAMENTALS", font=font(20, True), fill=(140, 120, 255))
draw.line([(60, cy+28), (W-60, cy+28)], fill=(40, 30, 70))
cy += 38

items2 = [
    ("Market Cap", "3.9T KRW", (200,190,240)),
    ("P/E (TTM)", "48.0x", (255,180,140)),
    ("Fwd P/E", "40.0x", (200,190,240)),
    ("EPS '24", "894 KRW", (200,190,240)),
    ("Rev '24", "181.4B", (140,200,255)),
    ("Rev '25E", "237B", (140,200,255)),
    ("Rev Growth", "+30%", (100,220,160)),
    ("Gross Mg.", "72%", (100,220,160)),
]

col = 0
row_y = cy
for label, val, vc in items2:
    x = 60 + col * 250
    draw.text((x, row_y), label, font=font(18), fill=(100, 100, 140))
    draw.text((x, row_y+22), val, font=font(24, True), fill=vc)
    col += 1
    if col >= 4:
        col = 0
        row_y += 55
cy = row_y + 55

# 52주 레인지
draw.text((60, cy), "52-Week Range", font=font(18), fill=(100, 100, 140))
draw.text((60, cy+22), "21,150", font=font(18), fill=(200, 120, 120))
progress_bar(draw, 170, cy+24, 680, 16, (50400-21150)/(53900-21150), (100, 70, 180))
mx2 = 170 + int(680 * (50400-21150)/(53900-21150))
draw.ellipse([mx2-6, cy+21, mx2+6, cy+43], fill=(180, 140, 255))
draw.text((870, cy+22), "53,900", font=font(18), fill=(140, 120, 220))
cy += 50

# 핵심 경쟁력
draw.text((60, cy), "COMPETITIVE MOAT", font=font(20, True), fill=(140, 120, 255))
draw.line([(60, cy+28), (W-60, cy+28)], fill=(40, 30, 70))
cy += 38

moats = [
    ("Monopoly", "글로벌 유일 양산급 HPA 장비 공급사"),
    ("Customers", "Samsung(3nm GAA), TSMC(2nm), Intel, SK Hynix"),
    ("IP Moat", "YEST 특허 소송 승소. 12-24개월 인증 장벽"),
    ("Balance", "순현금 170B KRW, 부채 거의 없음 (D/E 0.01)"),
    ("Pipeline", "HPO 신제품(GENI-SE) + imec CFET/3D 메모리 공동개발"),
]
for tag, desc in moats:
    bw = badge(draw, 80, cy, tag, (60, 40, 100))
    draw.text((80+bw+5, cy+4), desc, font=font(19), fill=(170, 160, 210))
    cy += 35

cy += 10

# Thesis
draw.text((60, cy), "INVESTMENT THESIS", font=font(20, True), fill=(140, 120, 255))
cy += 30
thesis2 = [
    "3nm GAA / 2nm 전환 → HPA 공정 필수화 (기존 열처리 대체 불가)",
    "HBM DRAM이 HPA 채택 시작 → 새로운 수요 축 확보",
    "HPO(고압산화) 신제품으로 TAM 확장 중",
    "순현금 170B, 무차입 → 반도체 경기 변동에 강한 체력",
    "5/14 FY2025 실적 발표 — 매출 +30% 성장 확인 예상",
]
for line in thesis2:
    draw.text((80, cy), f"  {line}", font=font(19), fill=(170, 160, 210))
    cy += 28

cy += 10
draw.text((60, cy), "KEY RISKS", font=font(20, True), fill=(255, 130, 100))
cy += 30
risks2 = [
    "삼성전자 편중 (매출 대부분) — 삼성 capex 감소 시 직격",
    "Crescendo 31% 잔여 지분 → 추가 블록딜 오버행",
    "P/E 48x 고밸류 — 실적 미스 시 급격한 디레이팅 리스크",
    "주문 타이밍 변동성 (분기별 매출 lumpiness 큼)",
]
for line in risks2:
    draw.text((80, cy), f"  {line}", font=font(19), fill=(200, 140, 130))
    cy += 28

y += card_h2 + 20

# ═══ STRATEGY & RULES ═══
rbox(draw, 30, y, W-30, y+350, r=20, fill=(12, 18, 35), outline=(80, 120, 180))
draw.text((60, y+15), "TRADING RULES & STRATEGY", font=font(24, True), fill=(80, 150, 255))
draw.line([(60, y+48), (W-60, y+48)], fill=(30, 60, 100))

rules = [
    ("1", "Position Sizing", "종목당 최대 50%, 현금 최소 10% 유지"),
    ("2", "Stop Loss", "진입가 대비 -15~20% 하회 시 전량 매도"),
    ("3", "Take Profit", "목표가 도달 시 50% 분할 매도, 나머지 트레일링 스탑"),
    ("4", "Rebalancing", "주 1회 가격 체크, 월 1회 포지션 재검토"),
    ("5", "New Entry", "Alpha Hunter 시그널 발생 시 현금으로 신규 진입"),
    ("6", "Risk Control", "포트폴리오 전체 -10% 시 전 포지션 50% 축소"),
    ("7", "Earnings", "실적 발표 전 포지션 축소 검토 (HPSP 5/14)"),
]

ry = y + 60
for num, title, desc in rules:
    rbox(draw, 60, ry, 95, ry+30, r=8, fill=(40, 70, 120))
    draw.text((68, ry+3), num, font=font(18, True), fill=(200, 220, 255))
    draw.text((110, ry+3), title, font=font(20, True), fill=(180, 200, 240))
    draw.text((110, ry+28), desc, font=font(18), fill=(120, 140, 170))
    ry += 42

y += 370

# ═══ RISK/REWARD MATRIX ═══
rbox(draw, 30, y, W-30, y+200, r=20, fill=(15, 15, 30), outline=(100, 80, 140))
draw.text((60, y+15), "RISK / REWARD MATRIX", font=font(24, True), fill=(180, 160, 255))
draw.line([(60, y+48), (W-60, y+48)], fill=(40, 30, 70))

# AROC
draw.text((60, y+65), "AROC", font=font(28, True), fill=(80, 200, 140))
draw.text((170, y+68), "Upside +9.2%  |  Downside -16.0%  |  R:R 0.58:1", font=font(22), fill=(150, 170, 200))
draw.text((170, y+95), "Conviction: HIGH — 밸류에이션 합리적, 모멘텀 강력, 배당 매력", font=font(18), fill=(120, 150, 170))

# HPSP
draw.text((60, y+130), "HPSP", font=font(28, True), fill=(160, 130, 255))
draw.text((170, y+133), "Upside +38.9%  |  Downside -20.6%  |  R:R 1.89:1", font=font(22), fill=(150, 170, 200))
draw.text((170, y+160), "Conviction: VERY HIGH — 독점 + 구조적 성장, 고밸류 감안해도 매력적", font=font(18), fill=(120, 150, 170))

y += 220

# ═══ FOOTER ═══
rbox(draw, 30, y, W-30, y+80, r=20, fill=(8, 12, 25), outline=(40, 50, 80))
ctext(draw, "ALPHA HUNTER  |  Powered by Claude Code AI  |  Virtual Portfolio", y+10, font(20, True), (80, 100, 140))
ctext(draw, "This is NOT financial advice. Virtual investment for research purposes only.", y+40, font(16), (60, 70, 100))

# 크롭
final_h = y + 100
img_cropped = img.crop((0, 0, W, final_h))
img_cropped.save(f"{OUT_DIR}/alpha_hunter_report.png", quality=95)
print(f"Report saved: {OUT_DIR}/alpha_hunter_report.png ({W}x{final_h})")
