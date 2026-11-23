import os
import math
import base64
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# KINETIC ENERGY ARCADE - Complete student virtual physics lab
# ============================================================
st.set_page_config(page_title="Kinetic Energy Arcade", page_icon="⚡",
                   layout="wide", initial_sidebar_state="collapsed")

BASE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(BASE, "assets")

# ---------------- PHYSICS FUNCTIONS ----------------
def calculate_kinetic_energy(mass, velocity):
    """Kinetic energy in joules: KE = 1/2 * m * v^2."""
    return 0.5 * mass * velocity ** 2

def calculate_potential_energy(mass, height, gravity=9.81):
    """Gravitational potential energy in joules: PE = m*g*h."""
    return mass * gravity * height

def calculate_velocity_energy_data(mass, max_velocity=20):
    velocities = np.linspace(0, max_velocity, 101)
    energies = [calculate_kinetic_energy(mass, v) for v in velocities]
    return velocities, energies

def compare_masses(mass_a, mass_b, velocity):
    return (calculate_kinetic_energy(mass_a, velocity),
            calculate_kinetic_energy(mass_b, velocity))

def elastic_collision(m1, m2, u1, u2):
    """Final velocities for a one-dimensional perfectly elastic collision."""
    v1 = ((m1-m2)*u1 + 2*m2*u2)/(m1+m2)
    v2 = ((m2-m1)*u2 + 2*m1*u1)/(m1+m2)
    return v1, v2

def audio_html(filename):
    """Return an HTML audio player for a bundled WAV sound."""
    path = os.path.join(ASSET, "sounds", filename)
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f'<audio controls style="width:100%;height:34px"><source src="data:audio/wav;base64,{encoded}" type="audio/wav"></audio>'

def arcade_energy_graph(mass, selected_velocity=None):
    velocities, energies = calculate_velocity_energy_data(mass)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=velocities, y=energies, mode="lines",
        name="KINETIC ENERGY", line=dict(color="#2DE2E6", width=4),
        fill="tozeroy", fillcolor="rgba(45,226,230,.08)"))
    if selected_velocity is not None:
        fig.add_trace(go.Scatter(x=[selected_velocity],
            y=[calculate_kinetic_energy(mass, selected_velocity)],
            mode="markers", name="SELECTED VALUE",
            marker=dict(color="#FF4365", size=15, line=dict(color="#FFD23F",width=2))))
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0D0D1A", font=dict(color="#F4F4F8",family="Courier New"),
        xaxis_title="VELOCITY (m/s)", yaxis_title="KINETIC ENERGY (J)",
        margin=dict(l=18,r=18,t=35,b=20),
        xaxis=dict(gridcolor="rgba(255,255,255,.10)"),
        yaxis=dict(gridcolor="rgba(255,255,255,.10)"))
    return fig

def collision_figure(m1,m2,u1,u2,v1,v2):
    """Animated 1D collision illustration; valid when A closes on B (u1 > u2)."""
    if u1 <= u2:
        return None
    t_hit=10/(u1-u2)
    pre=np.linspace(0,t_hit,22)
    post=np.linspace(0,5,24)[1:]
    positions=[(-5+u1*t,5+u2*t) for t in pre]
    positions += [(v1*t,v2*t) for t in post]
    size_a=25+4.2*m1; size_b=25+4.2*m2
    fig=go.Figure(data=[go.Scatter(x=[positions[0][0],positions[0][1]],y=[0,0],
        mode="markers+text",text=["OBJECT A","OBJECT B"],textposition="top center",
        textfont=dict(color="#F4F4F8",size=12,family="Courier New"),
        marker=dict(size=[size_a,size_b],color=["#2DE2E6","#FF4365"],
                    line=dict(color="#FFD23F",width=3)),showlegend=False)])
    frames=[]
    for i,(xa,xb) in enumerate(positions):
        phase="APPROACHING" if i<len(pre) else "AFTER COLLISION"
        frames.append(go.Frame(name=str(i),data=[go.Scatter(x=[xa,xb],y=[0,0])],
            layout=go.Layout(annotations=[dict(x=.5,y=1.12,xref="paper",yref="paper",
                text=phase,showarrow=False,font=dict(color="#FFD23F",size=14))])))
    fig.frames=frames
    steps=[dict(method="animate",args=[[str(i)],{"mode":"immediate",
        "frame":{"duration":65,"redraw":True},"transition":{"duration":0}}],label=str(i+1))
        for i in range(len(frames))]
    xs=[p for pair in positions for p in pair]
    fig.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0D0D1A",font=dict(color="#F4F4F8",family="Courier New"),
        height=350,margin=dict(l=20,r=20,t=75,b=35),showlegend=False,
        xaxis=dict(range=[min(xs)-3,max(xs)+3],title="ILLUSTRATIVE TRACK POSITION",
                   gridcolor="rgba(255,255,255,.08)"),
        yaxis=dict(visible=False,range=[-1,1]),
        shapes=[dict(type="line",x0=min(xs)-3,x1=max(xs)+3,y0=0,y1=0,
                     line=dict(color="#59627A",width=8))],
        updatemenus=[dict(type="buttons",showactive=False,x=.01,y=1.22,
            buttons=[
                dict(label="▶ PLAY",method="animate",args=[None,{"fromcurrent":True,
                    "frame":{"duration":65,"redraw":True},"transition":{"duration":0}}]),
                dict(label="↺ RESTART",method="animate",args=[[str(0)],{"mode":"immediate",
                    "frame":{"duration":0,"redraw":True},"transition":{"duration":0}}]),
                dict(label="Ⅱ PAUSE",method="animate",args=[[None],{"mode":"immediate",
                    "frame":{"duration":0,"redraw":False},"transition":{"duration":0}}])])],
        sliders=[dict(active=0,x=.17,y=1.22,len=.8,currentvalue=dict(prefix="FRAME "),
            steps=steps)])
    return fig

# ---------------- ARCADE STYLE ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800&family=Rajdhani:wght@500;600;700&display=swap');
.stApp {background:radial-gradient(circle at 80% 0%,rgba(45,226,230,.10),transparent 28%),#0D0D1A;color:#F4F4F8}
header[data-testid="stHeader"]{background:rgba(13,13,26,.9)}
.block-container{padding-top:1.5rem;padding-bottom:2.5rem;max-width:1450px}
h1,h2,h3{font-family:'Orbitron',monospace!important;letter-spacing:.035em}
p,label,div,span{font-family:'Rajdhani',sans-serif}
.arcade-title{color:#FFD23F;font-family:'Orbitron',monospace;font-size:clamp(1.8rem,4vw,3.2rem);font-weight:800;text-shadow:3px 3px 0 #FF4365}
.kicker{color:#2DE2E6;font-family:'Orbitron',monospace;letter-spacing:.18em;font-size:.75rem}
.panel{background:#17192B;border:1px solid rgba(45,226,230,.35);border-radius:14px;padding:16px;margin:8px 0}
.score{color:#FFD23F;font-family:'Orbitron',monospace;font-size:2.2rem;font-weight:800}
.formula{background:#17192B;border:1px solid #2DE2E6;color:#2DE2E6;padding:13px 18px;border-radius:10px;font-family:'Orbitron',monospace}
div[data-testid="stMetric"]{background:#17192B;border:1px solid rgba(45,226,230,.3);border-radius:12px;padding:12px}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:#FFD23F!important;font-family:'Orbitron',monospace!important}
.stButton>button{background:#FF4365;color:white;border:0;border-radius:8px;font-family:'Orbitron',monospace;font-weight:700}
.stButton>button:hover{background:#FFD23F;color:#0D0D1A}
div[data-testid="stRadio"] label{color:#F4F4F8!important}
hr{border-color:rgba(130,150,190,.25)!important}
.home-box{background:radial-gradient(circle at 50% 30%,rgba(45,226,230,.15),transparent 40%),linear-gradient(145deg,#17172B,#0D0D1A);border:2px solid rgba(45,226,230,.65);border-radius:20px;padding:38px 20px;text-align:center;box-shadow:0 0 26px rgba(45,226,230,.12)}
.home-logo{font-family:'Orbitron',monospace;font-size:clamp(2rem,5vw,4rem);font-weight:800;color:#FFD23F;text-shadow:3px 3px 0 #FF4365;line-height:1.2}
.home-tag{color:#BFCBE0;font-size:1.15rem;letter-spacing:.15em}
.motion-track{height:74px;position:relative;overflow:hidden;background:linear-gradient(transparent 47%,#59627A 48%,#59627A 55%,transparent 56%)}
.motion-ball{position:absolute;top:15px;left:0;width:42px;height:42px;border-radius:50%;background:#2DE2E6;border:3px solid #FFD23F;box-shadow:0 0 15px #2DE2E6;animation:moveball 3s linear infinite}
@keyframes moveball{from{transform:translateX(0)}to{transform:translateX(600px)}}
</style>
""",unsafe_allow_html=True)

# ---------------- SESSION / HOME ----------------
if "started" not in st.session_state: st.session_state.started=False
if "sound_on" not in st.session_state: st.session_state.sound_on=True

if not st.session_state.started:
    logo_path=os.path.join(ASSET,"images","arcade_bolt.png")
    if os.path.exists(logo_path):
        a,b,c=st.columns([1,3,1])
        with b: st.image(logo_path,width=110)
    st.markdown('<div class="home-box"><div class="kicker">PLAYER 01 • INSERT COIN</div><br><div class="home-logo">KINETIC ENERGY<br>ARCADE</div><br><div class="home-tag">A RETRO VIRTUAL PHYSICS LAB</div><br><div class="formula">KE = ½ × m × v²</div><br><p>Run experiments • Compare objects • Explore energy in motion</p><p style="color:#FF4365;font-size:24px">✦ ▣ ⚡ ▣ ✦</p></div>',unsafe_allow_html=True)
    x,y,z=st.columns([1,2,1])
    with y:
        if st.button("▶ START GAME",use_container_width=True):
            st.session_state.started=True
            st.rerun()
        st.caption("TEAM: OM • KUSHAL • ISHANI • ATMIKA")
        st.caption("ARCADE START SOUND")
        st.markdown(audio_html("start.wav"), unsafe_allow_html=True)
    st.stop()

with st.sidebar:
    st.markdown("## ⚡ ARCADE MENU")
    page=st.radio("SELECT YOUR MISSION",[
        "🏠 HOME","01 VELOCITY RUN","02 MASS BATTLE","03 GRAPH ZONE",
        "04 COLLISION ARENA","05 ROLLER COASTER"
    ])
    st.divider()
    st.caption("OM • KUSHAL • ISHANI • ATMIKA")
    st.caption("ECS | COMPUTATIONAL PHYSICS")
    st.session_state.sound_on=st.toggle("Sound effects",value=st.session_state.sound_on)
    if st.button("↩ EXIT TO TITLE",use_container_width=True):
        st.session_state.started=False
        st.rerun()

if page=="🏠 HOME":
    st.markdown('<div class="home-box"><div class="home-logo">KINETIC ENERGY ARCADE</div><p>Choose a mission from the left menu.</p></div>',unsafe_allow_html=True)
    st.stop()

st.markdown('<div class="kicker">PLAYER 01 • COMPUTATIONAL PHYSICS • CCE-01</div>',unsafe_allow_html=True)
st.markdown('<div class="arcade-title">⚡ KINETIC ENERGY ARCADE</div>',unsafe_allow_html=True)
st.markdown('<div class="formula">KE = ½ × m × v²</div>',unsafe_allow_html=True)

# ---------------- MISSION 1 ----------------
if page.startswith("01"):
    st.header("VELOCITY RUN")
    st.write("Change velocity and watch the object move faster. Keep mass fixed to explore the v-squared relationship.")
    left,right=st.columns([1,1.2])
    with left:
        mass=st.slider("OBJECT MASS (kg)",1.0,20.0,2.0,.5,key="vel_mass")
        velocity=st.slider("VELOCITY (m/s)",0.0,20.0,5.0,.5,key="vel_v")
        ke=calculate_kinetic_energy(mass,velocity)
        st.markdown(f'<div class="panel"><div class="kicker">ENERGY SCORE</div><div class="score">{ke:.2f} J</div><p>½ × {mass:g} × {velocity:g}²</p></div>',unsafe_allow_html=True)
        if st.session_state.sound_on: st.markdown(audio_html("score.wav"),unsafe_allow_html=True)
    with right:
        duration=max(.7,5.5-velocity*.23)
        play="paused" if velocity==0 else "running"
        st.markdown(f'<div class="panel"><div class="kicker">LIVE MOTION TRACK</div><div class="motion-track"><div class="motion-ball" style="animation-duration:{duration:.2f}s;animation-play-state:{play}"></div></div><p>Speed setting: {velocity:.1f} m/s</p></div>',unsafe_allow_html=True)
        st.plotly_chart(arcade_energy_graph(mass,velocity),use_container_width=True,config={"displayModeBar":False})
    st.success("Physics fact: doubling velocity at constant mass makes kinetic energy four times larger.")

# ---------------- MISSION 2 ----------------
elif page.startswith("02"):
    st.header("MASS BATTLE")
    st.write("Compare two objects travelling at the same speed. The larger visual object represents the greater mass.")
    velocity=st.slider("COMMON VELOCITY (m/s)",0.0,20.0,6.0,.5,key="mass_v")
    ca,cb=st.columns(2)
    with ca: ma=st.slider("OBJECT A MASS (kg)",1.0,20.0,2.0,.5,key="mass_a")
    with cb: mb=st.slider("OBJECT B MASS (kg)",1.0,20.0,8.0,.5,key="mass_b")
    ea,eb=compare_masses(ma,mb,velocity)
    # Relative size is a visual cue only; energy is calculated from exact mass values.
    size_a=28+ma*5; size_b=28+mb*5
    visual=go.Figure()
    visual.add_trace(go.Scatter(x=[1,2],y=[0,0],mode="markers+text",
        text=[f"A • {ma:g} kg",f"B • {mb:g} kg"],textposition="bottom center",
        marker=dict(size=[size_a,size_b],color=["#2DE2E6","#FF4365"],
                    line=dict(color="#FFD23F",width=3)),showlegend=False))
    visual.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0D0D1A",height=270,margin=dict(l=10,r=10,t=20,b=55),
        xaxis=dict(visible=False,range=[0,3]),yaxis=dict(visible=False,range=[-1.3,1.3]))
    st.plotly_chart(visual,use_container_width=True,config={"displayModeBar":False})
    a,b=st.columns(2); a.metric("OBJECT A KINETIC ENERGY",f"{ea:.2f} J"); b.metric("OBJECT B KINETIC ENERGY",f"{eb:.2f} J")
    bars=go.Figure([go.Bar(x=["OBJECT A","OBJECT B"],y=[ea,eb],
        marker_color=["#2DE2E6","#FF4365"],text=[f"{ea:.1f} J",f"{eb:.1f} J"],textposition="outside")])
    bars.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#0D0D1A",
        yaxis_title="KINETIC ENERGY (J)",height=330,margin=dict(l=15,r=15,t=25,b=20))
    st.plotly_chart(bars,use_container_width=True,config={"displayModeBar":False})
    st.info("At the same velocity, kinetic energy is directly proportional to mass. Object size is a visual representation, not a physical scale.")

# ---------------- MISSION 3 ----------------
elif page.startswith("03"):
    st.header("GRAPH ZONE")
    mass=st.slider("MASS (kg)",1.0,20.0,4.0,.5,key="graph_m")
    velocity=st.slider("SELECTED VELOCITY (m/s)",0.0,20.0,8.0,.5,key="graph_v")
    energy=calculate_kinetic_energy(mass,velocity)
    st.metric("SELECTED KINETIC ENERGY",f"{energy:.2f} J")
    st.plotly_chart(arcade_energy_graph(mass,velocity),use_container_width=True,config={"displayModeBar":False})
    st.info("For constant mass, kinetic energy follows a parabolic curve because it depends on velocity squared.")

# ---------------- MISSION 4 ----------------
elif page.startswith("04"):
    st.header("COLLISION ARENA")
    st.write("Set two objects moving along one straight line. The animation is shown when Object A catches Object B.")
    a,b=st.columns(2)
    with a:
        m1=st.slider("OBJECT A MASS (kg)",1.0,10.0,2.0,.5,key="col_m1")
        u1=st.slider("OBJECT A INITIAL VELOCITY (m/s)",-10.0,10.0,5.0,.5,key="col_u1")
    with b:
        m2=st.slider("OBJECT B MASS (kg)",1.0,10.0,2.0,.5,key="col_m2")
        u2=st.slider("OBJECT B INITIAL VELOCITY (m/s)",-10.0,10.0,0.0,.5,key="col_u2")
    v1,v2=elastic_collision(m1,m2,u1,u2)
    before=calculate_kinetic_energy(m1,u1)+calculate_kinetic_energy(m2,u2)
    after=calculate_kinetic_energy(m1,v1)+calculate_kinetic_energy(m2,v2)
    st.markdown("### ANIMATED COLLISION")
    fig=collision_figure(m1,m2,u1,u2,v1,v2)
    if fig is None:
        st.warning("For this left-to-right visual setup, set Object A's velocity higher than Object B's to see them approach and collide.")
    else:
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    x,y=st.columns(2); x.metric("A FINAL VELOCITY",f"{v1:.2f} m/s"); y.metric("B FINAL VELOCITY",f"{v2:.2f} m/s")
    x,y=st.columns(2); x.metric("TOTAL KE BEFORE",f"{before:.2f} J"); y.metric("TOTAL KE AFTER",f"{after:.2f} J")
    st.caption(f"Energy difference due to numerical rounding: {abs(before-after):.10f} J")
    st.info("For an ideal perfectly elastic collision, total momentum and total kinetic energy are conserved.")
    st.caption("COLLISION SOUND EFFECT")
    if st.session_state.sound_on:
        st.markdown(audio_html("collision.wav"), unsafe_allow_html=True)

# ---------------- MISSION 5 ----------------
elif page.startswith("05"):
    st.header("ROLLER COASTER ENERGY RIDE")
    st.write("Move the coaster along the track and observe how gravitational potential energy changes into kinetic energy.")
    mass=st.slider("COASTER MASS (kg)",10.0,100.0,50.0,5.0,key="coaster_m")
    start_height=st.slider("STARTING HEIGHT (m)",10.0,60.0,40.0,1.0,key="coaster_h")
    progress=st.slider("COASTER POSITION (%)",0,100,40,1,key="coaster_progress")
    # A simple hill profile: starts high, descends to a valley, then climbs a smaller hill.
    p=progress/100
    height=start_height*(1-p) + (start_height*.25)*(math.sin(math.pi*p)**2)
    height=max(0.0,height)
    total=calculate_potential_energy(mass,start_height)
    pe=calculate_potential_energy(mass,height)
    ke=max(0.0,total-pe)
    speed=math.sqrt(2*ke/mass) if mass>0 else 0
    xs=np.linspace(0,100,201)
    ys=[start_height*(1-x/100)+(start_height*.25)*(math.sin(math.pi*x/100)**2) for x in xs]
    track=go.Figure()
    track.add_trace(go.Scatter(x=xs,y=ys,mode="lines",line=dict(color="#2DE2E6",width=5),
        fill="tozeroy",fillcolor="rgba(45,226,230,.10)",name="TRACK"))
    track.add_trace(go.Scatter(x=[progress],y=[height],mode="markers+text",
        text=["COASTER"],textposition="top center",
        marker=dict(size=22,color="#FF4365",line=dict(color="#FFD23F",width=3)),showlegend=False))
    track.update_layout(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#0D0D1A",
        xaxis_title="TRACK POSITION (%)",yaxis_title="HEIGHT (m)",height=330,
        margin=dict(l=15,r=15,t=20,b=20),xaxis=dict(gridcolor="rgba(255,255,255,.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,.08)"))
    st.plotly_chart(track,use_container_width=True,config={"displayModeBar":False})
    x,y,z=st.columns(3)
    x.metric("POTENTIAL ENERGY",f"{pe:.1f} J")
    y.metric("KINETIC ENERGY",f"{ke:.1f} J")
    z.metric("SPEED",f"{speed:.2f} m/s")
    st.metric("TOTAL MECHANICAL ENERGY",f"{pe+ke:.1f} J")
    st.info("Model assumption: friction and air resistance are ignored, so total mechanical energy remains constant. The coaster starts from rest.")

st.divider()
st.caption("KINETIC ENERGY ARCADE • PYTHON FUNCTIONS • COMPUTATIONAL PHYSICS")
