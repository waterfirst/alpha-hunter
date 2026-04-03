#!/usr/bin/env python3
"""Alpha Hunter 가상 투자 포트폴리오 현황판"""

from PIL import Image, ImageDraw, ImageFont
import os, json

WIDTH, HEIGHT = 1080, 1920
OUTPUT = "/home/ubuntu/.cokacdir/workspace/cp7jpheo/alpha_hunter/portfolio_status.png"

def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/nanum/NanumSquareB.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumSquare.ttf",
        "/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumSquareR.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_gradient(draw, c1, c2):
    for y in range(HEIGHT):
        r = int(c1[0] + (c2[0]-c1[0]) * y/HEIGHT)
        g = int(c1[1] + (c2[1]-c1[1]) * y/HEIGHT)
        b = int(c1[2] + (c2[2]-c1[2]) * y/HEIGHT)
        draw.line([(0,y),(WIDTH,y)], fill=(r,g,b))

def center_text(draw, text, y, font, fill):
    bbox = draw.textbbox((0,0), text, font=font)
    x = (WIDTH - (bbox[2]-bbox[0])) // 2
    draw.text((x, y), text, font=font, fill=fill)

def draw_bar(draw, x, y, w, h, pct, color_fg, color_bg=(50,50,70)):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=h//2, fill=color_bg)
    fill_w = max(h, int(w * min(pct, 1.0)))
    draw.rounded_rectangle([x, y, x+fill_w, y+h], radius=h//2, fill=color_fg)

img = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)
draw_gradient(draw, (10, 15, 30), (20, 25, 50))

# ─── 헤더 ───
draw.rounded_rectangle([40, 40, WIDTH-40, 200], radius=20, fill=(20, 30, 55), outline=(60, 100, 180))
center_text(draw, "ALPHA HUNTER", 55, get_font(52, True), (100, 180, 255))
center_text(draw, "Virtual Investment Portfolio", 120, get_font(30), (120, 150, 200))
center_text(draw, "2026-04-02 | Day 1", 158, get_font(24), (100, 130, 170))

# ─── 총 자산 요약 ───
draw.rounded_rectangle([40, 230, WIDTH-40, 420], radius=20, fill=(15, 25, 50), outline=(50, 80, 140))

draw.text((80, 250), "Total Portfolio", font=get_font(26), fill=(100, 140, 190))

# USD
draw.text((80, 290), "USD", font=get_font(22, True), fill=(80, 120, 160))
draw.text((80, 320), "$100,000.00", font=get_font(40, True), fill=(100, 220, 160))
draw.text((420, 335), "invested: $49,980 | cash: $50,020", font=get_font(22), fill=(100, 140, 170))

# KRW
draw.text((80, 370), "KRW", font=get_font(22, True), fill=(80, 120, 160))
draw.text((80, 395), "", font=get_font(20), fill=(100, 140, 170))
# We show KRW part
draw.text((150, 370), "140,000,000원", font=get_font(28, True), fill=(100, 220, 160))
draw.text((500, 375), "invested: 50,400,000 | cash: 89,600,000", font=get_font(18), fill=(100, 140, 170))

# ─── AROC 카드 ───
y = 450
draw.rounded_rectangle([40, y, WIDTH-40, y+480], radius=20, fill=(15, 30, 55), outline=(60, 140, 100))

# 종목명
draw.rounded_rectangle([70, y+20, 200, y+65], radius=12, fill=(40, 100, 70))
draw.text((85, y+25), "AROC", font=get_font(28, True), fill=(200, 255, 200))
draw.text((220, y+28), "Archrock Inc.", font=get_font(26, True), fill=(200, 230, 200))
draw.text((220, y+60), "NYSE | Energy / Midstream Gas Compression", font=get_font(20), fill=(100, 150, 130))

# 가격 정보
draw.text((70, y+100), "Entry Price", font=get_font(22), fill=(120, 150, 170))
draw.text((70, y+130), "$35.70", font=get_font(44, True), fill=(255, 255, 255))

draw.text((350, y+100), "Target", font=get_font(22), fill=(120, 150, 170))
draw.text((350, y+130), "$39.00", font=get_font(36, True), fill=(100, 220, 160))
draw.text((540, y+140), "(+9.2%)", font=get_font(24), fill=(100, 220, 160))

draw.text((700, y+100), "Stop Loss", font=get_font(22), fill=(120, 150, 170))
draw.text((700, y+130), "$30.00", font=get_font(36, True), fill=(255, 100, 100))
draw.text((880, y+140), "(-16.0%)", font=get_font(24), fill=(255, 100, 100))

# 포지션
draw.line([(70, y+190), (WIDTH-70, y+190)], fill=(40, 70, 60), width=1)
draw.text((70, y+205), "Shares: 1,400주", font=get_font(26, True), fill=(200, 220, 240))
draw.text((400, y+205), "Invested: $49,980", font=get_font(26, True), fill=(200, 220, 240))

# 52주 범위
draw.text((70, y+260), "52-Week Range", font=get_font(22), fill=(120, 150, 170))
draw.text((70, y+290), "$20.12", font=get_font(20), fill=(255, 150, 150))
draw_bar(draw, 170, y+293, 650, 18, (35.70-20.12)/(37.73-20.12), (60, 160, 120), (30, 50, 45))
# 현재가 마커
marker_x = 170 + int(650 * (35.70-20.12)/(37.73-20.12))
draw.ellipse([marker_x-8, y+289, marker_x+8, y+315], fill=(100, 255, 160))
draw.text((840, y+290), "$37.73", font=get_font(20), fill=(100, 220, 160))

# 애널리스트
draw.text((70, y+330), "Analyst Consensus", font=get_font(22), fill=(120, 150, 170))
draw.rounded_rectangle([70, y+360, 250, y+400], radius=12, fill=(30, 100, 60))
draw.text((85, y+365), "STRONG BUY", font=get_font(24, True), fill=(100, 255, 130))
draw.text((270, y+368), "8 Buy / 0 Hold / 0 Sell", font=get_font(22), fill=(150, 180, 170))

# 투자 근거
draw.text((70, y+420), "Thesis:", font=get_font(22, True), fill=(140, 170, 200))
draw.text((70, y+448), "천연가스 압축 인프라 핵심. 미드스트림 에너지 수요 증가 수혜", font=get_font(20), fill=(120, 150, 180))

# ─── HPSP 카드 ───
y2 = y + 510
draw.rounded_rectangle([40, y2, WIDTH-40, y2+480], radius=20, fill=(15, 25, 50), outline=(100, 80, 160))

# 종목명
draw.rounded_rectangle([70, y2+20, 240, y2+65], radius=12, fill=(80, 50, 120))
draw.text((85, y2+25), "403870", font=get_font(28, True), fill=(220, 200, 255))
draw.text((260, y2+28), "HPSP Co., Ltd.", font=get_font(26, True), fill=(220, 200, 240))
draw.text((260, y2+60), "KOSDAQ | Semiconductor Equipment", font=get_font(20), fill=(140, 120, 170))

# 가격 정보
draw.text((70, y2+100), "Entry Price", font=get_font(22), fill=(120, 150, 170))
draw.text((70, y2+130), "50,400", font=get_font(44, True), fill=(255, 255, 255))
draw.text((310, y2+150), "KRW", font=get_font(22), fill=(150, 150, 170))

draw.text((400, y2+100), "Target", font=get_font(22), fill=(120, 150, 170))
draw.text((400, y2+130), "70,000", font=get_font(36, True), fill=(100, 220, 160))
draw.text((590, y2+140), "(+38.9%)", font=get_font(24), fill=(100, 220, 160))

draw.text((730, y2+100), "Stop Loss", font=get_font(22), fill=(120, 150, 170))
draw.text((730, y2+130), "40,000", font=get_font(36, True), fill=(255, 100, 100))
draw.text((910, y2+140), "(-20.6%)", font=get_font(24), fill=(255, 100, 100))

# 포지션
draw.line([(70, y2+190), (WIDTH-70, y2+190)], fill=(50, 40, 70), width=1)
draw.text((70, y2+205), "Shares: 1,000주", font=get_font(26, True), fill=(200, 220, 240))
draw.text((400, y2+205), "Invested: 50,400,000원", font=get_font(26, True), fill=(200, 220, 240))

# 52주 범위
draw.text((70, y2+260), "52-Week Range", font=get_font(22), fill=(120, 150, 170))
draw.text((70, y2+290), "28,000", font=get_font(20), fill=(255, 150, 150))
draw_bar(draw, 190, y2+293, 620, 18, (50400-28000)/(55000-28000), (100, 80, 180), (35, 30, 55))
marker_x2 = 190 + int(620 * (50400-28000)/(55000-28000))
draw.ellipse([marker_x2-8, y2+289, marker_x2+8, y2+315], fill=(180, 140, 255))
draw.text((830, y2+290), "55,000", font=get_font(20), fill=(100, 180, 255))

# 1년 수익률
draw.text((70, y2+330), "1Y Performance", font=get_font(22), fill=(120, 150, 170))
draw.rounded_rectangle([70, y2+360, 220, y2+400], radius=12, fill=(30, 80, 50))
draw.text((85, y2+365), "+79.04%", font=get_font(24, True), fill=(100, 255, 130))
draw.text((240, y2+368), "반도체 고압 수소 어닐링 장비 독점", font=get_font(22), fill=(150, 140, 180))

# 투자 근거
draw.text((70, y2+420), "Thesis:", font=get_font(22, True), fill=(140, 170, 200))
draw.text((70, y2+448), "HBM/첨단패키징 수요 폭증 → 고압 어닐링 장비 독점 수혜", font=get_font(20), fill=(120, 150, 180))

# ─── 하단 Risk/Reward ───
y3 = y2 + 510
draw.rounded_rectangle([40, y3, WIDTH-40, y3+180], radius=20, fill=(20, 20, 40), outline=(80, 80, 120))

center_text(draw, "Risk / Reward Summary", y3+15, get_font(26, True), (180, 180, 220))

# AROC
draw.text((70, y3+55), "AROC", font=get_font(24, True), fill=(100, 200, 140))
draw.text((180, y3+55), "Upside +9.2%  |  Downside -16.0%  |  R:R = 1:1.7", font=get_font(22), fill=(160, 170, 200))

# HPSP
draw.text((70, y3+95), "HPSP", font=get_font(24, True), fill=(160, 140, 255))
draw.text((180, y3+95), "Upside +38.9%  |  Downside -20.6%  |  R:R = 1.9:1", font=get_font(22), fill=(160, 170, 200))

# 전략 메모
draw.line([(70, y3+130), (WIDTH-70, y3+130)], fill=(50, 50, 80), width=1)
draw.text((70, y3+140), "Strategy: 주간 리밸런싱 체크. 목표가 도달 시 50% 분할 매도", font=get_font(22), fill=(130, 140, 170))

# 워터마크
center_text(draw, "ALPHA HUNTER — Virtual Portfolio — Not Financial Advice", HEIGHT-50, get_font(18), (60, 70, 90))

img.save(OUTPUT, quality=95)
print(f"Portfolio card saved: {OUTPUT}")
