#!/usr/bin/env python3
"""Alpha Hunter — 퇴직연금/개인연금 대시보드 (FinViz 스타일)"""

from PIL import Image, ImageDraw, ImageFont
import os, math, random

W, H = 1920, 2800
OUT = "/tmp/cokacdir-media/pension_dashboard.png"

def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumSquareR.ttf",
        "/usr/share/fonts/truetype/nanum/NanumSquareB.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumSquare.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def gradient(draw, c1, c2, y1=0, y2=H):
    for y in range(y1, y2):
        t = (y-y1) / max(1, y2-y1)
        r = int(c1[0]+(c2[0]-c1[0])*t)
        g = int(c1[1]+(c2[1]-c1[1])*t)
        b = int(c1[2]+(c2[2]-c1[2])*t)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

def rbox(draw, x1, y1, x2, y2, r=12, **kw):
    draw.rounded_rectangle([x1,y1,x2,y2], radius=r, **kw)

def ctext(draw, t, y, f, c, x=None):
    bb = draw.textbbox((0,0), t, font=f)
    tw = bb[2]-bb[0]
    if x is None:
        x = (W - tw) // 2
    draw.text((x, y), t, font=f, fill=c)
    return tw

def draw_sparkline(draw, x, y, w, h, data, color, fill_color=None):
    if not data or len(data) < 2:
        return
    mn, mx = min(data), max(data)
    rng = mx - mn if mx != mn else 1
    points = []
    for i, v in enumerate(data):
        px = x + int(i * w / (len(data)-1))
        py = y + h - int((v - mn) / rng * h)
        points.append((px, py))
    if fill_color:
        fill_pts = points + [(x+w, y+h), (x, y+h)]
        draw.polygon(fill_pts, fill=fill_color)
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=color, width=2)
    lx, ly = points[-1]
    draw.ellipse([lx-3, ly-3, lx+3, ly+3], fill=color)

def pct_color(pct):
    if pct > 5: return (30, 180, 80)
    if pct > 2: return (60, 160, 80)
    if pct > 0: return (80, 140, 80)
    if pct > -2: return (180, 80, 60)
    if pct > -5: return (200, 60, 50)
    return (220, 40, 40)

def pct_bg(pct):
    if pct > 5: return (20, 80, 40)
    if pct > 2: return (25, 70, 35)
    if pct > 0: return (30, 55, 30)
    if pct > -2: return (80, 30, 25)
    if pct > -5: return (90, 25, 20)
    return (100, 20, 15)


# ═══════════════════════════════════════
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)
gradient(draw, (12, 14, 22), (18, 20, 32))

# ═══ HEADER ═══
rbox(draw, 0, 0, W, 90, r=0, fill=(15, 18, 30))
draw.text((30, 15), "ALPHA HUNTER", font=font(40, True), fill=(60, 140, 255))
draw.text((350, 22), "Pension & Investment Dashboard", font=font(28), fill=(120, 140, 180))
draw.text((W-450, 15), "2026-04-21", font=font(24), fill=(100, 120, 160))
draw.text((W-450, 45), "퇴직연금 + 개인연금 + ETF 통합 뷰", font=font(20), fill=(80, 100, 140))

# 상단 지수 바
y = 100
rbox(draw, 20, y, W-20, y+70, r=12, fill=(18, 22, 38), outline=(40, 50, 70))

indices = [
    ("KOSPI", "3,180", "+0.85%", True),
    ("KOSDAQ", "1,042", "-1.23%", False),
    ("S&P 500", "5,528", "-0.42%", False),
    ("NASDAQ", "21,796", "+0.31%", True),
    ("Brent", "$105.4", "+3.24%", True),
    ("USD/KRW", "1,398", "-0.15%", False),
    ("10Y국채", "3.42%", "+0.05", True),
    ("VIX", "24.5", "-2.85%", False),
]

ix = 50
for name, val, chg, up in indices:
    draw.text((ix, y+10), name, font=font(16), fill=(100, 120, 150))
    draw.text((ix, y+30), val, font=font(22, True), fill=(220, 220, 240))
    c = (80, 200, 120) if up else (220, 80, 70)
    arrow = "▲" if up else "▼"
    draw.text((ix+100, y+32), f"{arrow}{chg}", font=font(18), fill=c)
    ix += 230

y = 190

# ═══ 섹터 히트맵 (FinViz 스타일) ═══
rbox(draw, 20, y, W-20, y+50, r=12, fill=(20, 25, 40))
draw.rectangle([20, y+35, W-20, y+50], fill=(20, 25, 40))
draw.text((40, y+10), "KOREAN MARKET SECTOR HEATMAP", font=font(24, True), fill=(100, 180, 255))

y += 60

# 대형 섹터 블록
sectors = [
    # (name, ticker, change%, width_ratio, height)
    ("삼성전자", "005930", +1.2, 0.20, 180),
    ("SK하이닉스", "000660", +3.5, 0.18, 180),
    ("현대차", "005380", -0.8, 0.12, 180),
    ("LG에너지솔루션", "373220", +2.1, 0.14, 180),
    ("NAVER", "035420", -1.5, 0.10, 180),
    ("카카오", "035720", -2.3, 0.08, 180),
    ("셀트리온", "068270", +0.5, 0.08, 180),
    ("KB금융", "105560", +1.8, 0.10, 180),

    # 2nd row
    ("POSCO홀딩스", "005490", -0.3, 0.14, 140),
    ("삼성SDI", "006400", +1.9, 0.12, 140),
    ("삼성바이오", "207940", +0.7, 0.12, 140),
    ("한화에어로", "012450", +5.2, 0.12, 140),
    ("HD현대중공업", "329180", +4.8, 0.10, 140),
    ("기아", "000270", -1.1, 0.10, 140),
    ("SK이노베이션", "096770", +2.4, 0.10, 140),
    ("LG화학", "051910", -0.6, 0.10, 140),
    ("KT&G", "033780", +0.3, 0.10, 140),

    # 3rd row
    ("삼성물산", "028260", +0.9, 0.10, 100),
    ("HPSP", "403870", +2.8, 0.10, 100),
    ("한미반도체", "042700", +6.1, 0.10, 100),
    ("리노공업", "058470", +3.2, 0.08, 100),
    ("에코프로비엠", "247540", -3.5, 0.08, 100),
    ("두산에너빌", "034020", +4.5, 0.08, 100),
    ("HD한국조선", "009540", +3.8, 0.08, 100),
    ("SK텔레콤", "017670", -0.2, 0.08, 100),
    ("삼성전기", "009150", +1.4, 0.08, 100),
    ("현대모비스", "012330", -0.9, 0.07, 100),
    ("LG전자", "066570", +0.6, 0.07, 100),
    ("한국전력", "015760", +1.1, 0.08, 100),
]

cx = 25
cy = y
row_max_h = 0
for name, ticker, chg, w_ratio, h in sectors:
    bw = int((W-50) * w_ratio)
    if cx + bw > W - 25:
        cx = 25
        cy += row_max_h + 5
        row_max_h = 0
    row_max_h = max(row_max_h, h)

    bg = pct_bg(chg)
    tc = pct_color(chg)
    rbox(draw, cx, cy, cx+bw-3, cy+h-3, r=6, fill=bg, outline=(bg[0]+20, bg[1]+20, bg[2]+20))

    # 종목명
    nf = font(min(20, max(14, bw//8)), True)
    draw.text((cx+8, cy+8), name, font=nf, fill=(230, 230, 240))

    # 변동률
    pf = font(min(28, max(16, bw//6)), True)
    sign = "+" if chg > 0 else ""
    draw.text((cx+8, cy+h//2-5), f"{sign}{chg}%", font=pf, fill=tc)

    # 티커 (작게)
    draw.text((cx+8, cy+h-22), ticker, font=font(12), fill=(100, 110, 130))

    cx += bw

y = cy + 110

# ═══ 포트폴리오 섹션들 ═══

# ─── 퇴직연금 (DC) ───
rbox(draw, 20, y, W//2-10, y+600, r=16, fill=(15, 20, 38), outline=(50, 80, 140))
draw.text((40, y+15), "퇴직연금 (DC형)", font=font(28, True), fill=(100, 180, 255))
draw.text((40, y+50), "평가금액: 3.80억 | 손익: +6,170만 (+19.37%)", font=font(22), fill=(180, 200, 230))

dc_etfs = [
    ("TIGER 반도체TOP10", "396500", 28, 37440, +22.08, [30,31,32,33,34,35,36,37,37]),
    ("KODEX 200미국채혼합", "267440", 19, 20877, +12.19, [18,19,19,20,20,20,21,21,21]),
    ("PLUS K방산", "447770", 11, 78000, +44.54, [54,58,62,66,70,74,76,78,78]),
    ("ACE KRX금현물", "411060", 9, 31550, +12.62, [28,29,29,30,30,31,31,32,32]),
    ("KODEX 200타겟커버드콜", "475180", 8, 19680, +6.29, [18,19,19,19,19,20,20,20,20]),
    ("RISE 삼성SK채권혼합50", "448290", 8, 11230, +1.67, [11,11,11,11,11,11,11,11,11]),
    ("SOL 조선TOP3플러스", "466920", 5, 37940, +44.06, [26,28,30,32,34,36,37,38,38]),
    ("KODEX 미국S&P500", "379800", 4, 23780, +25.59, [19,20,21,22,22,23,23,24,24]),
    ("기타(5종목)", "-", 8, None, 0, []),
]

ty = y + 85
for name, ticker, alloc, price, chg, spark in dc_etfs:
    rbox(draw, 40, ty, W//2-30, ty+70, r=10, fill=(20, 25, 42))

    draw.text((55, ty+8), name, font=font(18, True), fill=(200, 210, 230))
    draw.text((55, ty+35), ticker if ticker != "-" else "현금", font=font(14), fill=(90, 100, 130))

    # 비중
    rbox(draw, 400, ty+8, 460, ty+35, r=8, fill=(30, 50, 80))
    draw.text((410, ty+10), f"{alloc}%", font=font(16, True), fill=(140, 180, 255))

    # 현재가
    if price:
        draw.text((480, ty+8), f"{price:,}", font=font(18, True), fill=(200, 200, 220))
        c = (80, 200, 120) if chg > 0 else (220, 80, 70)
        s = "+" if chg > 0 else ""
        draw.text((480, ty+35), f"{s}{chg}%", font=font(16), fill=c)
    else:
        draw.text((480, ty+15), "안전자산", font=font(16), fill=(120, 140, 160))

    # 스파크라인
    if spark:
        sc = (60, 180, 100) if chg > 0 else (200, 80, 70)
        sf = (30, 80, 50, 40) if chg > 0 else (80, 30, 25, 40)
        draw_sparkline(draw, 620, ty+10, 280, 45, spark, sc)

    # 비중 바
    bar_w = int(300 * alloc / 100)
    rbox(draw, 55, ty+60, 55+300, ty+66, r=3, fill=(25, 30, 45))
    rbox(draw, 55, ty+60, 55+bar_w, ty+66, r=3, fill=(50, 100, 180))

    ty += 80

# 퇴직연금 파이
draw.text((40, ty+10), "Asset Mix", font=font(18, True), fill=(120, 150, 200))
colors_dc = [(50,120,200), (40,160,120), (60,100,180), (100,80,180), (80,100,60), (60,60,80), (200,140,60), (80,160,200), (50,50,70)]
cx_pie, cy_pie, r_pie = 200, ty+100, 70
start = 0
for i, (_, _, alloc, _, _, _) in enumerate(dc_etfs):
    extent = alloc / 100 * 360
    draw.pieslice([cx_pie-r_pie, cy_pie-r_pie, cx_pie+r_pie, cy_pie+r_pie],
                  start, start+extent, fill=colors_dc[i])
    start += extent

# 범례
lx = 310
ly = ty + 50
for i, (name, _, alloc, _, _, _) in enumerate(dc_etfs):
    draw.rectangle([lx, ly+2, lx+12, ly+14], fill=colors_dc[i])
    short = name[:10] + ".." if len(name) > 12 else name
    draw.text((lx+18, ly), f"{short} {alloc}%", font=font(14), fill=(160, 170, 190))
    ly += 22


# ─── 개인연금 (IRP) ───
rbox(draw, W//2+10, y, W-20, y+600, r=16, fill=(15, 20, 38), outline=(100, 60, 140))
draw.text((W//2+30, y+15), "개인연금 (IRP)", font=font(28, True), fill=(180, 140, 255))
draw.text((W//2+30, y+50), "평가금액: 1.57억 | 손익: +2,280만 (+16.99%)", font=font(22), fill=(200, 190, 230))

irp_etfs = [
    ("KODEX 200타겟커버드콜", "475180", 20, 19680, +5.38, [18,19,19,19,19,20,20,20,20]),
    ("RISE 네트워크인프라", "464240", 15, 45420, +7.63, [42,43,43,44,44,45,45,45,45]),
    ("KODEX 미국나스닥100", "379800", 14, 26050, +5.32, [24,25,25,25,26,26,26,26,26]),
    ("ACE 구글밸류체인", "480850", 14, 20965, +41.84, [15,16,17,18,19,20,20,21,21]),
    ("KODEX 미국AI인프라", "490050", 12, 23610, +41.88, [17,18,19,20,21,22,23,24,24]),
    ("ACE KRX금현물", "411060", 12, 31550, +23.88, [25,26,27,28,29,30,31,32,32]),
    ("KODEX 미국S&P500", "379800", 8, 23780, +26.34, [19,20,21,22,22,23,23,24,24]),
    ("PLUS K방산", "447770", 6, 78000, +2.17, [76,77,77,77,78,78,78,78,78]),
]

ty2 = y + 85
rx = W//2 + 10
for name, ticker, alloc, price, chg, spark in irp_etfs:
    rbox(draw, rx+20, ty2, W-40, ty2+70, r=10, fill=(25, 20, 42))

    draw.text((rx+35, ty2+8), name, font=font(18, True), fill=(210, 200, 240))
    draw.text((rx+35, ty2+35), ticker, font=font(14), fill=(100, 90, 130))

    rbox(draw, rx+380, ty2+8, rx+440, ty2+35, r=8, fill=(50, 30, 70))
    draw.text((rx+390, ty2+10), f"{alloc}%", font=font(16, True), fill=(180, 140, 255))

    draw.text((rx+460, ty2+8), f"{price:,}", font=font(18, True), fill=(200, 200, 220))
    c = (80, 200, 120) if chg > 0 else (220, 80, 70)
    s = "+" if chg > 0 else ""
    draw.text((rx+460, ty2+35), f"{s}{chg}%", font=font(16), fill=c)

    if spark:
        sc = (140, 100, 220) if chg > 0 else (200, 80, 70)
        draw_sparkline(draw, rx+600, ty2+10, 280, 45, spark, sc)

    bar_w2 = int(300 * alloc / 100)
    rbox(draw, rx+35, ty2+60, rx+35+300, ty2+66, r=3, fill=(30, 25, 45))
    rbox(draw, rx+35, ty2+60, rx+35+bar_w2, ty2+66, r=3, fill=(100, 60, 180))

    ty2 += 80

# IRP 파이
draw.text((rx+20, ty2+10), "Asset Mix", font=font(18, True), fill=(150, 120, 200))
colors_irp = [(100,60,200), (140,80,220), (80,120,200), (60,80,120), (50,60,80), (200,160,60), (80,160,200), (180,80,60)]
cx2, cy2 = rx + 180, ty2+100
start = 0
for i, (_, _, alloc, _, _, _) in enumerate(irp_etfs):
    extent = alloc / 100 * 360
    draw.pieslice([cx2-r_pie, cy2-r_pie, cx2+r_pie, cy2+r_pie],
                  start, start+extent, fill=colors_irp[i])
    start += extent

lx2 = rx + 290
ly2 = ty2 + 50
for i, (name, _, alloc, _, _, _) in enumerate(irp_etfs):
    draw.rectangle([lx2, ly2+2, lx2+12, ly2+14], fill=colors_irp[i])
    short = name[:12] + ".." if len(name) > 14 else name
    draw.text((lx2+18, ly2), f"{short} {alloc}%", font=font(14), fill=(170, 160, 200))
    ly2 += 22

y += 620

# ═══ Alpha Hunter ETF 포트폴리오 ═══
rbox(draw, 20, y, W-20, y+500, r=16, fill=(12, 18, 32), outline=(60, 120, 80))
draw.text((40, y+15), "ALPHA HUNTER ETF PORTFOLIO", font=font(28, True), fill=(80, 200, 140))
draw.text((40, y+50), "가상 투자 1억원 | Core-Satellite 전략", font=font(22), fill=(140, 180, 160))

etf_data = [
    ("VOO", "S&P 500", "Core", 10, 510.00, -4.4, "USD"),
    ("SOXX", "Semiconductor", "Core", 10, 339.00, +9.2, "USD"),
    ("SCHD", "US Dividend", "Core", 10, 30.51, +12.1, "USD"),
    ("TIGER반도체", "KR Semi TOP10", "Core", 10, 33210, +2.8, "KRW"),
    ("KODEX200", "KOSPI 200", "Core", 10, 81225, +0.9, "KRW"),
    ("XLE", "Energy SPDR", "Core", 10, 105.00, +37.9, "USD"),
    ("BOTZ", "Robotics & AI", "Satellite", 7, 38.00, +14.8, "USD"),
    ("GEV", "GE Vernova", "Satellite", 3.5, 320.00, +22.0, "USD"),
    ("CEG", "Constellation", "Satellite", 3.5, 240.00, +18.0, "USD"),
    ("TIGER2차전지", "Battery", "Satellite", 6, 23950, +13.2, "KRW"),
    ("CASH", "현금", "Reserve", 10, None, 0, "KRW"),
]

# 테이블 헤더
ty3 = y + 85
headers = ["Ticker", "Name", "Type", "Alloc", "Entry", "YTD", "Signal"]
hx_positions = [40, 180, 360, 480, 570, 750, 870]
for i, h in enumerate(headers):
    draw.text((hx_positions[i], ty3), h, font=font(16, True), fill=(100, 140, 170))
ty3 += 30
draw.line([(40, ty3), (W-40, ty3)], fill=(30, 50, 60))
ty3 += 5

for ticker, name, typ, alloc, price, ytd, curr in etf_data:
    # 행 배경
    bg_row = (15, 22, 38) if etf_data.index((ticker, name, typ, alloc, price, ytd, curr)) % 2 == 0 else (18, 25, 42)
    rbox(draw, 30, ty3, W-30, ty3+34, r=4, fill=bg_row)

    tc = (60, 180, 120) if typ == "Core" else (180, 140, 255) if typ == "Satellite" else (120, 120, 140)
    draw.text((hx_positions[0], ty3+6), ticker, font=font(18, True), fill=(220, 220, 240))
    draw.text((hx_positions[1], ty3+8), name, font=font(16), fill=(160, 170, 190))

    rbox(draw, hx_positions[2], ty3+4, hx_positions[2]+80, ty3+28, r=6, fill=(tc[0]//4, tc[1]//4, tc[2]//4))
    draw.text((hx_positions[2]+8, ty3+6), typ, font=font(14, True), fill=tc)

    draw.text((hx_positions[3], ty3+6), f"{alloc}%", font=font(17, True), fill=(180, 200, 220))

    if price:
        if curr == "USD":
            draw.text((hx_positions[4], ty3+6), f"${price:,.2f}", font=font(17), fill=(180, 190, 210))
        else:
            draw.text((hx_positions[4], ty3+6), f"{price:,.0f}", font=font(17), fill=(180, 190, 210))

    # YTD
    yc = (60, 200, 120) if ytd > 0 else (220, 80, 70) if ytd < 0 else (120, 120, 140)
    s = "+" if ytd > 0 else ""
    draw.text((hx_positions[5], ty3+6), f"{s}{ytd}%", font=font(17, True), fill=yc)

    # Signal bar
    bar_pct = min(max((ytd + 10) / 50, 0), 1)
    bx = hx_positions[6]
    rbox(draw, bx, ty3+10, bx+150, ty3+24, r=5, fill=(25, 30, 45))
    rbox(draw, bx, ty3+10, bx+int(150*bar_pct), ty3+24, r=5, fill=yc)

    ty3 += 36

y += 520

# ═══ 하단 전략 요약 ═══
rbox(draw, 20, y, W//2-10, y+250, r=16, fill=(15, 20, 35), outline=(80, 120, 180))
draw.text((40, y+15), "PENDING STRATEGY", font=font(24, True), fill=(100, 180, 255))
draw.text((40, y+50), "Trigger: 이란전쟁 휴전/종료 시그널", font=font(20), fill=(200, 180, 140))
draw.text((40, y+80), "Timeframe: 2-3주 내 (4월 중순~말)", font=font(20), fill=(180, 200, 220))
draw.text((40, y+110), "Action: 현금 → VOO/SOXX 추가 매수", font=font(20, True), fill=(80, 200, 140))
draw.text((40, y+140), "Risk: 트럼프 발언 신뢰도 낮음", font=font(20), fill=(220, 140, 120))
draw.text((40, y+175), "Watch: XLE 부분 익절 (전쟁 종료 시 에너지 조정)", font=font(18), fill=(180, 170, 200))
draw.text((40, y+210), "Event: HPSP 실적 5/14 | Fed 의장 교체 5월", font=font(18), fill=(160, 150, 180))

# 우측: 총 자산 요약
rbox(draw, W//2+10, y, W-20, y+250, r=16, fill=(15, 20, 35), outline=(100, 80, 160))
draw.text((W//2+30, y+15), "TOTAL ASSET OVERVIEW", font=font(24, True), fill=(180, 160, 255))

assets = [
    ("퇴직연금 (DC)", "380,199,575원 (+19.37%)", (100, 180, 255)),
    ("개인연금 (IRP)", "156,706,130원 (+16.99%)", (180, 140, 255)),
    ("합산 실제 자산", "536,905,705원 (+8,450만)", (255, 200, 80)),
    ("Alpha Hunter (가상)", "$100,000 + 1억원", (80, 200, 140)),
]

ay = y + 55
for label, amount, c in assets:
    draw.text((W//2+40, ay), label, font=font(20), fill=(150, 150, 180))
    draw.text((W//2+40, ay+28), amount, font=font(26, True), fill=c)
    ay += 60

# 워터마크
y += 270
ctext(draw, "ALPHA HUNTER  |  Pension & Investment Dashboard  |  Powered by Claude Code AI  |  Not Financial Advice", y+10, font(16), (50, 55, 70))

# 크롭
final_h = y + 40
img_cropped = img.crop((0, 0, W, final_h))
img_cropped.save(OUT, quality=95)
print(f"Dashboard saved: {OUT} ({W}x{final_h})")
