import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.patheffects as pe

fig, ax = plt.subplots(figsize=(13, 7))
ax.set_xlim(0, 13)
ax.set_ylim(0, 7)
ax.axis("off")
fig.patch.set_facecolor("white")

# ── palette ──────────────────────────────────────────────────────────────────
PINK   = "#E8446A"
LGRAY  = "#CCCCCC"
DGRAY  = "#333333"
BGRAY  = "#F5F5F5"
GREEN  = "#2ECC71"
RED    = "#E74C3C"
YELLOW = "#F39C12"
BLUE   = "#3498DB"

def arrow(ax, x0, y0, x1, y1, color=DGRAY, lw=1.8):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=lw, mutation_scale=14))

def rounded_box(ax, cx, cy, w, h, color, lw=1.5, ls="-", facecolor="white", alpha=1.0):
    box = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                         boxstyle="round,pad=0.08",
                         linewidth=lw, linestyle=ls,
                         edgecolor=color, facecolor=facecolor, alpha=alpha, zorder=3)
    ax.add_patch(box)

def label(ax, x, y, txt, size=9, bold=False, color=DGRAY, ha="center", va="center"):
    w = "bold" if bold else "normal"
    ax.text(x, y, txt, ha=ha, va=va, fontsize=size, fontweight=w, color=color, zorder=5)

# ── LEFT: inputs ──────────────────────────────────────────────────────────────
# SUSPICIOUS badge (output from detectingfraud)
rounded_box(ax, 1.7, 5.0, 2.6, 1.0, PINK, lw=2, facecolor="#FDEEF2")
label(ax, 1.7, 5.35, "⚠  SUSPICIOUS", size=9, bold=True, color=PINK)
label(ax, 1.7, 4.72, "from detectingfraud", size=7.5, color="#888")

# User icon (speech bubble)
rounded_box(ax, 1.7, 2.9, 2.6, 1.4, LGRAY, facecolor=BGRAY)
# person silhouette (simplified)
circle = plt.Circle((1.1, 3.25), 0.22, color=DGRAY, zorder=5)
ax.add_patch(circle)
body = FancyBboxPatch((0.88, 2.72), 0.44, 0.38, boxstyle="round,pad=0.02",
                      facecolor=DGRAY, zorder=5)
ax.add_patch(body)
label(ax, 2.05, 3.28, '"Was this you?"', size=8.5, color=DGRAY, ha="center")
label(ax, 2.05, 2.98, "Cardholder responds", size=7.5, color="#888", ha="center")

label(ax, 1.7, 1.9, "Inputs", size=8, bold=True, color=DGRAY)

# bracket
ax.plot([3.05, 3.25, 3.25, 3.05], [4.55, 4.55, 3.15, 3.15],
        color=DGRAY, lw=1.5, zorder=4)

# ── ARROW input → agent ───────────────────────────────────────────────────────
arrow(ax, 3.55, 3.85, 5.0, 3.85, color=DGRAY)

# ── CENTER: Agent ─────────────────────────────────────────────────────────────
# dashed pink box
agent_box = FancyBboxPatch((5.05, 2.9), 1.9, 1.9,
                           boxstyle="round,pad=0.1",
                           linewidth=2.2, linestyle="--",
                           edgecolor=PINK, facecolor="white", zorder=3)
ax.add_patch(agent_box)

# gear + magnifier icon (approximated with circles and a rect)
cx, cy = 6.0, 3.95
outer = plt.Circle((cx, cy), 0.42, color=PINK, zorder=6)
inner = plt.Circle((cx, cy), 0.22, color="white", zorder=7)
ax.add_patch(outer)
ax.add_patch(inner)
# magnifier handle
ax.plot([cx+0.3, cx+0.55], [cy-0.3, cy-0.55], color=PINK, lw=4, zorder=6,
        solid_capstyle="round")

label(ax, 6.0, 3.1, "Agent", size=9, bold=True, color=DGRAY)

# ── ARROW agent → skill ───────────────────────────────────────────────────────
arrow(ax, 7.0, 3.95, 8.3, 3.95, color=DGRAY)
arrow(ax, 8.3, 3.85, 7.0, 3.85, color=DGRAY)

# ── RIGHT: analyzecontext Skill box ──────────────────────────────────────────
rounded_box(ax, 9.3, 3.9, 2.0, 1.5, BLUE, lw=2.5, facecolor="#EBF5FB")
# headset / HITL icon
hx, hy = 9.3, 4.25
circle2 = plt.Circle((hx, hy+0.05), 0.25, color=BLUE, zorder=6)
ax.add_patch(circle2)
circle3 = plt.Circle((hx, hy+0.05), 0.12, color="white", zorder=7)
ax.add_patch(circle3)
ax.plot([hx-0.25, hx-0.35, hx-0.35], [hy+0.05, hy+0.05, hy-0.12],
        color=BLUE, lw=2.5, zorder=6)
ax.plot([hx+0.25, hx+0.35, hx+0.35], [hy+0.05, hy+0.05, hy-0.12],
        color=BLUE, lw=2.5, zorder=6)
label(ax, 9.3, 3.58, "analyzecontext", size=8.5, bold=True, color=BLUE)
label(ax, 9.3, 3.33, "Skill", size=8.5, bold=True, color=BLUE)

# ── ARROWS: skill → 3 outcomes ───────────────────────────────────────────────
arrow(ax, 10.35, 4.55, 11.1, 5.55, color=GREEN, lw=2)
arrow(ax, 10.35, 3.85, 11.1, 3.85, color=RED,   lw=2)
arrow(ax, 10.35, 3.15, 11.1, 2.15, color=YELLOW, lw=2)

# outcome boxes
def outcome_box(ax, cx, cy, title, sub, color, facecolor):
    rounded_box(ax, cx, cy, 2.2, 0.85, color, lw=2, facecolor=facecolor)
    label(ax, cx, cy+0.16, title, size=8.5, bold=True, color=color)
    label(ax, cx, cy-0.16, sub,   size=7.5, color="#555")

outcome_box(ax, 12.1, 5.55, "✓  Authorize",    "Planned / Emergency", GREEN,  "#EAFAF1")
outcome_box(ax, 12.1, 3.85, "✗  Block & Refund", "Unrecognized Fraud",  RED,    "#FDEDEC")
outcome_box(ax, 12.1, 2.15, "?  Ask Again",    "Needs Clarification", YELLOW, "#FEF9E7")

# ── TITLE ─────────────────────────────────────────────────────────────────────
label(ax, 6.5, 6.6, "Human-in-the-Loop: analyzecontext Skill",
      size=13, bold=True, color=DGRAY)
label(ax, 6.5, 6.15,
      "Triggered after a SUSPICIOUS verdict — asks the cardholder for context before taking action",
      size=8.5, color="#666")

plt.tight_layout(pad=0.3)
plt.savefig("draw/Analyzecontext_Skill.png", dpi=150, bbox_inches="tight",
            facecolor="white")
print("saved: draw/Analyzecontext_Skill.png")
