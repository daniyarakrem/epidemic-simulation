<p align="center">
  <a href="https://raw.githubusercontent.com/daniyarakrem/epidemic-simulation/main/assets/preview.png">
    <img src="https://raw.githubusercontent.com/daniyarakrem/epidemic-simulation/main/assets/preview.png" 
         alt="Epidemic Simulation – SIR & Agent-Based Models" width="820">
  </a>
</p>

# Epidemic Simulation (SIR + Agent-Based)

Simulates epidemic spread with a classic **SIR model** (Euler method) and a simple **agent-based grid**.  
Includes a policy toggle that reduces contact rate mid-simulation and compares outcomes.

---

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt    # or: pip install numpy matplotlib
python3 sir_sim.py                 # saves figures/policy_compare.png
# optional:
python3 abm_grid.py                 # saves figures/abm_counts.png
