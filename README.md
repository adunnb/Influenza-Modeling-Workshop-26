# Neural ODE Influenza Forecaster

**2nd place, Challenge 1 — 2026 Modeling the Invisible Workshop (Team 3)**

This repository contains our forecasting model and results for Challenge 1 of the
[2026 Modeling the Invisible Workshop](https://sites.google.com/iu.edu/modelingtheinvisibleworkshop/home)
hosted at Indiana University.

---

## The Challenge

The competition target was weekly influenza hospitalizations per 100,000 people,
simulated from a hidden two-strain SIR model with waning cross-immunity and the
possibility of vaccination against strain 1. Teams received data in four rolling
releases and submitted 5-week-ahead forecasts of both hospitalizations and R(t)
after each release.

**Competition protocol:**

| Round | Training data | Forecast weeks |
|-------|---------------|----------------|
| 1     | Weeks 1–10    | 11–15          |
| 2     | Weeks 1–15    | 16–20          |
| 3     | Weeks 1–20    | 21–25          |
| 4     | Weeks 1–25    | 26–30          |

**Scoring:** `0.8 × RMSE_Hosp + 0.2 × RMSE_Rt`, summed across all four rounds.

The hidden model was revealed after the competition as a two-virus crossover model
based on: Zarnitsyna et al. (2018), *PLoS ONE* 13(6): e0199674.
[https://doi.org/10.1371/journal.pone.0199674](https://doi.org/10.1371/journal.pone.0199674)

---

## Our Approach

We used a **Neural ODE** to forecast the epidemic trajectory without fitting the
underlying mechanistic parameters. The model learns a latent 6-dimensional state
evolving as `dx/dt = f_θ(x, t)` where `f_θ` is a small MLP, trained using the
adjoint method via `torchdiffeq`. This sidesteps the non-identifiability problem
inherent in multi-strain SIR models when only aggregate hospitalization data is
available.

**Key design choices:**
- Latent state dimension 6 (matching the SIR compartment count as an inductive prior)
- Ensemble of models for uncertainty quantification
- R(t) estimated from the learned latent dynamics
- Full season re-training at each round using all available data

See the notebooks in order for the full walkthrough.

---

## Repository Structure

```
.
├── data/
│   ├── raw/                        # Reference and context data
│   │   ├── influenzaA2017.csv      # Historical influenza season (2017)
│   │   ├── influenzaA2018.csv      # Historical influenza season (2018)
│   │   └── SIRCrossover_sample1.csv  # Sample output from hidden model
│   └── releases/                   # Official competition data releases
│       ├── round-01.csv            # Weeks 1–15 (observed through round 1)
│       ├── round-02.csv            # Weeks 1–20
│       ├── round-03.csv            # Weeks 1–25
│       └── round-04.csv            # Weeks 1–30 (full season)
│
├── notebooks/
│   ├── 01_data.ipynb               # Data exploration and competition context
│   ├── 02_model.ipynb              # Neural ODE architecture, training, evaluation
│   └── 03_competition_workflow.ipynb  # Live submission interface (per-round)
│
├── predictions/                    # Our submitted forecasts (weeks + hosp + R0)
│   ├── round-01-submission.csv
│   ├── round-02-submission.csv
│   ├── round-03-submission.csv
│   └── round-04-submission.csv
│
├── results/
│   └── scores.md                   # RMSE scores per round and leaderboard result
│
├── requirements.txt
└── README.md
```

---

## Quickstart

```bash
git clone https://github.com/adunnb/Influenza-Modeling-Workshop-26.git
cd Influenza-Modeling-Workshop-26
pip install -r requirements.txt
```

Then run the notebooks in order:

1. `notebooks/01_data.ipynb` — understand the data structure and competition setup
2. `notebooks/02_model.ipynb` — train and evaluate the Neural ODE offline
3. `notebooks/03_competition_workflow.ipynb` — replay the live submission workflow

The data directory is pre-populated so all notebooks run without any additional downloads.

---

## Results

**Challenge 1 — 2nd place (Team 3)**

See [`results/scores.md`](results/scores.md) for per-round RMSE breakdowns.

Full competition leaderboards and team prediction plots are available on the
[official results page](https://sites.google.com/iu.edu/modelingtheinvisibleworkshop/the-challenge/challenges/challenge-results).

---

## Limitations

Retraining happens from scratch every round: four full ensembles, no
fine-tuning between rounds, because fine-tuning risked forgetting the
early-season trend once a new release contradicted it (see `02_model.ipynb`).
Everything ran on CPU; no notebook here uses a GPU. That made the offline
validation loop slow enough that we tuned hyperparameters mostly by hand
rather than through any systematic search.

The model also never saw anything beyond the current season. Round 1 trains
on 10 points and has to forecast 5 weeks out with no prior knowledge of what
an influenza season typically looks like. `influenzaA2017.csv` and
`influenzaA2018.csv` sit in `data/raw/` and get plotted in `01_data.ipynb`,
but neither ever touches training; they're there for comparison, not as
training data. Pretraining on, or otherwise conditioning the model on, public
CDC influenza surveillance data across more seasons would give it some sense
of epidemic shape before round 1 even starts, instead of asking it to learn
that from ten points.

---

## Dependencies

See `requirements.txt`. Key packages:

- `torch` — Neural ODE backbone
- `torchdiffeq` — ODE solvers and adjoint method
- `numpy`, `pandas` — data handling
- `matplotlib` — visualization

---

## Citation

If you use or build on this work, please cite the workshop:

> 2026 Modeling the Invisible Workshop, Indiana University.
> https://sites.google.com/iu.edu/modelingtheinvisibleworkshop/home

And the hidden model paper:

> Zarnitsyna VI, Bulusheva I, Handel A, Longini IM, Halloran ME, Antia R (2018).
> Intermediate levels of vaccination coverage may minimize seasonal influenza outbreaks.
> *PLoS ONE* 13(6): e0199674. https://doi.org/10.1371/journal.pone.0199674
