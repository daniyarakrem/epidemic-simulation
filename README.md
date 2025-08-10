# Epidemic Simulation (SIR + Agent-Based Modeling)

Simulates epidemic spread using:
- **SIR model** (Euler method) for deterministic dynamics
- **Agent-based model** for spatial, individual-level interactions

Includes a **policy intervention toggle** to reduce contact rate after a certain day, with visual comparisons of outcomes.

---

## Example Outputs

### SIR Model — Policy vs. Baseline

**Key Results (Example Run):**
- **Baseline peak infected:** 3,847 (Day 37.2)
- **Policy peak infected:** 3,190 (Day 36.2)
- **Attack rate:** Baseline 97.5% → Policy 92.7% (4.8% absolute reduction)

---

### Agent-Based Model — Counts Over Time

---

##  Methods

### SIR Model
- Uses Euler integration to solve the classic **Susceptible–Infected–Recovered** equations:
