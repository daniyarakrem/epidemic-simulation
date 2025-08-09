import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# states: 0=Susceptible, 1=Infected, 2=Recovered
np.random.seed(0)
N = 120                    # grid N x N
p_init_inf = 0.003         # initial infected fraction
beta = 0.35                # infection prob per infected neighbor per step
gamma = 0.02               # recovery prob per step
steps = 300

grid = np.zeros((N, N), dtype=np.uint8)
grid[np.random.rand(N, N) < p_init_inf] = 1

def infected_neighbors(g):
    up    = np.roll(g, -1, axis=0)
    down  = np.roll(g,  1, axis=0)
    left  = np.roll(g,  1, axis=1)
    right = np.roll(g, -1, axis=1)
    return (up==1) + (down==1) + (left==1) + (right==1)

fig, ax = plt.subplots(figsize=(6,6))
im = ax.imshow(grid, vmin=0, vmax=2, interpolation="nearest")
ax.set_title("ABM Epidemic (0=S,1=I,2=R)")
ax.axis("off")

counts_S, counts_I, counts_R = [], [], []

def step(_):
    global grid, beta
    inf_nbrs = infected_neighbors(grid)

    # simple policy: after 100 steps, reduce beta by 30%
    if len(counts_I) == 100:
        beta *= 0.7

    s_mask = (grid == 0)
    p_inf = 1 - (1 - beta) ** inf_nbrs
    new_I = (np.random.rand(N, N) < p_inf) & s_mask

    i_mask = (grid == 1)
    new_R = (np.random.rand(N, N) < gamma) & i_mask

    grid[new_I] = 1
    grid[new_R] = 2

    im.set_data(grid)
    S = np.sum(grid == 0); I = np.sum(grid == 1); R = np.sum(grid == 2)
    counts_S.append(S); counts_I.append(I); counts_R.append(R)
    return [im]

ani = FuncAnimation(fig, step, frames=steps, interval=50, blit=True)
plt.show()

# save counts plot
os.makedirs("figures", exist_ok=True)
plt.figure()
plt.plot(counts_S, label="S")
plt.plot(counts_I, label="I")
plt.plot(counts_R, label="R")
plt.title("ABM Counts Over Time"); plt.xlabel("Step"); plt.ylabel("Agents")
plt.legend(); plt.tight_layout()
plt.savefig("figures/abm_counts.png", dpi=200)
plt.show()
print('Saved plot -> figures/abm_counts.png')
