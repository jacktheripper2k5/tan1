# Blast Furnace Oxygen Balance

A yellow-themed Streamlit interface implementing Chapter 1, Problem 1.7
from J. G. Peacey and W. G. Davenport, *The Iron Blast Furnace:
Theory and Practice*.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit deployment

Upload `app.py`, `requirements.txt`, and `README.md` to GitHub.
Deploy `app.py` as the main file in Streamlit Community Cloud.

## Calculation

For 1000 Nm³ dry air, initial oxygen is:

0.21 × 1000 = 210 Nm³

For target fraction `y` and added oxygen `x`:

(210 + x) / (1000 + x) = y

Therefore:

x = (1000y − 210) / (1 − y)

Mass conversion:

m = volume / 22.414 × 32
