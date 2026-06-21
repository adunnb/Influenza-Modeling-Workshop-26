# Challenge 1 Results — Team 3

**Final standing: 2nd place**

Competition: [2026 Modeling the Invisible Workshop, Challenge 1](https://sites.google.com/iu.edu/modelingtheinvisibleworkshop/the-challenge/challenges/challenge-results)

---

## Scoring formula

Each round is scored as:

```
round_score = 0.8 × hosp_nrmse + 0.2 × r0_rmse
```

The challenge score is the average of `round_score` across all four rounds.

---

## Per-round scores

| Round | Training weeks | Forecast weeks | hosp_rmse | hosp_nrmse | r0_rmse  | round_score |
|-------|-----------------|------------------|-----------|------------|----------|-------------|
| 1     | 1–10            | 11–15            | 0.400000  | 0.206186   | 0.047958 | 0.174540    |
| 2     | 1–15            | 16–20            | 1.407835  | 0.368543   | 0.137113 | 0.322257    |
| 3     | 1–20            | 21–25            | 4.064234  | 1.092536   | 0.329727 | 0.939974    |
| 4     | 1–25            | 26–30            | 0.044721  | 0.072131   | 0.522494 | 0.162204    |
| **Total (avg)** |       |                  |           |            |          | **0.399744**|

---

## Final leaderboard — Challenge 1

| Rank | Team    | Challenge score |
|------|---------|------------------|
| 1    | Team-05 | 0.386849         |
| 2    | **Team-03** | **0.399744** |
| 3    | Team-07 | 0.460731         |
| 4    | Team-09 | 0.497027         |
| 5    | Team-02 | 0.515890         |
| 6    | Team-01 | 0.526690         |
| 7    | Team-08 | 0.637971         |
| 8    | Team-06 | 0.730898         |

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
