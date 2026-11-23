# Kinetic Energy Arcade — Complete Project

A retro arcade-style online virtual physics lab built with Python, Streamlit, NumPy and Plotly.

## Included features
1. Arcade home screen with Start Game.
2. Velocity Run with speed-controlled CSS motion animation and live energy graph.
3. Mass Battle with differently sized object visuals and energy comparison.
4. Graph Zone with a live kinetic-energy curve.
5. Collision Arena with animated 1D perfectly elastic collision, Play/Restart/Pause controls, final velocities and energy conservation check.
6. Roller Coaster Energy Ride showing height, potential energy, kinetic energy and speed.
7. Bundled pixel-art bolt logo and original synthesized WAV sound effects.

## Physics
- Kinetic energy: KE = 1/2 × m × v²
- Gravitational potential energy: PE = m × g × h
- Elastic collision: one-dimensional ideal model; total momentum and kinetic energy are conserved.
- Roller coaster model ignores friction and air resistance.

## Run locally (Windows)
Open this folder in VS Code. In its terminal run:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## Publish online using Streamlit Community Cloud
1. Create or sign in to GitHub.
2. Create a new repository, e.g. `kinetic-energy-arcade`.
3. Upload the full contents of this folder (including `assets/`, `app.py`, and `requirements.txt`).
4. Open Streamlit Community Cloud and connect your GitHub account.
5. Choose the repository, branch (usually `main`) and main file path `app.py`.
6. Click Deploy. When deployment finishes, copy the public app URL and share it with your teacher.

Do not upload passwords, API keys or private files. This project does not require secrets.

## Team
Om (Roll 29, PRN 126BTEC1141)
Kushal Babu (Roll 34, PRN 126BTEC1064)
Ishani (Roll 41, PRN 126BTEC1131)
Atmika (Roll 62, PRN 126BTEC1111)
