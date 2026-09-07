# Figure 7 — Trajectoire

**Statut :** `PROPOSED`  
**Message :** une trajectoire est une suite d'états fenêtrés, pas une courbe lissée.

```mermaid
flowchart LR
  S1["CS(w1)<br/>attention estimated<br/>WM refused"] --> S2["CS(w2)<br/>attention estimated<br/>fatigue high"]
  S2 --> S3["CS(w3)<br/>Refusal WINDOW<br/>undefined"]
  S3 --> S4["CS(w4)<br/>attention estimated<br/>context workday"]
```

```
capacity κ  ────────────────────────────────────────────  (lent)

state        ■■■■        ■■■■              ■■■■
window       w1          w2       (trou)   w4
refus              possible à chaque coupe
```

Pas d'interpolation du trou. Le trou est un résultat.
