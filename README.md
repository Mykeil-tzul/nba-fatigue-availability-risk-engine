# NBA Player Fatigue + Availability Risk Engine

A sports analytics and machine learning project that predicts short-term performance dips and workload-related availability risk in NBA players using game logs, schedule density, travel burden, rest patterns, and rolling performance baselines.

## Why I built this

As a former professional basketball player, I wanted to quantify something players feel in real life: fatigue is cumulative, travel matters, compressed schedules matter, and not all minutes cost the same.

This project turns that lived experience into a data product:
- a fatigue risk engine
- a performance dip prediction model
- a reusable player-level prediction pipeline

The goal is to show how basketball knowledge, data science, and machine learning engineering can come together in one real-world project.

## Project goals

This project combines three ideas into one:

1. **NBA Fatigue Risk Engine**  
   Estimate how schedule density, minutes load, and travel stress affect player performance.

2. **Performance Degradation Under Schedule Density**  
   Predict whether a player is likely to experience a next-game performance dip.

3. **Player Fatigue Prediction Pipeline**  
   Build a reusable end-to-end pipeline for ingesting NBA data, engineering workload features, training models, and generating predictions.

## Core questions

- Does playing in back-to-backs increase next-game performance decline?
- How much do rolling minutes and recent workload affect efficiency?
- Does travel burden raise fatigue-related risk?
- Can we predict short-term performance drops from schedule and workload context?
- Which player profiles appear most vulnerable to schedule compression?

## Target outcomes

This project focuses on two modeling tasks:

### 1) Classification
Predict whether a player will experience a **next-game performance dip**.

Example definitions may include:
- points below rolling average
- FG% / TS% below baseline
- Game Score below expected level
- meaningful drop in all-around production

### 2) Risk scoring / regression
Estimate a continuous **fatigue or availability risk score** based on:
- recent minutes
- days of rest
- back-to-back flags
- 3 games in 4 nights / 4 games in 6 nights
- travel burden
- age and experience curves

## Tech stack

- **Python**
- **pandas**
- **numpy**
- **scikit-learn**
- **SQL**
- **Matplotlib / Plotly**
- **Streamlit**
- **Git + GitHub**

## Data sources

Planned data sources include:
- NBA game logs
- Basketball-Reference game logs and player pages
- Publicly available schedule data
- Public injury / availability reports where appropriate

## Feature ideas

Examples of planned features:

### Schedule load
- back-to-back indicator
- games in last 3 days
- games in last 5 days
- 3-in-4 nights
- 4-in-6 nights
- days of rest

### Workload
- minutes last game
- rolling average minutes
- rolling points
- rolling assists
- rolling rebounds
- rolling shooting efficiency
- rolling Game Score

### Travel and context
- home vs away
- road trip length
- travel distance between games
- opponent strength proxy

### Player profile
- age
- years in league
- position group
- season-to-date workload

## Planned workflow

1. Collect player game log data
2. Clean and standardize raw data
3. Create workload and schedule-density features
4. Define performance dip labels
5. Train baseline classification models
6. Improve with better feature engineering
7. Evaluate model performance
8. Visualize fatigue-risk patterns
9. Build a small Streamlit app for interactive exploration

## Repository structure

```text
nba-fatigue-availability-risk-engine/
│
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling.ipynb
│   └── 05_error_analysis.ipynb
│
├── src/
│   ├── data_collection.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── labeling.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
│
├── sql/
├── models/
├── reports/
├── app/
└── tests/
