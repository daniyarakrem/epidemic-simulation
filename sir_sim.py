# sir_sim.py (final polished version)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os

# ---------- parameters ----------
N = 10_000        # population
I0, R0 = 10, 0    # initial infected, recovered
S0 = N - I0 - R0
beta = 0.30       # infection rate per day
gamma = 0.08      # recovery rate per day
days = 180
dt = 0.25

# policy: reduce contact rate after this day
policy_day = 30
beta_policy = beta * 0.70   # 30% reduction

# ---------- helpers ----------
def fmt_thousands(x, _):
    return f"{int(x):,}"

def run_sir(beta_before, beta_after=None, policy_day=None):
    steps = int(days / dt)
    t = np.linspace(0, days, steps + 1)
    S = np.zeros(steps + 1); I = np.zeros(steps + 1); R = np.zeros(steps + 1)
    S[0], I[0], R[0] = S0, I0, R0

    for k in range(steps):
        tt = k * dt
        if policy_day is not None and beta_after is not None and tt >= policy_day:
            beta_t = beta_after
        else:
            beta_t = beta_before

        s, i, r = S[k], I[k], R[k]
        new_inf = beta_t * s * i / N
        new_rec = gamma * i

        S[k+1] = s - new_inf * dt
        I[k+1] = i + (new_inf - new_rec) * dt
        R[k+1] = r + new_rec * dt

    return t, S, I, R

# ---------- simulate ----------
t0, S_base, I_base, R_base = run_sir(beta_before=beta)
t1, S_pol,  I_pol,  R_pol  = run_sir(beta_before=beta, beta_after=beta_policy, policy_day=policy_day)

peak_I_base, peak_day_base = I_base.max(), t0[I_base.argmax()]
peak_I_pol,  peak_day_pol  = I_pol.max(),  t1[I_pol.argmax()]
attack_base = R_base[-1] / N
attack_pol  = R_pol[-1]  / N

# ---------- style ----------
plt.rcParams.update({
    "figure.dpi": 140,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "font.size": 12,
})

os.makedirs("figures", exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 5.6))

# shaded policy window
ax.axvspan(policy_day, days, color="0.9", zorder=0)

# baseline curves
ax.plot(t0, S_base, label="S (baseline)", lw=2, alpha=0.9)
ax.plot(t0, I_base, label="I (baseline)", lw=3, alpha=0.9)
ax.plot(t0, R_base, label="R (baseline)", lw=2, alpha=0.9)

# policy infected curve
ax.plot(t1, I_pol,  ls="--", lw=3.2, label=f"I (policy @ day {policy_day})")

# annotate peaks
ax.scatter([peak_day_base], [peak_I_base], s=30, zorder=5)
ax.annotate(
    f"Peak I (base): {int(peak_I_base):,}\nDay {peak_day_base:.1f}",
    xy=(peak_day_base, peak_I_base),
    xytext=(peak_day_base + 8, peak_I_base * 0.85),
    arrowprops=dict(arrowstyle="->", lw=1),
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.8")
)

ax.scatter([peak_day_pol], [peak_I_pol], s=30, zorder=5)
ax.annotate(
    f"Peak I (policy): {int(peak_I_pol):,}\nDay {peak_day_pol:.1f}",
    xy=(peak_day_pol, peak_I_pol),
    xytext=(peak_day_pol + 8, peak_I_pol * 0.85),
    arrowprops=dict(arrowstyle="->", lw=1),
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.8")
)

# labels & legend
ax.set_title("SIR Epidemic Simulation • Policy vs Baseline", pad=20, weight="bold")
ax.set_xlabel("Days")
ax.set_ylabel("People")
ax.yaxis.set_major_formatter(FuncFormatter(fmt_thousands))
ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False)

# move subtitle & metrics below the plot, aligned right
fig.text(
    0.99, -0.05,
    f"Population={N:,} • β={beta:.2f}, γ={gamma:.2f} • Policy: β→{beta_policy:.2f} at day {policy_day}",
    ha="right", va="top", fontsize=10, color="0.35"
)
fig.text(
    0.99, -0.10,
    f"Attack rate: baseline {attack_base:.1%}  |  policy {attack_pol:.1%}  "
    f"({(attack_base-attack_pol):.1%} absolute reduction)",
    ha="right", va="top", fontsize=10, color="0.35"
)

fig.tight_layout()

# save hi-res PNG + crisp SVG
fig.savefig("figures/policy_compare.png", dpi=300, bbox_inches="tight")
fig.savefig("figures/policy_compare.svg", bbox_inches="tight")
plt.show()

print(f"[Baseline]   Peak infected: {peak_I_base:,.0f} on day {peak_day_base:.1f}")
print(f"[With policy] Peak infected: {peak_I_pol:,.0f} on day {peak_day_pol:.1f}")
print(f"Attack rate baseline: {attack_base:.1%} | policy: {attack_pol:.1%}")
print("Saved figures → figures/policy_compare.png and .svg")
