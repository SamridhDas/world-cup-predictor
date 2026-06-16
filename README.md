# FIFA World Cup 2026 Predictor

A full-scale World Cup prediction platform built using Python, historical international football data, Elo ratings, statistical team ratings, and Monte Carlo simulation.

The project simulates the entire FIFA World Cup 2026 format, including group stages, best third-place qualification, knockout rounds, extra time, and penalty shootouts. Match outcomes are generated using team attack, defence, form, and Elo-based ratings derived from international matches since 2018.

## Features

* FIFA World Cup 2026 tournament simulation
* Elo-based team strength ratings
* Attack and defence rating system
* Weighted historical performance analysis
* Group stage and knockout stage simulation
* Extra time and penalty shootouts
* Match-level statistics (shots, possession, corners, cards)
* Monte Carlo tournament forecasting
* Team qualification probabilities
* Future machine learning integration for expected goals prediction

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-learn (planned)
* FastAPI (planned)
* PostgreSQL (planned)
* Next.js (planned)

## Methodology

Team strength is calculated using a combination of:

* Historical match performance
* Tournament-weighted results
* Attack and defence ratings
* Recent form
* Elo ratings

The simulator then generates expected goals for each match and uses probability distributions to simulate realistic football scores. Thousands of tournament simulations are run to estimate each team's probability of reaching different stages and winning the tournament.
