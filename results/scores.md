# Challenge 1 Results — Team 3

**Final standing: 2nd place**

Competition: [2026 Modeling the Invisible Workshop, Challenge 1](https://sites.google.com/iu.edu/modelingtheinvisibleworkshop/the-challenge/challenges/challenge-results)

---

## Scoring formula

Each round is scored as:

```
score_round = 0.8 × RMSE_Hosp + 0.2 × RMSE_Rt
```

The final leaderboard score is the sum of `score_round` across all four rounds.

---

## Per-round scores

| Round | Training weeks | Forecast weeks | RMSE_Hosp | RMSE_Rt | Round score |
|-------|---------------|----------------|-----------|---------|-------------|
| 1     | 1–10          | 11–15          |           |         |             |
| 2     | 1–15          | 16–20          |           |         |             |
| 3     | 1–20          | 21–25          |           |         |             |
| 4     | 1–25          | 26–30          |           |         |             |
| **Total** |           |                |           |         |             |

*Fill in per-round scores from the official results page.*

---

## Notes

- **Round 1** was the hardest: only 10 weeks of training data, during the early
  exponential growth phase, with no indication yet whether the season would be
  unimodal or bimodal.
- **Round 3** data revealed the second peak, which significantly helped the Neural
  ODE learn the two-strain dynamics implicitly.
- R(t) estimation was derived from the latent state trajectory rather than fit
  directly, which contributed to the RMSE_Rt component.

---

## Official leaderboard

Full leaderboard images (all teams) are on the
[competition results page](https://sites.google.com/iu.edu/modelingtheinvisibleworkshop/the-challenge/challenges/challenge-results).

The hidden model was a two-virus SIR with crossover immunity, based on
Zarnitsyna et al. (2018), *PLoS ONE* 13(6): e0199674.
