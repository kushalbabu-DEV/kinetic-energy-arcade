import os
import math
import base64

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Kinetic Energy Arcade",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Physics helpers
def kinetic_energy(mass, velocity):
    return 0.5 * mass * velocity ** 2

def potential_energy(mass, height, gravity=9.81):
    return mass * gravity * height

def elastic_collision(m1, m2, u1, u2):
    v1 = ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2)
    v2 = ((m2 - m1) * u2 + 2 * m1 * u1) / (m1 + m2)
    return v1, v2

def coaster_height(start_height, progress):
    x = np.array([0, 12, 25, 40, 55, 70, 84, 100], dtype=float)
    y = start_height * np.array([1.00, 0.42, 0.70, 0.18, 0.52, 0.12, 0.30, 0.00])
    return float(np.interp(progress, x, y))

def play_sound(filename):
    path = os.path.join(ASSETS_DIR, "sounds", filename)
    if not os.path.isfile(path):
        return
    with open(path, "rb") as audio:
        encoded = base64.b64encode(audio.read()).decode("ascii")
    st.markdown(
        f'<audio controls style="width:100%;height:34px"><source src="data:audio/wav;base64,{encoded}" type="audio/wav"></audio>',
        unsafe_allow_html=True,
    )

def chart_layout(fig, height=360):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#101323",
        font=dict(color="#F4F4F8", family="Rajdhani"),
        height=height,
        margin=dict(l=18, r=18, t=35, b=25),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,.09)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,.09)")
    return fig

def energy_curve(mass, selected_velocity=None):
    velocities = np.linspace(0, 20, 151)
    energies = 0.5 * mass * velocities ** 2
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=velocities, y=energies, mode="lines", name="Kinetic energy",
        line=dict(color="#2DE2E6", width=4),
        fill="tozeroy", fillcolor="rgba(45,226,230,.08)",
    ))
    if selected_velocity is not None:
        fig.add_trace(go.Scatter(
            x=[selected_velocity], y=[kinetic_energy(mass, selected_velocity)],
            mode="markers", name="Selected value",
            marker=dict(size=14, color="#FF4365", line=dict(color="#FFD23F", width=2)),
        ))
    fig.update_layout(xaxis_title="Velocity (m/s)", yaxis_title="Kinetic energy (J)")
    return chart_layout(fig, 370)

def coaster_track(start_height, progress, current_height):
    positions = np.linspace(0, 100, 301)
    heights = [coaster_height(start_height, p) for p in positions]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=positions, y=heights, mode="lines", name="Track",
        line=dict(color="#2DE2E6", width=5),
        fill="tozeroy", fillcolor="rgba(45,226,230,.08)",
    ))
    fig.add_trace(go.Scatter(
        x=[progress], y=[current_height], mode="markers+text",
        text=["COASTER"], textposition="top center",
        marker=dict(size=22, color="#FF4365", line=dict(color="#FFD23F", width=3)),
    ))
    fig.update_layout(xaxis_title="Track position (%)", yaxis_title="Height (m)")
    fig.update_yaxes(range=[0, start_height * 1.15])
    return chart_layout(fig, 340)

def energy_profile(mass, start_height, progress):
    positions = np.linspace(0, 100, 201)
    heights = np.array([coaster_height(start_height, p) for p in positions])
    total = potential_energy(mass, start_height)
    pe = mass * 9.81 * heights
    ke = np.maximum(0, total - pe)
    current_h = coaster_height(start_height, progress)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=positions, y=pe, mode="lines", name="Potential energy", line=dict(color="#2DE2E6", width=3)))
    fig.add_trace(go.Scatter(x=positions, y=ke, mode="lines", name="Kinetic energy", line=dict(color="#FF4365", width=3)))
    fig.add_vline(x=progress, line_dash="dash", line_color="#FFD23F")
    fig.update_layout(xaxis_title="Track position (%)", yaxis_title="Energy (J)", legend=dict(orientation="h", y=1.12))
    return chart_layout(fig, 330)

# Arcade theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800;900&family=Rajdhani:wght@400;500;600;700&display=swap');
:root{--bg:#0b0d18;--cyan:#2de2e6;--pink:#ff4365;--yellow:#ffd23f;--white:#f4f4f8}
.stApp{background:radial-gradient(ellipse at 78% 0%,rgba(45,226,230,.13),transparent 31%),radial-gradient(ellipse at 10% 35%,rgba(255,67,101,.07),transparent 26%),#0b0d18;color:var(--white)}
.block-container{padding-top:1.3rem;padding-bottom:3rem;max-width:1450px}
h1,h2,h3{font-family:'Orbitron',monospace!important;letter-spacing:.025em}
p,label,div,span{font-family:'Rajdhani',sans-serif}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#151725,#0d101b);border-right:1px solid rgba(45,226,230,.22)}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3{color:var(--yellow)}
.arcade-title{color:var(--yellow);font-family:'Orbitron',monospace;font-size:clamp(1.7rem,3.6vw,3.2rem);font-weight:900;text-shadow:3px 3px 0 var(--pink),0 0 24px rgba(255,210,63,.17);line-height:1.2}
.kicker{color:var(--cyan);font-family:'Orbitron',monospace;letter-spacing:.16em;font-size:.72rem;text-transform:uppercase}
.hero{background:radial-gradient(circle at 50% 20%,rgba(45,226,230,.15),transparent 42%),linear-gradient(145deg,#191b31,#0d101d 72%);border:1px solid rgba(45,226,230,.72);border-radius:22px;padding:clamp(28px,4vw,54px) 22px;text-align:center;box-shadow:0 0 34px rgba(45,226,230,.1),inset 0 0 35px rgba(45,226,230,.035)}
.hero-title{color:var(--yellow);font-family:'Orbitron',monospace;font-size:clamp(2.1rem,5vw,4.4rem);font-weight:900;line-height:1.2;text-shadow:4px 4px 0 var(--pink)}
.hero-sub{color:#c4cce0;font-family:'Orbitron',monospace;letter-spacing:.16em}
.formula,.panel,.mission-card{background:linear-gradient(145deg,#191d32,#111422);border:1px solid rgba(45,226,230,.35);border-radius:14px;padding:16px;margin:7px 0}
.formula{color:var(--cyan);font-family:'Orbitron',monospace;text-align:center}
.score{color:var(--yellow);font-family:'Orbitron',monospace;font-size:2.1rem;font-weight:800}
.mission-card{min-height:140px}
.mission-icon{font-size:2rem}
.mission-title{color:var(--yellow);font-family:'Orbitron',monospace;font-weight:700;margin:8px 0}
.muted{color:#b9c3d8}
div[data-testid="stMetric"]{background:#171a2d;border:1px solid rgba(45,226,230,.28);border-radius:12px;padding:12px}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:var(--yellow)!important;font-family:'Orbitron',monospace!important}
.stButton>button{background:linear-gradient(90deg,#ff4365,#ff5b75);color:white;border:1px solid rgba(255,210,63,.5);border-radius:9px;font-family:'Orbitron',monospace;font-weight:700;min-height:2.6rem}
.stButton>button:hover{background:var(--yellow);color:#101323;border-color:var(--yellow)}
.scanline{height:3px;background:linear-gradient(90deg,transparent,var(--cyan),var(--pink),transparent);border-radius:4px;margin:14px 0}
.motion-track{height:76px;position:relative;overflow:hidden;border-radius:10px;background:linear-gradient(transparent 47%,#68718b 48%,#68718b 55%,transparent 56%),linear-gradient(90deg,rgba(45,226,230,.06),rgba(255,67,101,.06));border:1px solid rgba(45,226,230,.17)}
.motion-ball{position:absolute;top:16px;left:0;width:43px;height:43px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,#2de2e6 35%,#087b91 100%);border:3px solid var(--yellow);box-shadow:0 0 18px var(--cyan);animation:run-track 3s linear infinite}
@keyframes run-track{from{left:4px}to{left:calc(100% - 51px)}}
@media(max-width:700px){.hero{padding:26px 14px}.hero-title{font-size:2rem}.block-container{padding-left:1rem;padding-right:1rem}}
</style>
""", unsafe_allow_html=True)

MISSIONS = [
    "🏠 HOME", "01 VELOCITY RUN", "02 MASS BATTLE", "03 GRAPH ZONE",
    "04 COLLISION ARENA", "05 ROLLER COASTER", "06 CHALLENGE MODE",
    "07 LEARNING CORNER", "08 ABOUT PROJECT",
]
with st.sidebar:
    logo = os.path.join(ASSETS_DIR, "images", "arcade_bolt.png")
    if os.path.isfile(logo):
        st.image(logo, width=76)
    st.markdown("## ⚡ ARCADE MENU")
    page = st.radio("SELECT YOUR MISSION", MISSIONS, key="arcade_page")
    sound_on = st.toggle("Sound effects", value=False, key="arcade_sound")
    st.divider()
    st.caption("OM  •  KUSHAL  •  ISHANI  •  ATMIKA")
    st.caption("ECS | COMPUTATIONAL PHYSICS | CCE-01")

def header(section, title, subtitle):
    st.markdown(f'<div class="kicker">{section}</div><div class="arcade-title">{title}</div><p class="muted">{subtitle}</p><div class="scanline"></div>', unsafe_allow_html=True)

if page == "🏠 HOME":
    st.markdown('<div class="hero"><div class="kicker">PLAYER 01  •  INSERT COIN  •  CCE-01</div><br><div class="hero-title">KINETIC ENERGY<br>ARCADE</div><br><div class="hero-sub">A RETRO VIRTUAL PHYSICS LAB</div><br><div class="formula">KE = ½ × m × v²</div><p>RUN EXPERIMENTS  •  COMPARE OBJECTS  •  EXPLORE ENERGY IN MOTION</p><div style="color:#ff4365;font-size:25px;letter-spacing:12px">✦ ▣ ⚡ ▣ ✦</div></div>', unsafe_allow_html=True)
    st.markdown("### SELECT YOUR NEXT MISSION")
    cards = [
        ("🏎️", "VELOCITY RUN", "Change speed and watch kinetic energy respond."),
        ("⚖️", "MASS BATTLE", "Compare objects with different masses."),
        ("📈", "GRAPH ZONE", "Explore the velocity-squared curve."),
        ("💥", "COLLISION ARENA", "Animate an ideal elastic collision."),
        ("🎢", "ROLLER COASTER", "Watch potential and kinetic energy change."),
        ("🕹️", "CHALLENGE MODE", "Test your understanding and earn a score."),
    ]
    for row in (cards[:3], cards[3:]):
        cols = st.columns(3)
        for col, (icon, title, desc) in zip(cols, row):
            with col:
                st.markdown(f'<div class="mission-card"><div class="mission-icon">{icon}</div><div class="mission-title">{title}</div><div class="muted">{desc}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="kicker">EXTRA LEVELS</div><b>LEARNING CORNER</b> — formulas, worked examples and assumptions. &nbsp; <b>ABOUT PROJECT</b> — team, tools and project details.</div>', unsafe_allow_html=True)
    if sound_on:
        with st.expander("ARCADE START SOUND"):
            play_sound("start.wav")
    st.stop()

st.markdown('<div class="kicker">PLAYER 01  •  COMPUTATIONAL PHYSICS  •  CCE-01</div><div class="arcade-title">⚡ KINETIC ENERGY ARCADE</div><div class="formula">KE = ½ × m × v²</div><div class="scanline"></div>', unsafe_allow_html=True)

if page.startswith("01"):
    header("MISSION 01 / MOTION LAB", "VELOCITY RUN", "Change velocity and watch the object move faster. Keep mass fixed to explore the v-squared relationship.")
    left, right = st.columns([1, 1.25])
    with left:
        mass = st.slider("OBJECT MASS (kg)", 1.0, 20.0, 2.0, 0.5)
        velocity = st.slider("VELOCITY (m/s)", 0.0, 20.0, 5.0, 0.5)
        energy = kinetic_energy(mass, velocity)
        st.markdown(f'<div class="panel"><div class="kicker">ENERGY SCORE</div><div class="score">{energy:.2f} J</div><p>½ × {mass:g} × {velocity:g}²</p></div>', unsafe_allow_html=True)
        st.metric("MOMENTUM (kg·m/s)", f"{mass * velocity:.2f}")
        if sound_on:
            with st.expander("ENERGY SCORE SOUND"):
                play_sound("score.wav")
    with right:
        duration = max(0.65, 5.5 - velocity * 0.23)
        state = "paused" if velocity == 0 else "running"
        st.markdown(f'<div class="panel"><div class="kicker">LIVE MOTION TRACK</div><div class="motion-track"><div class="motion-ball" style="animation-duration:{duration:.2f}s;animation-play-state:{state}"></div></div><p>Speed setting: {velocity:.1f} m/s</p></div>', unsafe_allow_html=True)
        st.plotly_chart(energy_curve(mass, velocity), use_container_width=True, config={"displayModeBar": False})
    st.success("PHYSICS FACT: Doubling velocity at constant mass makes kinetic energy four times larger.")
    with st.expander("WHY DOES THIS HAPPEN?"):
        st.write("Velocity is squared in the kinetic-energy equation. If velocity changes from 5 m/s to 10 m/s, the squared term changes from 25 to 100. With mass unchanged, kinetic energy becomes four times larger.")

elif page.startswith("02"):
    header("MISSION 02 / COMPARISON LAB", "MASS BATTLE", "Compare two objects travelling at the same speed. The larger visual object represents the greater mass.")
    velocity = st.slider("COMMON VELOCITY (m/s)", 0.0, 20.0, 6.0, 0.5)
    a, b = st.columns(2)
    with a:
        ma = st.slider("OBJECT A MASS (kg)", 1.0, 20.0, 2.0, 0.5)
    with b:
        mb = st.slider("OBJECT B MASS (kg)", 1.0, 20.0, 8.0, 0.5)
    ea, eb = kinetic_energy(ma, velocity), kinetic_energy(mb, velocity)
    visual = go.Figure(go.Scatter(
        x=[1, 2], y=[0, 0], mode="markers+text",
        text=[f"A • {ma:g} kg", f"B • {mb:g} kg"],
        textposition="bottom center",
        marker=dict(size=[28 + ma * 5, 28 + mb * 5], color=["#2DE2E6", "#FF4365"], line=dict(color="#FFD23F", width=3)),
    ))
    visual.update_layout(xaxis=dict(visible=False, range=[0, 3]), yaxis=dict(visible=False, range=[-1.3, 1.3]))
    st.plotly_chart(chart_layout(visual, 275), use_container_width=True, config={"displayModeBar": False})
    c1, c2 = st.columns(2)
    c1.metric("OBJECT A KINETIC ENERGY", f"{ea:.2f} J")
    c2.metric("OBJECT B KINETIC ENERGY", f"{eb:.2f} J")
    bars = go.Figure(go.Bar(x=["OBJECT A", "OBJECT B"], y=[ea, eb], marker_color=["#2DE2E6", "#FF4365"], text=[f"{ea:.1f} J", f"{eb:.1f} J"], textposition="outside"))
    bars.update_layout(yaxis_title="Kinetic energy (J)")
    st.plotly_chart(chart_layout(bars, 320), use_container_width=True, config={"displayModeBar": False})
    st.info("At the same velocity, kinetic energy is directly proportional to mass. Object size is a visual cue, not a physical scale.")

elif page.startswith("03"):
    header("MISSION 03 / DATA VISUALISATION", "GRAPH ZONE", "Explore the relationship between velocity and kinetic energy using a live graph.")
    left, right = st.columns([1, 1.5])
    with left:
        mass = st.slider("MASS (kg)", 1.0, 20.0, 4.0, 0.5)
        velocity = st.slider("SELECTED VELOCITY (m/s)", 0.0, 20.0, 8.0, 0.5)
        energy = kinetic_energy(mass, velocity)
        st.metric("SELECTED KINETIC ENERGY", f"{energy:.2f} J")
        st.markdown(f'<div class="panel"><div class="kicker">CALCULATION</div><div class="score">{energy:.2f} J</div><p>½ × {mass:g} × {velocity:g}²</p></div>', unsafe_allow_html=True)
    with right:
        st.plotly_chart(energy_curve(mass, velocity), use_container_width=True, config={"displayModeBar": False})
    st.info("For constant mass, kinetic energy follows a parabolic curve because it depends on velocity squared.")

elif page.startswith("04"):
    header("MISSION 04 / INTERACTION LAB", "COLLISION ARENA", "Set two objects moving along one straight line. Observe their final velocities and conservation checks.")
    a, b = st.columns(2)
    with a:
        m1 = st.slider("OBJECT A MASS (kg)", 1.0, 10.0, 2.0, 0.5)
        u1 = st.slider("OBJECT A INITIAL VELOCITY (m/s)", -10.0, 10.0, 5.0, 0.5)
    with b:
        m2 = st.slider("OBJECT B MASS (kg)", 1.0, 10.0, 2.0, 0.5)
        u2 = st.slider("OBJECT B INITIAL VELOCITY (m/s)", -10.0, 10.0, 0.0, 0.5)
    v1, v2 = elastic_collision(m1, m2, u1, u2)
    p_before, p_after = m1 * u1 + m2 * u2, m1 * v1 + m2 * v2
    ke_before = kinetic_energy(m1, u1) + kinetic_energy(m2, u2)
    ke_after = kinetic_energy(m1, v1) + kinetic_energy(m2, v2)
    if u1 > u2:
        gap, hit_gap = 6.0, 0.65
        hit_time = 2 * (gap - hit_gap) / (u1 - u2)
        pre = np.linspace(0, hit_time, 24)
        post = np.linspace(0, max(1.0, 7.0 / max(abs(v1), abs(v2), 1.0)), 30)[1:]
        positions = [(-gap + u1*t, gap + u2*t) for t in pre]
        positions += [(-hit_gap + v1*t, hit_gap + v2*t) for t in post]
        frames = [go.Frame(name=str(i), data=[go.Scatter(x=[x, y], y=[0, 0])]) for i, (x, y) in enumerate(positions)]
        fig = go.Figure(data=[go.Scatter(x=list(positions[0]), y=[0, 0], mode="markers+text", text=["OBJECT A", "OBJECT B"], textposition="top center", marker=dict(size=[25+4.2*m1, 25+4.2*m2], color=["#2DE2E6", "#FF4365"], line=dict(color="#FFD23F", width=3)))], frames=frames)
        fig.update_layout(xaxis=dict(range=[min(x for pair in positions for x in pair)-4, max(x for pair in positions for x in pair)+4], title="Illustrative track position (m)"), yaxis=dict(visible=False, range=[-1, 1]), updatemenus=[dict(type="buttons", buttons=[dict(label="▶ PLAY", method="animate", args=[None, {"frame": {"duration": 65, "redraw": True}, "fromcurrent": True}]), dict(label="↺ RESTART", method="animate", args=[["0"], {"mode": "immediate", "frame": {"duration": 0}}])])])
        st.plotly_chart(chart_layout(fig, 350), use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("To view the left-to-right collision animation, set Object A's initial velocity higher than Object B's.")
    c1, c2 = st.columns(2)
    c1.metric("A FINAL VELOCITY", f"{v1:.2f} m/s")
    c2.metric("B FINAL VELOCITY", f"{v2:.2f} m/s")
    c1, c2 = st.columns(2)
    c1.metric("TOTAL KE BEFORE", f"{ke_before:.2f} J")
    c2.metric("TOTAL KE AFTER", f"{ke_after:.2f} J")
    c1, c2 = st.columns(2)
    c1.metric("MOMENTUM BEFORE", f"{p_before:.2f} kg·m/s")
    c2.metric("MOMENTUM AFTER", f"{p_after:.2f} kg·m/s")
    st.success(f"Conservation check — momentum difference: {abs(p_before-p_after):.8f}; kinetic-energy difference: {abs(ke_before-ke_after):.8f} J.")
    st.info("This is an ideal one-dimensional perfectly elastic collision.")
    if sound_on:
        with st.expander("COLLISION SOUND EFFECT"):
            play_sound("collision.wav")

elif page.startswith("05"):
    header("MISSION 05 / ENERGY TRANSFER", "ROLLER COASTER ENERGY RIDE", "Move the coaster along a multi-hill track and observe gravitational potential energy changing into kinetic energy.")
    a, b, c = st.columns(3)
    with a:
        mass = st.slider("COASTER MASS (kg)", 10.0, 100.0, 50.0, 5.0)
    with b:
        start_height = st.slider("STARTING HEIGHT (m)", 10.0, 60.0, 40.0, 1.0)
    with c:
        progress = st.slider("COASTER POSITION (%)", 0, 100, 40, 1)
    height = coaster_height(start_height, progress)
    total = potential_energy(mass, start_height)
    pe = potential_energy(mass, height)
    ke = max(0.0, total - pe)
    speed = math.sqrt(2 * ke / mass) if mass > 0 else 0
    st.plotly_chart(coaster_track(start_height, progress, height), use_container_width=True, config={"displayModeBar": False})
    x, y, z = st.columns(3)
    x.metric("POTENTIAL ENERGY", f"{pe:.1f} J")
    y.metric("KINETIC ENERGY", f"{ke:.1f} J")
    z.metric("SPEED", f"{speed:.2f} m/s")
    st.metric("TOTAL MECHANICAL ENERGY", f"{pe+ke:.1f} J")
    st.plotly_chart(energy_profile(mass, start_height, progress), use_container_width=True, config={"displayModeBar": False})
    st.info("Model assumption: friction and air resistance are ignored, so total mechanical energy remains constant. The coaster starts from rest.")

elif page.startswith("06"):
    header("MISSION 06 / ARCADE QUIZ", "PHYSICS CHALLENGE", "Answer five quick questions. Check your score and revise the concepts you missed.")
    questions = [
        ("What is the SI unit of kinetic energy?", ["Newton", "Joule", "Watt", "Pascal"], 1, "Energy is measured in joules (J)."),
        ("If velocity doubles while mass stays the same, kinetic energy becomes…", ["2 times", "3 times", "4 times", "8 times"], 2, "KE depends on v², so 2² = 4."),
        ("At the same velocity, which object has greater kinetic energy?", ["The heavier object", "The lighter object", "Both always equal", "Cannot be determined"], 0, "At fixed velocity, KE is directly proportional to mass."),
        ("Which quantities are conserved in an ideal elastic collision?", ["Only speed", "Only momentum", "Momentum and kinetic energy", "Neither"], 2, "An ideal elastic collision conserves total momentum and total kinetic energy."),
        ("As a coaster moves down a frictionless track, what happens?", ["KE changes to PE", "PE changes to KE", "Both become zero", "Mass increases"], 1, "As height decreases, gravitational potential energy is converted into kinetic energy."),
    ]
    with st.form("physics_challenge"):
        choices = []
        for i, (question, options, answer, explanation) in enumerate(questions):
            st.markdown(f"**LEVEL {i+1:02d}** · {question}")
            choices.append(st.radio("Choose one answer", options, key=f"quiz_{i}", label_visibility="collapsed"))
            if i < len(questions)-1:
                st.divider()
        submitted = st.form_submit_button("SUBMIT MY SCORE ⚡", use_container_width=True)
    if submitted:
        st.session_state["quiz_score"] = sum(choice == questions[i][1][questions[i][2]] for i, choice in enumerate(choices))
        st.session_state["quiz_choices"] = choices
    if st.session_state.get("quiz_score") is not None:
        score = st.session_state["quiz_score"]
        st.markdown(f'<div class="panel"><div class="kicker">YOUR ARCADE SCORE</div><div class="score">{score} / 5</div><p>{"ENERGY CHAMPION!" if score == 5 else "NICE RUN! KEEP PRACTISING." if score >= 3 else "KEEP TRAINING, PLAYER 01!"}</p></div>', unsafe_allow_html=True)
        for i, (question, options, answer, explanation) in enumerate(questions):
            if st.session_state["quiz_choices"][i] == options[answer]:
                st.success(f"Level {i+1}: Correct — {explanation}")
            else:
                st.warning(f"Level {i+1}: Correct answer: {options[answer]}. {explanation}")
        if st.button("PLAY AGAIN ↻", use_container_width=True):
            st.session_state["quiz_score"] = None
            st.rerun()

elif page.startswith("07"):
    header("MISSION 07 / STUDY DECK", "LEARNING CORNER", "Quick explanations, equations and worked examples behind the simulations.")
    st.markdown("### 01 · KINETIC ENERGY")
    st.latex(r"KE = \frac{1}{2}mv^2")
    st.write("Kinetic energy is the energy an object possesses because it is moving. It depends on the object's mass and the square of its speed.")
    st.markdown("**Worked example:** For a 2 kg object moving at 5 m/s:")
    st.latex(r"KE = \frac{1}{2}\times 2\times 5^2 = 25\;J")
    st.divider()
    st.markdown("### 02 · GRAVITATIONAL POTENTIAL ENERGY")
    st.latex(r"PE = mgh")
    st.write("Gravitational potential energy depends on mass, gravitational acceleration and height above the selected reference level.")
    st.markdown("**Worked example:** A 2 kg object at a height of 3 m, using g = 9.81 m/s²:")
    st.latex(r"PE = 2\times 9.81\times 3 = 58.86\;J")
    st.divider()
    st.markdown("### 03 · MOMENTUM")
    st.latex(r"p = mv")
    st.write("Linear momentum is the product of mass and velocity. In an isolated system, total momentum is conserved during a collision.")
    st.divider()
    st.markdown("### 04 · PERFECTLY ELASTIC COLLISION")
    st.write("For an ideal one-dimensional perfectly elastic collision, total momentum and total kinetic energy before the collision equal their respective totals after the collision.")
    st.latex(r"m_1u_1+m_2u_2=m_1v_1+m_2v_2")
    st.divider()
    st.markdown("- Collision Arena uses an ideal one-dimensional perfectly elastic collision.\n- Roller Coaster starts from rest and ignores friction and air resistance.\n- Mass Battle object sizes are visual indicators, not to-scale physical drawings.\n- The simulations are mathematical models, not measurements from physical laboratory equipment.")

elif page.startswith("08"):
    header("MISSION 08 / PROJECT FILE", "ABOUT THE PROJECT", "The people, programming tools and physics ideas behind Kinetic Energy Arcade.")
    st.markdown("### PROJECT OVERVIEW")
    st.write("Kinetic Energy Arcade is an interactive virtual physics laboratory developed for Computational Physics. It uses Python calculations, graphs and animations to help users explore how mass, velocity and height affect mechanical energy.")
    st.markdown("### PROJECT TEAM")
    team = [("Om", "Roll No. 29"), ("Kushal Babu", "Roll No. 34"), ("Ishani", "Roll No. 41"), ("Atmika", "Roll No. 62")]
    cols = st.columns(4)
    for col, (name, roll) in zip(cols, team):
        with col:
            st.markdown(f'<div class="mission-card"><div class="mission-icon">👾</div><div class="mission-title">{name}</div><div class="muted">{roll}</div></div>', unsafe_allow_html=True)
    st.markdown("### TECHNOLOGIES USED")
    c1, c2, c3 = st.columns(3)
    c1.metric("PROGRAMMING", "Python")
    c2.metric("INTERFACE", "Streamlit")
    c3.metric("GRAPHS", "Plotly + NumPy")
    st.markdown("### PROJECT LIMITATIONS")
    st.write("The models use idealised assumptions. Real-world friction, air resistance, rotation, track deformation and other losses are not included unless specifically stated.")

st.divider()
st.markdown('<div class="kicker">KINETIC ENERGY ARCADE 2.0  •  BUILT WITH PYTHON  •  COMPUTATIONAL PHYSICS</div>', unsafe_allow_html=True)
