# ⚡ Kinetic Energy Arcade 2.0

A retro arcade-themed virtual physics lab built with **Python, Streamlit, NumPy and Plotly**. The project makes energy and motion concepts easier to explore through interactive controls, charts, visual simulations and a short physics challenge.

## Arcade missions

| Mission | What it demonstrates |
| --- | --- |
| **Velocity Run** | Change mass and velocity, calculate kinetic energy and inspect the velocity–energy curve. |
| **Mass Battle** | Compare two masses moving at the same velocity. |
| **Graph Zone** | Explore the parabolic relationship between velocity and kinetic energy. |
| **Collision Arena** | Visualise an ideal one-dimensional elastic collision and compare momentum and kinetic energy before and after. |
| **Roller Coaster** | Explore how gravitational potential energy changes into kinetic energy along an illustrative track. |
| **Challenge Mode** | Answer five questions and review explanations. |
| **Learning Corner** | Review equations, examples and model assumptions. |
| **About Project** | View the project details, team and technologies. |

## Physics used

- Kinetic energy: `KE = 1/2 × m × v²`
- Gravitational potential energy: `PE = m × g × h`
- Linear momentum: `p = m × v`
- In an ideal one-dimensional elastic collision, total momentum and total kinetic energy are conserved.

## Run the project locally

1. Install Python 3.10 or later.
2. Clone or download this repository.
3. Open a terminal in `Kinetic_Energy_Arcade_COMPLETE`.
4. Install the required packages:

   ```powershell
   py -m pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   py -m streamlit run app.py
   ```

6. Open `http://localhost:8501` in your browser.

You can also use `INSTALL_AND_RUN.bat` to install dependencies and start the app, or `RUN_ARCADE.bat` after installation.

## Publish the website with Streamlit Community Cloud

This is a **Streamlit web application**, not a static HTML site.

1. Push the repository to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/) and choose **Create app**.
3. Select this repository, the `main` branch, and set the main file path to:

   `Kinetic_Energy_Arcade_COMPLETE/app.py`

4. Deploy. Streamlit installs packages from `Kinetic_Energy_Arcade_COMPLETE/requirements.txt`.
5. After deployment, use the generated public URL to share the arcade.

For an existing deployment, keep the same app and main-file path. New commits to the connected branch should trigger a redeploy. Check the Streamlit deployment logs if a build fails.

## Repository layout

```text
Kinetic_Energy_Arcade_COMPLETE/
├── .streamlit/
│   └── config.toml
├── app.py
├── requirements.txt
├── README.md
├── assets/
│   ├── images/
│   │   └── arcade_bolt.png
│   └── sounds/
│       ├── start.wav
│       ├── collision.wav
│       └── score.wav
└── docs/
    └── ONLINE_DEPLOYMENT.md
```

## Team

- Om — Roll No. 29
- Kushal Babu — Roll No. 34
- Ishani — Roll No. 41
- Atmika — Roll No. 62

## Model assumptions and limitations

- The simulations are educational mathematical models, not measurements from physical laboratory equipment.
- Collision Arena assumes a one-dimensional perfectly elastic collision.
- The roller coaster starts from rest and ignores friction and air resistance.
- Mass Battle object sizes are visual indicators, not to-scale drawings.
- Google Fonts load externally when internet access is available; fallback fonts are used otherwise.
