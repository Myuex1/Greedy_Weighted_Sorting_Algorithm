# Summary

Sequences a list of items by attribute similarity to minimize transition cost between states. At each step the algorithm greedily selects the next item whose attributes are closest to the current one, reducing total accumulated difference across the full sequence.

Built to solve a real scheduling problem in a manufacturing environment, minimizing pump ramp time between production runs. The approach generalizes to any domain where order matters and transition cost is a function of how different two states are.

---

## How It Works
## How It Works

1. Define your items and their attributes (flow rate, density, etc.)
2. Assign weights to each attribute reflecting their real-world cost impact
3. The algorithm scores each candidate transition and picks the lowest cost
4. Tune weights using the Ratio of Ratios method (see below)

**Output:** An optimized sequence that minimizes total weighted transition cost

---

## How To Tune Weights

*This is a limited example to explain tuning.*

### Score Function

```
Score = (Flow Rate Differance * Weight) + (Density Difference * Weight)
```

Adapt to your system — this is just a simplified example.

### Example Transitions

|  | Transition 1 (A → B) | Transition 2 (C → D) |
|--|----------------------|----------------------|
| Flow Rate Diff | 15 lbs/min (Weight: 5) | 20 lbs/min (Weight: 5) |
| Density Diff | 0.2 LBS/ft² (Weight: 100) | 0.6 LBS/ft² (Weight: 100) |
| Real Waste | 50 ft³ | 100 ft³ |

---

## Tuning Walkthrough

### Round 1: Initial Calculation

```
Model Score 1 = (15 * 5) + (0.2 * 100) = 95     | Real Waste: 50 ft³
Model Score 2 = (20 * 5) + (0.6 * 100) = 160    | Real Waste: 100 ft³
```

**Ratio of Ratios:**

```
           (Model Ratio: 95 / 160)
Result  =  ----------------------  =  1.1875
           (Real Ratio:  50 / 100)
```

This is close to 1 but not quite. To get closer to 1, the bottom needs to be bigger.

---

### Round 2: Adjustment (Density Weight 100 → 200)

```
Model Score 1 = (15 * 5) + (0.2 * 200) = 115    | Real Waste: 50 ft³
Model Score 2 = (20 * 5) + (0.6 * 200) = 220    | Real Waste: 100 ft³
```

**Ratio of Ratios:**

```
           (115 / 220)
Result  =  ----------  =  1.045
           (50 / 100)
```

This is closer to 1, so we are moving in the right direction.

---

## Goal: Ratio of Ratios = 1

If this is close to 1 for a bunch of different combinations, the algorithm will correctly predict waste in reality, and be functional.
