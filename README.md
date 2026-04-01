# 💎 Diamond Dynamics: Consistency + Adjustment Tool

## Overview  
Diamond Dynamics is a Streamlit application that evaluates player performance through consistency and adjustment using game-by-game data.

Rather than relying on static averages, players establish their own baseline from their data, allowing performance to be evaluated relative to themselves. As each new game is added, the dataset becomes cumulative, meaning trends, baselines, and scores continuously evolve over time.

---

## Core Concepts  

- Consistency → How stable a player’s performance is relative to their evolving baseline  
- Adjustment → How well a player responds after performance changes  

Both metrics update with each new data point, creating a dynamic view of performance over time.

---

## Features  

- Upload game-by-game player data (CSV or Excel)  
- Supports Game or Date-based sequencing  
- Player-specific baseline (self-referenced)  
- Cumulative, evolving calculations after each game  
- Rolling trends for consistency and adjustment  
- Automated insights summarizing performance, trends, and player profile  

---

## How It Works  

1. Upload your dataset (e.g., game logs from FanGraphs)  
2. Select a time column (Game or Date) and a stat (OPS, OBP, etc.)  
3. The tool:
   - Builds a player-specific baseline  
   - Updates calculations cumulatively with each data point  
   - Tracks consistency and adjustment over time  
   - Generates written insights to contextualize performance  
4. Outputs include metrics, trend charts, and insights  

---

## Example Data  

```csv
Game,OPS
1,0.850
2,0.920
3,0.780
```

or

```csv
Date,OBP
2026-03-01,0.300
2026-03-02,0.400
2026-03-03,0.350
```

---

## Tech Stack  

- Python  
- Streamlit  
- Pandas  
- NumPy  
- Altair  

---

## Run Locally  

```bash
git clone https://github.com/yourusername/diamond-dynamics-tool.git
cd diamond-dynamics-tool
pip install -r requirements.txt
streamlit run app.py
```

---

## Author  
Grace Maretsky  


