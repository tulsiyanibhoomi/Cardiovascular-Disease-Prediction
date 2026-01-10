import os
import streamlit as st
import pandas as pd
import joblib
import time
import json
from PIL import Image


# PAGE CONFIG
st.set_page_config(
    page_title="CardioCare AI",
    page_icon="❤️",
    layout="wide"
)

# SESSION STATE INIT
if 'current_page' not in st.session_state:
    st.session_state.current_page = "DASHBOARD"
if 'theme' not in st.session_state:
    st.session_state.theme = "light"
if 'title' not in st.session_state:
    st.session_state.title = "DASHBOARD"

def nav_to(page_name):
    st.session_state.current_page = page_name
    st.session_state.close_sidebar_flag = True
    st.session_state.title = page_name

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
    st.session_state.close_sidebar_flag = True

# SIDEBAR CLOSE LOGIC
if st.session_state.get("close_sidebar_flag", False):
    js = """
    <script>
        function collapseSidebar() {
            try {
                const doc = window.parent ? window.parent.document : window.document;
                doc.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', code: 'Escape', keyCode: 27, which: 27, bubbles: true}));
            } catch (e) {
                console.log(e);
            }
        }

        collapseSidebar();
        setTimeout(collapseSidebar, 100);
        setTimeout(collapseSidebar, 300);
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)
    st.session_state.close_sidebar_flag = False

# THEME ENGINE CSS
theme_css = {
    "light": {
        "bg": "radial-gradient(at 0% 0%, rgba(0, 200, 255, 0.1) 0, transparent 50%), radial-gradient(at 100% 100%, rgba(255, 50, 200, 0.1) 0, transparent 50%), #fdf6f0",
        "text": "#1a1a2e",
        "card_bg": "rgba(255, 255, 255, 0.95)",
        "card_border": "rgba(255, 100, 220, 0.3)",
        "nav_bg": "rgba(255, 255, 255, 0.95)",
        "sub_text": "#5a5a6f",
        "accent": "#ff77cc",
        "accent_vibrant": "#ff77cc",
        "accent_shadow": "0 0 12px rgba(0, 255, 255, 0.25)",
        "metric_bg": "rgba(255, 119, 204, 0.08)",
        "input_bg": "#f0f4ff",
        "title_gradient": "linear-gradient(to right, #1a1a2e 40%, var(--accent) 100%)"
    }
}


t = theme_css[st.session_state.theme]

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800&display=swap');

    :root {{
        --bg-primary: {t['bg']};
        --text-primary: {t['text']};
        --card-bg: {t['card_bg']};
        --card-border: {t['card_border']};
        --nav-bg: {t['nav_bg']};
        --sub-text: {t['sub_text']};
        --accent: {t['accent']};
        --accent-vibrant: {t['accent_vibrant']};
        --metric-bg: {t['metric_bg']};
        --input-bg: {t.get('input_bg', 'rgba(255,255,255,0.05)')};
        --title-gradient: {t['title_gradient']};
    }}

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    .stApp {{
        background: var(--bg-primary);
        background-attachment: fixed;
        color: var(--text-primary);
    }}

    [data-testid="stHeader"] {{ display: none !important; }}
    
    @media (min-width: 992px) {{
        section[data-testid="stSidebar"] {{ display: none !important; }}
        [data-testid="stHeader"] {{ display: none !important; }}
    }}
    
    @media (max-width: 991px) {{
        [data-testid="stHeader"] {{ 
            display: block !important; 
            background: transparent !important;
        }}
        
        section[data-testid="stSidebar"] {{ 
            background-color: var(--nav-bg) !important;
            border-right: 1px solid var(--card-border);
        }}
        
        [data-testid="stHorizontalBlock"]:has(.stButton) {{
            display: none !important;
        }}
        
        .app-title {{ font-size: 3rem !important; }}
        .main .block-container {{ padding-top: 3rem !important; }}
    }}
    
    .main .block-container {{ 
        padding-top: 0 !important; 
        padding-bottom: 5rem !important;
        max-width: 1400px; 
        margin: 0 auto; 
    }}

    [data-testid="stVerticalBlock"] > div:has(div.stButton) {{
        position: relative;
        z-index: 1000;
        background: transparent !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
        border-bottom: none !important;
        padding: 1.5rem 0;
        margin-top: 0 !important;
        margin-bottom: 2rem;
        box-shadow: none !important;
        display: flex;
        justify-content: center;
    }}

    [data-testid="stHorizontalBlock"] {{
        gap: 0.5rem !important;
        align-items: center;
        max-width: 1350px;
        margin: 0 auto;
        padding-bottom: 0.8rem !important;
    }}

    div.stButton > button {{
        background: var(--card-bg) !important;
        color: var(--sub-text) !important;
        border: 1px solid var(--card-border) !important;
        padding: 0 1.8rem !important;
        height: 44px !important;
        border-radius: 50px !important;
        font-weight: 800 !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
        font-size: 0.72rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12) !important;
        position: relative;
        overflow: hidden;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    /* Target the LAST button in the horizontal block (Theme Change) */
    [data-testid="stHorizontalBlock"] > div:nth-child(6) button {{
        background: transparent !important;
        border: 1px solid var(--accent-vibrant) !important;
        color: var(--accent-vibrant) !important;
        box-shadow: none !important;
    }}
    
    [data-testid="stHorizontalBlock"] > div:nth-child(6) button:hover {{
        background: var(--accent-vibrant) !important;
        color: {('#000000' if st.session_state.theme == 'dark' else '#ffffff')} !important;
        box-shadow: 0 0 20px var(--accent-vibrant) !important;
        transform: translateY(-2px) !important;
    }}

    div.stButton > button::after {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to bottom, rgba(255,255,255,0.1), transparent);
        opacity: 0;
        transition: opacity 0.3s;
    }}


    div.stButton > button:hover {{
        color: var(--accent-vibrant) !important;
        border-color: var(--accent-vibrant) !important;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
    }}

    div.stButton > button:hover::after {{
        opacity: 1;
    }}

    div.stButton > button:active {{
        transform: translateY(1px);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
    }}

    div.stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-vibrant) 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 10px 30px -5px rgba(6, 182, 212, 0.5) !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}


    div.stButton > button[kind="primary"]::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 50%;
        background: rgba(255, 255, 255, 0.1);
        pointer-events: none;
    }}

    div.stButton > button[kind="primary"]:hover {{
        box-shadow: 0 15px 40px -5px rgba(6, 182, 212, 0.7) !important;
        filter: brightness(1.1);
    }}

    /* --- CARD SYSTEM --- */
    .card {{
        background: var(--card-bg);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid var(--card-border);
        border-radius: 40px;
        padding: 3.5rem;
        box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 0.4);
        margin-bottom: 4rem;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }}

    .card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 6px;
        background: linear-gradient(90deg, var(--accent), var(--accent-vibrant));
        opacity: 0.8;
    }}

    .card:hover {{
        border-color: var(--accent-vibrant);
        transform: translateY(-3px);
        box-shadow: 0 50px 120px -30px rgba(0, 0, 0, 0.5);
    }}

    .app-title {{
        text-align: center;
        font-size: 5rem;
        font-weight: 900;
        letter-spacing: -0.05em;
        font-family: 'Outfit', sans-serif;
        background: var(--title-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 0.95;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }}

    .app-subtitle-premium {{
        text-align: center;
        color: var(--premium-color);
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.4em;
        margin-bottom: 3rem;
        opacity: 0.9;
    }}


    .metric-card-new {{
        display: flex;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        margin: 10px 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        background: #fff;
    }}

    .metric-card-new:hover {{
        transform: translateY(-6px);
        box-shadow: 0 12px 28px rgba(0,0,0,0.15);
    }}

    .metric-left {{
        width: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        color: #fff;
    }}

    .metric-right {{
        padding: 1rem 1.5rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.3rem;
    }}

    .metric-label {{
        font-size: 0.75rem;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }}

    .divider {{
        height: 1px;
        background: linear-gradient(to right, transparent, var(--accent), transparent);
        opacity: 0.2;
        margin: 5rem 0;
    }}

    .stNumberInput input, .stSelectbox [data-baseweb="select"] {{
        background: var(--input-bg) !important;
        color: var(--text-primary) !important;
        border-radius: 16px !important;
        border: 2px solid var(--card-border) !important;
        padding: 0.6rem !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    .stNumberInput input:focus, .stSelectbox [data-baseweb="select"]:focus-within {{
        border-color: var(--accent-vibrant) !important;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.3) !important;
        background: var(--card-bg) !important;
        transform: scale(1.01);
    }}
    
    label p {{
        font-size: 0.8rem !important;
        font-weight: 800 !important;
        color: var(--text-primary) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin-bottom: 0.5rem !important;
    }}
    .disclaimer-box {{
        background: rgba(124, 58, 237, 0.1);
        border-left: 5px solid var(--accent-vibrant);
        padding: 1.8rem;
        border-radius: 0 20px 20px 0;
        margin-top: 2.5rem;
        font-size: 0.85rem;
        color: var(--sub-text);
        line-height: 1.8;
    }}

    div.stFormSubmitButton > button {{
        background: linear-gradient(135deg, #ff69b4, #ff1493) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.7rem 2.2rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.25) !important;
        transition: all 0.3s ease;
    }}

    div.stFormSubmitButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.3) !important;
    }}


    </style>
    """,
    unsafe_allow_html=True
)

nav_cols = st.columns([1.2,1,1,1,1])

with nav_cols[0]:
    st.markdown("""
    <div style="
        color: var(--accent-vibrant);
        max-width: 800px;
        padding: 0px 0px 50px 0px;
    ">
        <h1 style="margin:0; font-family:'Outfit'; font-weight:900; font-size:2rem;">CardioCare AI</h1>
    </div>
    """, unsafe_allow_html=True)

with nav_cols[1]:
    if st.button("DASHBOARD", use_container_width=True,
                 type="primary" if st.session_state.current_page == "DASHBOARD" else "secondary"):
        nav_to("DASHBOARD")
        st.rerun()

with nav_cols[2]:
    if st.button("PREDICTION", use_container_width=True,
                 type="primary" if st.session_state.current_page == "PREDICTION" else "secondary"):
        nav_to("PREDICTION")
        st.rerun()

with nav_cols[3]:
    if st.button("ANALYTICS", use_container_width=True,
                 type="primary" if st.session_state.current_page == "ANALYSIS" else "secondary"):
        nav_to("ANALYSIS")
        st.rerun()

with nav_cols[4]:
    if st.button("DISCLAIMER", use_container_width=True,
                 type="primary" if st.session_state.current_page == "DISCLAIMER" else "secondary"):
        nav_to("DISCLAIMER")
        st.rerun()

st.markdown(
    """
    <style>
    /* Hidden by default */
    #mobile-app-name {
        display: none;
        text-align: center;
        font-weight: bold;
        font-size: 3rem;
        margin-bottom:2rem;
        color: var(--accent);
        padding: 0.5rem 0;
    }

    /* Show only on screens smaller than 768px (mobile/tablet) */
    @media screen and (max-width: 992px) {
        #mobile-app-name {
            display: block;
        }
    }
    </style>

    <div id="mobile-app-name">CardioCare AI</div>
    """,
    unsafe_allow_html=True
)

# MOBILE SIDEBAR
with st.sidebar:
    st.markdown(
        f'<div style="text-align:center; padding: 1rem 0 1.5rem 0;">'
        f'<h2 style="color:{t["accent_vibrant"]}; font-family:\'Outfit\'; margin:0; font-weight:700; font-size:1.5rem;">Menu</h2></div>',
        unsafe_allow_html=True
    )

    sidebar_pages = {
        "DASHBOARD": "Dashboard",
        "PREDICTION": "Prediction",
        "ANALYSIS": "Analytics",
        "DISCLAIMER": "Disclaimer"
    }

    for i, (key, label) in enumerate(sidebar_pages.items()):
        active = st.session_state.current_page.lower() == key
        if st.button(
            label.lower(),
            key=f"sidebar_btn_{i}_{key}",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            nav_to(key.upper())
            st.rerun()

    st.markdown(
        """
        <style>
        div.stButton button {
            text-transform: lowercase !important;
            margin-bottom: 0.4rem !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


if st.session_state.current_page.lower() != "dashboard":
    st.markdown(
        f'<h2 style="text-align:center; color: var(--accent-vibrant); margin-top: -10px;">{st.session_state.current_page}</h2>',
        unsafe_allow_html=True
    )


# MODEL LOADING

@st.cache_resource
def load_model():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "model", "final_model.pkl")
    model = joblib.load(model_path)

    return model

model = load_model()


# DASHBOARD PAGE

if st.session_state.current_page == "DASHBOARD":

    st.markdown(
        """
        <div style="text-align:center; margin-bottom: 4rem;">
            <p style="color:var(--sub-text); max-width: 850px; margin: 0 auto 0 auto; line-height: 2; font-size: 1.2rem; font-weight: 500;">
                CardioCare AI uses advanced technology to monitor your heart health. We turn your health data into clear, actionable insights so you can care for your heart with confidence.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
    if st.button("CHECK MY HEART HEALTH", type="primary"):
        nav_to("PREDICTION")
        st.rerun()

    insight_cols = st.columns(4)

    with insight_cols[0]:
        st.markdown("""
        <div class="metric-card-new">
            <div class="metric-left" style="background:#7c3aed;">💊</div>
            <div class="metric-right">
                <div class="metric-value">70K+</div>
                <div class="metric-label">Patient Records</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with insight_cols[1]:
        st.markdown("""
        <div class="metric-card-new">
            <div class="metric-left" style="background:#10b981;">🧬</div>
            <div class="metric-right">
                <div class="metric-value">11</div>
                <div class="metric-label">Health Factors</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with insight_cols[2]:
        st.markdown("""
        <div class="metric-card-new">
            <div class="metric-left" style="background:#f59e0b;">📈</div>
            <div class="metric-right">
                <div class="metric-value">73%</div>
                <div class="metric-label">Accuracy</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with insight_cols[3]:
        st.markdown("""
        <div class="metric-card-new">
            <div class="metric-left" style="background:#ef4444;">🎯</div>
            <div class="metric-right">
                <div class="metric-value">0.71</div>
                <div class="metric-label">Precision</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# PREDICTION PAGE

elif st.session_state.current_page == "PREDICTION":
    st.markdown('<div class="app-subtitle-premium">Check Your Heart Health Score</div>', unsafe_allow_html=True)


    with st.form(key="prediction_form"):
        
        cols = st.columns([0.3, 0.8, 0.1, 0.8, 0.3])
        with cols[1]:
            st.markdown('<div style="margin-top: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)
            age = st.number_input("Age (years) *", min_value=18, max_value=120, step=1)
        with cols[3]:
            st.markdown('<div style="margin-top: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)
            gender = st.radio("Gender *", ["Female", "Male"], index=1, horizontal=True)

        cols = st.columns([0.3, 0.8, 0.1, 0.8, 0.3])
        with cols[1]:
            st.markdown('<div style="margin-top: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)
            height = st.number_input("Height (cm) *", min_value=90, max_value=240)
        with cols[3]:
            st.markdown('<div style="margin-top: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)    
            weight = st.number_input("Weight (kg) *", min_value=30.0, max_value=220.0, step=0.1)

        cols = st.columns([0.3, 0.8, 0.1, 0.8, 0.3])
        with cols[1]:
            st.markdown('<div style="margin-top: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)    
            ap_hi = st.number_input("Systolic BP (mmHg) *", min_value=80, max_value=240)
        with cols[3]:
            st.markdown('<div style="margin-top: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)    
            ap_lo = st.number_input("Diastolic BP (mmHg) *", min_value=40, max_value=200)

        cols= st.columns([0.3, 0.8, 0.1, 0.8, 0.3])
        with cols[1]:
            st.markdown('<div style="margin-top: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)    
            cholesterol = st.selectbox("Cholesterol *", ["Normal (<200 mg/dL)", "Above Normal (200-239 mg/dL)", "Well Above Normal (>=240 mg/dL)"])
        with cols[3]:
            st.markdown('<div style="margin-top: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)    
            gluc = st.selectbox("Glucose *", ["Normal (<100 mg/dL)", "Above Normal (100-125 mg/dL)", "Well Above Normal (>=126 mg/dL)"])

        cols = st.columns([0.3, 0.5, 0.1, 0.5, 0.1, 0.5, 0.3])
        st.markdown(
        """
        <style>
            div[data-testid="stRadio"] > div {
                justify-content: center;
            }
            label[data-testid="stWidgetLabel"] {
                text-align: center;
                width: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        with cols[1]:
            st.markdown('<div style="margin-top: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)    
            smoke = st.radio("Do you smoke? *", ["No", "Yes"], horizontal=True)

        with cols[3]:
            st.markdown('<div style="margin-top: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)    
            alco = st.radio("Do you drink alcohol? *", ["No", "Yes"], horizontal=True)

        with cols[5]:
            st.markdown('<div style="margin-top: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)    
            active = st.radio("Are you physically active? *", ["Yes", "No"], horizontal=True)


        submit = st.form_submit_button("Get Prediction")

    st.markdown(
        """
        <style>
            div.stElementContainer.st-key-FormSubmitter-prediction_form-Get-Prediction {
                width: 100% !important;
                display: flex !important;
                justify-content: center !important;
                margin-bottom: 2rem;
            }
            div.stFormSubmitButton {
                display: flex !important;
                justify-content: center !important;
                width: auto !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )   




    cholesterol_map = {
        "Normal (<200 mg/dL)": 1,
        "Above Normal (200-239 mg/dL)": 2,
        "Well Above Normal (>=240 mg/dL)": 3
    }

    gluc_map = {
        "Normal (<100 mg/dL)": 1,
        "Above Normal (100-125 mg/dL)": 2,
        "Well Above Normal (>=126 mg/dL)": 3
    }

    if submit:
        try:
            age_years = int(age)
            gender_val = 1 if gender == "Male" else 0
            height = int(height)
            weight = float(weight)
            ap_hi = int(ap_hi)
            ap_lo = int(ap_lo)
            cholesterol_val = cholesterol_map[cholesterol]
            gluc_val = gluc_map[gluc]
            smoke_val = 1 if smoke == "Yes" else 0
            alco_val = 1 if alco == "Yes" else 0
            active_val = 1 if active == "Yes" else 0

            if ap_lo >= ap_hi:
                st.warning("⚠️ Diastolic BP (ap_lo) should be **less than** Systolic BP (ap_hi). Please correct the values.")
            else:

                bmi = weight / ((height / 100) ** 2)
                pulse_pressure = ap_hi - ap_lo
                cholesterol_gluc_interaction = cholesterol_val * gluc_val

                chol_2 = 1 if cholesterol_val == 2 else 0
                chol_3 = 1 if cholesterol_val == 3 else 0
                gluc_2 = 1 if gluc_val == 2 else 0
                gluc_3 = 1 if gluc_val == 3 else 0

                columns = [
                    "age_years", "gender", "BMI", "ap_hi", "ap_lo",
                    "pulse_pressure", "cholesterol_gluc_interaction",
                    "smoke", "alco", "active",
                    "chol_2", "chol_3", "gluc_2", "gluc_3"
                ]

                input_features = [
                    age_years, gender_val, bmi, ap_hi, ap_lo,
                    pulse_pressure, cholesterol_gluc_interaction,
                    smoke_val, alco_val, active_val,
                    chol_2, chol_3, gluc_2, gluc_3
                ]

                input_df = pd.DataFrame([input_features], columns=columns)
                probability = model.predict_proba(input_df)[0][1] * 100

                risk_label = "HIGH RISK" if probability >= 50 else "LOW RISK"
                risk_color = "#ef4444" if probability >= 50 else "#10b981"

                st.markdown("""
                    <div style="
                        text-align: center; 
                        color: #00CED1;
                        font-size: 2rem; 
                        font-weight: 800;
                        font-family: 'Plus Jakarta Sans', sans-serif;
                        margin-top: 2rem;
                        margin-bottom: 1rem;
                    ">
                        Your Health Report
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(
                    f"""
                <div style="
                    display: flex; 
                    flex-direction: column; 
                    align-items: center; 
                    justify-content: center; 
                    padding: 3rem 0;
                    background-color: {risk_color}20;
                    border-radius: 15px;
                ">
                    <div style="text-align: center;">
                        <p style="color: var(--sub-text); font-weight: 700; margin-top: 0.5rem; font-size: 1rem;">
                            Prediction Assessment
                        </p>
                        <span style="
                            font-size: 5rem; 
                            font-weight: 900; 
                            color: {risk_color}; 
                            font-family: 'Outfit'; 
                            line-height: 1; 
                            text-shadow: 0 0 30px {risk_color}40;
                        ">
                            {risk_label}
                        </span>
                        <p style="
                            margin-top: 1rem; 
                            font-size: 1.25rem; 
                            font-weight: 600; 
                            color: {risk_color}; 
                            font-family: 'Outfit';
                        ">
                            Heart disease risk: {probability:.2f}%
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
                )

                st.markdown(
                    """
                    <div style="
                        background:#FFF4E5;
                        padding:10px 15px;
                        border-left: 4px solid #FFA500;
                        border-radius:8px;
                        font-size:13px;
                        color:#3E3E3E;
                        margin-top:1rem;
                    ">
                    ⚠️ <b>Disclaimer:</b> This is an estimate based on the data provided. It is <b>not a medical diagnosis</b>. 
                    Always consult a healthcare professional for personalized advice.
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                advice_list = []

                if smoke_val == 1:
                    advice_list.append("🚭 Quit Smoking: Your heart will thank you in the long run. Consider professional help or support groups.")
                if alco_val == 1:
                    advice_list.append("🍷 Reduce Alcohol: Limit drinks to lower blood pressure and reduce heart strain.")
                if active_val == 0:
                    advice_list.append("🏃‍♂️ Stay Active: Aim for at least 30 minutes of walking or light exercise daily.")
                if bmi > 25:
                    advice_list.append("⚖️ Maintain Healthy Weight: Focus on balanced diet and exercise to reduce cardiovascular risk.")
                if ap_hi > 130 or ap_lo > 80:
                    advice_list.append("💓 Monitor Blood Pressure: Check regularly and consult a doctor if numbers remain high.")
                if cholesterol_val > 1:
                    advice_list.append("🥗 Heart-Friendly Diet: Reduce fried foods and include healthy fats like olive oil and nuts.")
                if gluc_val > 1:
                    advice_list.append("🍬 Control Sugar Intake: High sugar levels can harm blood vessels and heart health.")

                st.markdown("<h4 style='color:#FF6B6B; margin-top: 3rem; margin-bottom: 0.5rem;'>💡 Your Heart Health Insights</h4>", unsafe_allow_html=True)

                if advice_list:
                    for item in advice_list:
                        st.markdown(
                            f"""
                            <div style="
                                background: linear-gradient(135deg, #FFE3E3, #FFD6D6);
                                padding: 12px 18px;
                                border-radius: 12px;
                                margin-bottom: 8px;
                                border-left: 5px solid #FF6B6B;
                                font-size: 15px;
                                color: #2E2E2E;
                                ">
                                {item}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown(
                            """
                            <div style="
                                background: linear-gradient(135deg, #E0FFE0, #CCFFD6);
                                padding: 12px 18px;
                                border-radius: 12px;
                                margin-bottom: 12px;
                                border-left: 5px solid #10B981;
                                font-size: 15px;
                                color: #2E2E2E;
                                margin-top:2rem;
                            ">
                            🎉 You're doing great! Keep up your healthy lifestyle!
                            </div>
                            """,
                            unsafe_allow_html=True
                    )

                notif = st.empty()
                notif.markdown("""
                    <div style="position: fixed; top: 20px; right: 20px; background-color: #10B981; color: white; padding: 12px 18px; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0,0,0,0.2); z-index: 1000; font-weight: 600;">
                        📢 Your health assessment is ready. See your detailed results below.    
                    </div>
                """, unsafe_allow_html=True)

                time.sleep(3)
                notif.empty()    

            
        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")


# ANALYTICS PAGE

elif st.session_state.current_page == "ANALYSIS":

    with open("assets/model_all_data.json") as f:
        model_data = json.load(f)

    metrics = model_data['metrics']
    train_test = model_data['trainTestAccuracy']

    st.markdown('<p style="color:var(--sub-text); text-align:center; font-size:0.95rem;">A comprehensive view of your heart health prediction using our Smart Engine model.</p>', unsafe_allow_html=True)


    with st.container():
        st.markdown("### 🩺 Risk Levels")
        st.markdown("""
        - 🟢 **Low Risk (0-30%)** - Heart health looks good.
        - 🟡 **Medium Risk (30-60%)** - Some risk factors detected, monitor closely.
        - 🔴 **High Risk (60%+)** - Strongly consider consulting a doctor.
        """)
        st.info("These risk levels are based on patterns learned from 70,000+ records and validated metrics.")

    algorithms = model_data["algorithms"]

    best_model = max(algorithms, key=algorithms.get)
    best_acc = algorithms[best_model]

    model_info = {
        "Gradient Boosting": "An ensemble method that combines weak learners sequentially to reduce errors. High accuracy and robust to overfitting.",
        "XGBoost": "Extreme Gradient Boosting. Optimized boosting method with regularization. Fast and accurate.",
        "Random Forest": "Ensemble of decision trees. Reduces overfitting compared to a single tree.",
        "Decision Tree": "Simple interpretable tree model. Can overfit on small datasets.",
        "Logistic Regression": "Linear model for binary classification. Easy to interpret, good baseline.",
        "Naive Bayes": "Probabilistic classifier based on Bayes theorem. Fast but assumes feature independence.",
        "K Nearest Neighbors": "Instance-based model. Predicts based on nearest neighbors. Sensitive to data scaling."
    }

    with st.container():
        st.markdown(f"### 🧠 Model Used: {best_model}")
        st.markdown(
            f"<p style='color:var(--sub-text); font-size:0.9rem;'>"
            f"Our Smart Engine uses **{best_model}** with accuracy of **{best_acc:.2f}%**. "
            f"{model_info.get(best_model, '')}</p>",
            unsafe_allow_html=True
        )

    st.markdown("### 🔹 Model Comparison")
    max_cols = 3
    model_items = list(algorithms.items())
    for i in range(0, len(model_items), max_cols):
        cols = st.columns(min(max_cols, len(model_items) - i))
        for col, (model, acc) in zip(cols, model_items[i:i+max_cols]):
            info_text = model_info.get(model, "")
            bg_color = "#d1f0d1" if model == best_model else "#e0e0e0"
            with col:
                st.markdown(
                    f"""
                    <div style="
                        background-color: {bg_color};
                        border-radius: 12px;
                        padding: 1rem;
                        text-align: center;
                        min-height: 200px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
                        word-wrap: break-word;
                    ">
                        <h4 style='margin:0'>{model}</h4>
                        <p style='font-size:1.2rem; font-weight:bold; margin:0'>{acc:.2f}%</p>
                        <small style='color:gray'>{info_text}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    with st.container():
        st.markdown("### 📈 Model Performance Metrics")
        st.markdown(
            "<p style='color:var(--sub-text); font-size:0.9rem;'>Overall evaluation of the heart risk prediction model.</p>",
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        for col, metric, value, help_text in zip(
            [col1, col2, col3, col4],
            ["🎯 Accuracy", "🔍 Precision", "📌 Recall", "📈 ROC AUC"],
            [metrics['accuracy'], metrics['precision'], metrics['recall'], metrics['rocAuc']],
            [
                "Overall correctness of the model",
                "How many predicted risks were actually correct",
                "How many actual risk cases were detected",
                "Model's ability to distinguish between low & high risk"
            ]
        ):
            with col:
                st.markdown(
                    f"""
                    <div style="
                        background-color:#f5f5f5;
                        border-radius:12px;
                        padding:1rem;
                        text-align:center;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
                    ">
                        <h4 style='margin:0'>{metric}</h4>
                        <p style='font-size:1.5rem; font-weight:bold; margin:0'>{value*100:.2f}%</p>
                        <small style='color:gray'>{help_text}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown(
            f"<p style='color:var(--sub-text); margin-top:1.5rem; font-size:0.9rem;'>Training Accuracy: {train_test['train']}%</p>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<p style='color:var(--sub-text); font-size:0.9rem;'>Test Accuracy: {train_test['test']}%</p>",
            unsafe_allow_html=True
        )



    st.markdown("### 🔹 Model Evaluation")
    tabs = st.tabs(["Confusion Matrix", "ROC Curve", "Precision-Recall", "Calibration", "Learning Curve"])
    
    with tabs[0]:
        st.markdown("#### Confusion Matrix")
        st.markdown("This matrix shows how many predictions were correct and where errors occurred:")
        st.markdown("""
        - **True Negative (TN):** Correctly predicted no heart risk.
        - **False Positive (FP):** Incorrectly predicted risk when there was none.
        - **False Negative (FN):** Missed predicting risk.
        - **True Positive (TP):** Correctly predicted heart risk.
        """)
        conf_img = Image.open("assets/confusion_matrix.png")
        st.image(conf_img, width=500)

    with tabs[1]:
        st.markdown("#### ROC Curve")
        st.markdown("The ROC curve shows the trade-off between **true positive rate** and **false positive rate**. A higher area under the curve (AUC = {:.2f}) indicates better discrimination between low and high risk.".format(metrics['rocAuc']))
        roc_img = Image.open("assets/roc_curve.png")
        st.image(roc_img, width=500)

    with tabs[2]:
        st.markdown("#### Precision-Recall Curve")
        st.markdown("This curve evaluates the balance between **precision** (how many predicted risks are correct) and **recall** (how many actual risks are detected).")
        pr_img = Image.open("assets/precision_recall_curve.png")
        st.image(pr_img, width=500)

    with tabs[3]:
        st.markdown("#### Calibration Curve")
        st.markdown("This curve shows how well predicted probabilities reflect actual outcomes. A perfectly calibrated model will align along the diagonal.")
        cal_img = Image.open("assets/calibration_curve.png")
        st.image(cal_img, width=500)

    with tabs[4]:
        st.markdown("#### Learning Curve")
        st.markdown("This curve shows how the model improves with more training data and whether it suffers from underfitting or overfitting.")
        lc_img = Image.open("assets/learning_curve.png")
        st.image(lc_img, width=700)

    with st.container():
        st.markdown("### 🔹 Key Insights")
        st.markdown("""
        - The model is **73% accurate** and well-calibrated for predicting heart risk.
        - Confusion matrix shows the model slightly misses some high-risk cases (False Negatives), but overall balance is strong.
        - Visual analysis confirms the model generalizes well with increasing training data (learning curve).
        """)


# DISCLAIMER PAGE

elif st.session_state.current_page == "DISCLAIMER":

    st.markdown(
        """
        <div style="
            background-color: #fff3cd;
            border-left: 6px solid #ffeeba;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            font-size: 0.95rem;
            color: #856404;
        ">
            <p>
            The heart risk prediction model is an <strong>AI-powered tool</strong> trained on historical data. 
            It is intended for <strong>informational and educational purposes only</strong> and <strong>does not replace medical advice</strong>.
            </p>
            <p>
            We are <strong>not responsible</strong> for any decisions, diagnoses, or outcomes based on the model’s predictions. 
            Always consult a qualified healthcare professional for medical advice or concerns regarding your heart health.
            </p>
            <p>
            By using this tool, you acknowledge that it provides <strong>probabilistic predictions</strong> based on patterns in the data and may not reflect your personal health status accurately.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "💡 Always seek professional medical evaluation if you have any heart-related concerns. "
        "This tool is only for preliminary insights."
    )