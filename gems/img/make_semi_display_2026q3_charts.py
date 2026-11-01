"""Charts for semiconductor_vs_display_analyst_report_2026q3.qmd.

Every number below is copied from the report body (IR / company releases /
broker report as labelled there). Nothing is estimated here.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Patch

OUT = Path(__file__).resolve().parent
FONT = "/usr/share/fonts/truetype/nanum/NanumSquare_acR.ttf"
font_manager.fontManager.addfont(FONT)
plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT).get_name()
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

NAVY = "#1F3A5F"
TEAL = "#2A9D8F"
ORANGE = "#E76F51"
GREY = "#8D99AE"
LIGHT = "#E9ECEF"


def save(fig, name):
    fig.savefig(OUT / name, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# 1. SDC 7 quarters: revenue / operating profit bars + 2026 margin line
quarters = ["25.1Q", "25.2Q", "25.3Q", "25.4Q", "26.1Q", "26.2Q", "26.3Q"]
revenue = [5.9, 6.4, 8.1, 9.5, 6.7, 7.5, 8.0]
op = [0.5, 0.5, 1.2, 2.0, 0.4, 0.7, 1.1]
margin = [None, None, None, None, 5, 9, 14]

fig, ax = plt.subplots(figsize=(9, 4.8))
x = range(len(quarters))
w = 0.38
b1 = ax.bar([i - w / 2 for i in x], revenue, w, color=LIGHT, edgecolor=GREY, label="매출")
b2 = ax.bar([i + w / 2 for i in x], op, w, color=NAVY, label="영업이익")
for bar, v in zip(b1, revenue):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 0.15, f"{v:.1f}", ha="center", fontsize=9, color="#495057")
for bar, v in zip(b2, op):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 0.15, f"{v:.1f}", ha="center", fontsize=9, color=NAVY, fontweight="bold")
tick_labels = [
    f"{q}\n이익률 {m}%" if m is not None else q for q, m in zip(quarters, margin)
]
ax.set_xticks(list(x))
ax.set_xticklabels(tick_labels, fontsize=9)
for label, m in zip(ax.get_xticklabels(), margin):
    if m is not None:
        label.set_color(ORANGE)
        label.set_fontweight("bold")
ax.set_ylabel("조 원")
ax.set_ylim(0, 11.5)
ax.axvspan(3.5, 6.5, color=TEAL, alpha=0.07)
ax.text(5, 10.9, "2026년: 1Q 저점 이후 회복", ha="center", fontsize=10, color=TEAL)
ax.legend(loc="upper left", frameon=False, fontsize=9)
ax.set_title("삼성디스플레이(SDC) 분기 매출·영업이익 추이", loc="left", fontsize=13, fontweight="bold")
fig.text(0.01, -0.02, "출처: 삼성전자 IR 경영설명회 자료 (SDC 페이지). 영업이익률은 2026년 분기만 IR 공식 수치.", fontsize=8, color=GREY)
save(fig, "semi_display_01_sdc_trend.png")

# 2. 2026 3Q operating profit scale (조 원) - linear, labelled multiple
labels = ["삼성전자 DS\n(반도체)", "SK하이닉스", "삼성디스플레이\n(SDC)"]
values = [106.5, 83.3, 1.1]
colors = [NAVY, NAVY, ORANGE]
fig, ax = plt.subplots(figsize=(9, 4.2))
bars = ax.barh(labels[::-1], values[::-1], color=colors[::-1], height=0.55)
for bar, v in zip(bars, values[::-1]):
    ax.text(v + 1.5, bar.get_y() + bar.get_height() / 2, f"{v:.1f}조 원", va="center", fontsize=11, fontweight="bold")
ax.text(22, 0, "삼성전자 DS 영업이익의 약 1/97", va="center", fontsize=10, color=GREY)
ax.set_xlim(0, 125)
ax.set_xlabel("2026년 3분기 영업이익 (조 원)")
ax.set_title("2026년 3분기 영업이익 규모 비교", loc="left", fontsize=13, fontweight="bold")
fig.text(0.01, -0.03, "출처: 삼성전자·SK하이닉스 공식 보도자료 (삼성전자 DS 부문 · SK하이닉스 연결). SDC는 IR 경영설명회 자료.", fontsize=8, color=GREY)
save(fig, "semi_display_02_q3_scale.png")

# 3. 2026 3Q operating margin: SDC vs SK하이닉스 (company-stated)
fig, ax = plt.subplots(figsize=(7.5, 4.2))
names = ["SDC\n(IR 공식)", "SK하이닉스\n(회사 표기)"]
margins = [14, 80]
bars = ax.bar(names, margins, color=[ORANGE, NAVY], width=0.5)
for bar, v in zip(bars, margins):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 2, f"{v}%", ha="center", fontsize=13, fontweight="bold")
ax.set_ylim(0, 95)
ax.set_ylabel("영업이익률 (%)")
ax.text(1, 45, "영업이익÷매출\n= 79.7%", ha="center", fontsize=9, color="white")
ax.set_title("2026년 3분기 영업이익률", loc="left", fontsize=13, fontweight="bold")
fig.text(0.01, -0.03, "삼성전자 DS 영업이익률은 발표문에 없어 제외. SK하이닉스는 회사 표기 80%를 그대로 씀.", fontsize=8, color=GREY)
save(fig, "semi_display_03_q3_margin.png")

# 4. Source-status matrix: which value is verified how
status_color = {
    "IR 검증": TEAL,
    "회사 발표": NAVY,
    "증권사 리포트": "#E9C46A",
    "미확인": "#DEE2E6",
}
rows = [
    "3분기 매출",
    "3분기 영업이익",
    "전년 동기 대비 영업이익",
    "영업이익률",
    "목표주가 변화",
]
cols = ["SDC", "LG디스플레이", "삼성전자 DS", "SK하이닉스"]
grid = [
    ["IR 검증", "미확인", "회사 발표", "회사 발표"],
    ["IR 검증", "증권사 리포트", "회사 발표", "회사 발표"],
    ["IR 검증", "증권사 리포트", "미확인", "회사 발표"],
    ["IR 검증", "미확인", "미확인", "회사 발표"],
    ["미확인", "증권사 리포트", "미확인", "미확인"],
]
fig, ax = plt.subplots(figsize=(9.5, 4.6))
for r, row in enumerate(grid):
    for c, s in enumerate(row):
        ax.add_patch(plt.Rectangle((c, len(rows) - 1 - r), 0.94, 0.88, color=status_color[s]))
        txt_color = "white" if s in ("IR 검증", "회사 발표") else "#212529"
        ax.text(c + 0.47, len(rows) - 1 - r + 0.44, s, ha="center", va="center", fontsize=10, color=txt_color)
ax.set_xlim(0, len(cols))
ax.set_ylim(0, len(rows))
ax.set_xticks([c + 0.47 for c in range(len(cols))])
ax.set_xticklabels(cols, fontsize=11, fontweight="bold")
ax.set_yticks([len(rows) - 1 - r + 0.44 for r in range(len(rows))])
ax.set_yticklabels(rows, fontsize=10)
ax.tick_params(length=0)
for side in ("top", "right", "bottom", "left"):
    ax.spines[side].set_visible(False)
ax.xaxis.tick_top()
legend = [Patch(color=v, label=k) for k, v in status_color.items()]
ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=4, frameon=False, fontsize=9)
ax.set_title("값마다 출처가 다르다: 확인 상태 한눈에 보기", loc="left", fontsize=13, fontweight="bold", pad=34)
save(fig, "semi_display_04_source_status.png")

print("wrote 4 charts to", OUT)
