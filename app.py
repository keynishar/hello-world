import html
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.caption("A tiny app-building playground: type a name, style it, and add animated weather or celebration effects.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact", "Comic Sans MS"],
    )
    font_size = st.slider("Font size (px)", min_value=20, max_value=110, value=52, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender", "Midnight"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    speed = st.slider("Animation speed", min_value=0.4, max_value=3.0, value=1.3, step=0.1,
                      help="Lower values move more slowly; higher values move more quickly.")
    density = st.slider("Effect density", min_value=8, max_value=70, value=32, step=2)

backgrounds = {
    "Light": ("#f8fafc", "#172033"),
    "Dark": ("#10131a", "#f8fafc"),
    "Ocean": ("linear-gradient(135deg, #005f73, #0a9396, #94d2bd)", "#ffffff"),
    "Sunset": ("linear-gradient(135deg, #ff7e5f, #feb47b, #7b2ff7)", "#ffffff"),
    "Forest": ("linear-gradient(135deg, #163a2b, #387a52, #b7d7a8)", "#ffffff"),
    "Lavender": ("linear-gradient(135deg, #eee7ff, #d7c6ff, #fce7f3)", "#34244f"),
    "Midnight": ("linear-gradient(135deg, #090a2a, #172554, #312e81)", "#ffffff"),
}
bg, text_color = backgrounds[background]
safe_name = html.escape(name or "Hello World")
safe_font = font_family.replace("'", "").replace('"', "")

# The animation runs inside the embedded browser component using CSS. It does not
# continuously rerun the whole Streamlit script, so the controls remain responsive.
effect_config = {
    "None": ("", ""),
    "Rain": ("💧", "rain"),
    "Snow": ("❄", "snow"),
    "Hail": ("●", "hail"),
    "Wind Gust": ("〰", "wind"),
    "Confetti": ("🎉", "confetti"),
    "Tornado": ("🌪", "tornado"),
}
symbol, effect_class = effect_config[effect]

particles = ""
if effect != "None":
    # Deterministic varied positions and delays are enough; CSS loops forever.
    import random
    rng = random.Random(2026)
    particle_items = []
    for i in range(density):
        left = rng.randint(1, 99)
        delay = rng.uniform(-8.0, 0.0)
        duration = rng.uniform(2.2, 6.5) / speed
        size = rng.randint(12, 28) if effect in ("Confetti", "Snow") else rng.randint(10, 20)
        drift = rng.randint(-100, 100)
        rotation = rng.randint(0, 720)
        particle_items.append(
            f'<span class="particle {effect_class}" style="left:{left}%;'
            f'animation-delay:{delay:.2f}s;animation-duration:{duration:.2f}s;'
            f'font-size:{size}px;--drift:{drift}px;--rotation:{rotation}deg;">{symbol}</span>'
        )
    particles = "".join(particle_items)

if name_mode == "Ticker Tape":
    name_markup = f'<div class="ticker"><span>{safe_name}</span><span aria-hidden="true">{safe_name}</span></div>'
elif name_mode == "Repeated":
    name_markup = '<div class="repeated">' + "".join(f"<div>{safe_name}</div>" for _ in range(6)) + "</div>"
else:
    name_markup = f'<div class="center-name">{safe_name}</div>'

ticker_css = """
.ticker { display:flex; width:max-content; gap:3rem; white-space:nowrap; animation: marquee 12s linear infinite; }
.ticker span { flex:0 0 auto; }
@keyframes marquee { from { transform:translateX(100%); } to { transform:translateX(-100%); } }
""" if name_mode == "Ticker Tape" else ""

html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing:border-box; }}
html, body {{ margin:0; width:100%; height:100%; }}
.stage {{
  position:relative; width:100%; height:620px; overflow:hidden; border-radius:18px;
  background:{bg}; color:{text_color}; font-family:'{safe_font}', sans-serif;
  display:flex; align-items:center; justify-content:center; isolation:isolate;
}}
.effects {{ position:absolute; inset:0; overflow:hidden; pointer-events:none; z-index:1; }}
.particle {{ position:absolute; top:-12%; display:block; opacity:.85; user-select:none;
  animation-iteration-count:infinite; animation-timing-function:linear; will-change:transform; }}
.rain {{ color:#55b8ff; text-shadow:0 0 5px #55b8ff; animation-name:fall-rain; }}
.hail {{ color:#d9f3ff; text-shadow:0 0 5px #b8e7ff; animation-name:fall-hail; }}
.snow {{ color:#fff; text-shadow:0 0 8px #8bdcff; animation-name:fall-snow; }}
.confetti {{ animation-name:fall-confetti; }}
.wind {{ color:rgba(255,255,255,.9); animation-name:blow-wind; }}
.tornado {{ animation-name:spin-tornado; }}
@keyframes fall-rain {{ from {{ transform:translate3d(0,-10vh,0) rotate(15deg); }} to {{ transform:translate3d(calc(var(--drift)*.15),115vh,0) rotate(15deg); }} }}
@keyframes fall-hail {{ from {{ transform:translate3d(0,-10vh,0); }} to {{ transform:translate3d(calc(var(--drift)*.25),115vh,0); }} }}
@keyframes fall-snow {{ 0% {{ transform:translate3d(0,-10vh,0) rotate(0); }} 50% {{ transform:translate3d(calc(var(--drift)*.5),50vh,0) rotate(180deg); }} 100% {{ transform:translate3d(0,115vh,0) rotate(360deg); }} }}
@keyframes fall-confetti {{ 0% {{ transform:translate3d(0,-10vh,0) rotate(0); }} 100% {{ transform:translate3d(var(--drift),115vh,0) rotate(var(--rotation)); }} }}
@keyframes blow-wind {{ 0% {{ transform:translate3d(-20vw,0,0) scaleX(.7); opacity:0; }} 20% {{opacity:.8}} 100% {{ transform:translate3d(120vw,25vh,0) scaleX(1.5); opacity:0; }} }}
@keyframes spin-tornado {{ 0% {{ transform:translate3d(0,-10vh,0) rotate(0) scale(.6); }} 50% {{ transform:translate3d(var(--drift),50vh,0) rotate(360deg) scale(1.2); }} 100% {{ transform:translate3d(0,115vh,0) rotate(720deg) scale(.6); }} }}
.name-layer {{ position:relative; z-index:2; width:100%; padding:24px; font-size:{font_size}px;
  font-weight:700; text-align:center; overflow:hidden; text-shadow:0 2px 12px rgba(0,0,0,.16); }}
.center-name {{ overflow-wrap:anywhere; }}
.repeated {{ display:flex; flex-direction:column; align-items:center; gap:.2em; line-height:1.05; overflow-wrap:anywhere; }}
{ticker_css}
.hint {{ position:absolute; bottom:14px; right:18px; z-index:3; font:12px Arial,sans-serif; opacity:.7; }}
@media (prefers-reduced-motion: reduce) {{ .particle, .ticker {{ animation-duration:30s !important; }} }}
</style>
</head>
<body>
<div class="stage">
  <div class="effects">{particles}</div>
  <div class="name-layer">{name_markup}</div>
  <div class="hint">Hello World Motion Lab</div>
</div>
</body>
</html>
"""

components.html(html_doc, height=640, scrolling=False)
st.caption("Tip: Change the controls in the sidebar to experiment with fonts, backgrounds, and looping effects.")
