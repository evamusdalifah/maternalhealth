import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# ================= PAGE =================
st.set_page_config(page_title="Maternal Health Dashboard", layout="wide")

# ================= RISK ENCODING =================
RISK_MAP = {
    "low risk":1,
    "mid risk":2,
    "high risk":3
}

INV_RISK_MAP = {v:k for k,v in RISK_MAP.items()}

st.markdown("""
<style>
.metric-card {
    background-color: #111827;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
    transition: 0.3s;
}
.metric-card:hover {
    transform: scale(1.03);
    border: 1px solid rgba(255,255,255,0.15);
}
.metric-title {
    font-size: 14px;
    color: #9ca3af;
}
.metric-value {
    font-size: 28px;
    font-weight: bold;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

sdg_data = {
    "Year":[2010,2020,2030],
    "MMR":[346,189,70],
    "IMR":[26,17,12]
}

sdg_df = pd.DataFrame(sdg_data)

# ================= COLOR MAP =================
COLOR_MAP = {
    "low risk":"#2ecc71",
    "mid risk":"#f39c12",
    "high risk":"#e74c3c"
}

st.markdown("""
<div style="
background:rgba(255,255,255,0.03);
padding:30px;
border-radius:18px;
text-align:center;
border:1px solid rgba(255,255,255,0.08);
backdrop-filter: blur(6px);
margin-bottom:25px;
">
<h1 style="margin:0;font-size:44px;">Maternal Health Dashboard</h1>
<p style="color:#9ca3af;margin-top:8px;">
Interactive dashboard for analyzing maternal health risk and predicting pregnancy risk level
</p>
</div>
""", unsafe_allow_html=True)

# ================= SDG SECTION =================
left, right = st.columns([1.2,1])

# ---------- LEFT : BACKGROUND ----------
with left:
    st.subheader("Background")

    st.markdown("""
Menurut **Utomo (1985)**, kematian atau mortalitas didefinisikan sebagai hilangnya secara permanen seluruh tanda kehidupan setelah kelahiran hidup.

Beberapa indikator mortalitas yang tercatat dalam **Sensus Penduduk 2020 (SP2020)** adalah:

- **Angka Kematian Bayi (AKB)** → jumlah kematian bayi <1 tahun per 1.000 kelahiran.
- **Rasio Kematian Ibu (RKI)** → jumlah kematian ibu akibat komplikasi kehamilan/persalinan per 100.000 kelahiran hidup.

Berdasarkan data Sensus Penduduk 2010, angka kematian ibu (AKI) di Indonesia cukup tinggi, dengan estimasi mencapai sekitar 346 kematian per 100.000 kelahiran hidup. 
Sementara itu, angka kematian bayi (AKB) sekitar tahun 2010 tercatat berkisar 34 per 1.000 kelahiran hidup, yang menunjukkan risiko signifikan bagi kelangsungan hidup bayi baru lahir pada periode tersebut.

Atas hal ini, Perserikatan Bangsa-Bangsa (PBB) menetapkan sustainable Development Goals (SDGs), dengan dua tujuan diantara nya adalah menurunkan angka kematian ibu dan bayi, yang didukung oleh data di sisi kanan.
""")

# ---------- RIGHT : CHART ----------
with right:
    st.subheader("Global Health Targets (SDGs)")

    c1, c2 = st.columns(2)

    with c1:
        fig_mmr = px.bar(sdg_df, x="Year", y="MMR", text="MMR")
        fig_mmr.update_traces(marker_color=["#4c72b0","#4c72b0","#c0392b"])
        fig_mmr.update_layout(font_color="white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_mmr, use_container_width=True)

    with c2:
        fig_imr = px.bar(sdg_df, x="Year", y="IMR", text="IMR")
        fig_imr.update_traces(marker_color=["#4c72b0","#4c72b0","#c0392b"])
        fig_imr.update_layout(font_color="white", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_imr, use_container_width=True)

# ---------- FULL WIDTH PROJECT GOAL ----------
st.markdown("---")

st.subheader("🎯 Tujuan Project")

st.markdown("""
Berdasarkan latar belakang tersebut diatas, project ini dibuat untuk memprediksi tingkat resiko kehamilan berdasarkan data kesehatan
umum menggunakan simulasi dataset Kaggle. Hal ini diharapkan dapat membantu tim medis dalam memberikan perawatan yang lebih tepat kepada ibu hamil sehingga
menghindari tingginya resiko kehamilan.
""")

st.divider()
    
# ================= LOAD DATA =================
df = pd.read_csv("maternal.csv")
model = joblib.load("dt_joblib")

DEBUG = False

if DEBUG:
    st.write(model.feature_names_in_)

# ================= SIDEBAR FILTER =================
st.sidebar.markdown("## 🔎 Filter Data")

# AGE
age_range = st.sidebar.slider(
    "Mother Age",
    int(df.Age.min()),
    int(df.Age.max()),
    (int(df.Age.min()), int(df.Age.max()))
)

# BLOOD SUGAR
bs_range = st.sidebar.slider(
    "Blood Sugar",
    float(df.BS.min()),
    float(df.BS.max()),
    (float(df.BS.min()), float(df.BS.max()))
)

# SYSTOLIC
sys_range = st.sidebar.slider(
    "Systolic BP",
    int(df.SystolicBP.min()),
    int(df.SystolicBP.max()),
    (int(df.SystolicBP.min()), int(df.SystolicBP.max()))
)

# DIASTOLIC
dia_range = st.sidebar.slider(
    "Diastolic BP",
    int(df.DiastolicBP.min()),
    int(df.DiastolicBP.max()),
    (int(df.DiastolicBP.min()), int(df.DiastolicBP.max()))
)

filtered_df = df[
    df.Age.between(age_range[0], age_range[1]) &
    df.BS.between(bs_range[0], bs_range[1]) &
    df.SystolicBP.between(sys_range[0], sys_range[1]) &
    df.DiastolicBP.between(dia_range[0], dia_range[1])
]

if filtered_df.empty:
    st.warning("No data matches selected filters")
    st.stop()

# CONTACT ME
st.sidebar.markdown("---")
st.sidebar.markdown("### 👩‍💻 Contact Me")

st.sidebar.markdown("""
<div style="
background:#0b1a2b;
padding:16px 18px;
border-radius:16px;
line-height:1.4;
">

<h4 style="margin-bottom:4px;">Eva Musdalifah</h4>

<p style="margin:0;color:#9ca3af;font-size:13px;">
Data Analyst • Machine Learning
</p>

<div style="margin:10px 0;">
<span style="
background:#16a34a;
padding:4px 10px;
border-radius:999px;
font-size:12px;
font-weight:600;
">
Available for freelance | Open to work
</span>
</div>

<a href="https://www.linkedin.com/in/evamusdalifah/" target="_blank" style="display:block;margin:6px 0;color:#60a5fa;text-decoration:none;">🔗 Linkedin</a>

<a href="https://github.com/evamusdalifah" target="_blank" style="display:block;margin:6px 0;color:#60a5fa;text-decoration:none;">💻 Github</a>

<a href="mailto:evamusdalifah04@gmail.com" style="display:block;margin:6px 0;color:#60a5fa;text-decoration:none;">📧 Email</a>

<a href="https://wa.me/6285746606551" target="_blank" style="display:block;margin:6px 0;color:#60a5fa;text-decoration:none;">📱 WhatsApp</a>

<a href="https://drive.google.com/file/d/12yUh6Sd9mpoff0tEj_fcflcmFcdAE57q/view?usp=sharing" target="_blank"
style="display:block;margin:6px 0;color:#60a5fa;text-decoration:none;">
📄 View CV
</a>
                                        
</div>
""", unsafe_allow_html=True)

def card(title, value):
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """

def risk_card(title, value, color):
    return f"""
    <div style="
        background:{color};
        padding:20px;
        border-radius:14px;
        text-align:center;
        color:white;
        font-weight:bold;
        box-shadow:0 0 15px {color}55;
    ">
        <div style="font-size:14px;opacity:0.9;">{title}</div>
        <div style="font-size:28px;margin-top:5px;">{value}</div>
    </div>
    """

# ================= KPI =================
st.markdown("<h3 style='text-align:center;'>Summary Statistics</h3>", unsafe_allow_html=True)

left_space, center, right_space = st.columns([0.2,6,0.2])

with center:

    # ===== ROW 1 =====
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

    c1.markdown(card("Total Patients", len(filtered_df)), unsafe_allow_html=True)
    c2.markdown(card("Average Age", round(filtered_df.Age.mean(),1)), unsafe_allow_html=True)
    c3.markdown(card("Average Glucose", round(filtered_df.BS.mean(),1)), unsafe_allow_html=True)
    c4.markdown(card("Avg Systolic BP", round(filtered_df.SystolicBP.mean(),1)), unsafe_allow_html=True)
    c5.markdown(card("Avg Diastolic BP", round(filtered_df.DiastolicBP.mean(),1)), unsafe_allow_html=True)
    c6.markdown(card("Avg Heart Rate", round(filtered_df.HeartRate.mean(),1)), unsafe_allow_html=True)
    c7.markdown(card("Avg Body Temp", round(filtered_df.BodyTemp.mean(),1)), unsafe_allow_html=True)

    # ===== ROW 2 =====
    k8, k9, k10, k11, k12, k13, k14  = st.columns(7)
    
    high_risk_pct = (filtered_df.RiskLevel == "high risk").mean()*100
    mid_pct = (filtered_df.RiskLevel == "mid risk").mean()*100
    low_pct = (filtered_df.RiskLevel == "low risk").mean()*100
    
    k8.markdown(risk_card("High Risk", f"{high_risk_pct:.1f}%", "#e74c3c"), unsafe_allow_html=True)
    k9.markdown(risk_card("Mid Risk", f"{mid_pct:.1f}%", "#f39c12"), unsafe_allow_html=True)
    k10.markdown(risk_card("Low Risk", f"{low_pct:.1f}%", "#2ecc71"), unsafe_allow_html=True)
    k11.empty()
    k12.empty()
    k13.empty()
    k14.empty()
st.divider()

# ================= CHART ROW =================
st.markdown(
    "<h3 style='text-align:center;'>Health Indicator Distribution by Risk Level</h3>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;color:gray;'>Shows how each health variable varies across pregnancy risk categories</p>",
    unsafe_allow_html=True
)

c1, c2, c3, c4, c5 = st.columns(5)

# ---------- PIE ----------
with c1:
    st.caption("Risk Distribution")

    fig = px.pie(
        filtered_df,
        names="RiskLevel",
        color="RiskLevel",
        color_discrete_map=COLOR_MAP
    )

    fig.update_layout(
        font_color="white",
        margin=dict(l=0,r=0,t=20,b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
    )

    fig.update_traces(textfont_color="white")
    st.plotly_chart(fig, use_container_width=True)

# ---------- AGE ----------
with c2:
    st.caption("Age Distribution")

    fig_age = px.box(
        filtered_df,
        x="RiskLevel",
        y="Age",
        color="RiskLevel",
        color_discrete_map=COLOR_MAP,
        category_orders={"RiskLevel":["low risk","mid risk","high risk"]}
    )

    fig_age.update_layout(font_color="white", margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig_age, use_container_width=True)

# ---------- BS ----------
with c3:
    st.caption("Blood Sugar")

    fig_bs = px.box(
        filtered_df,
        x="RiskLevel",
        y="BS",
        color="RiskLevel",
        color_discrete_map=COLOR_MAP,
        category_orders={"RiskLevel":["low risk","mid risk","high risk"]}
    )

    fig_bs.update_layout(font_color="white", margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig_bs, use_container_width=True)

# ---------- SYSTOLIC ----------
with c4:
    st.caption("Systolic BP")

    fig_sys = px.box(
        filtered_df,
        x="RiskLevel",
        y="SystolicBP",
        color="RiskLevel",
        color_discrete_map=COLOR_MAP,
        category_orders={"RiskLevel":["low risk","mid risk","high risk"]}
    )

    fig_sys.update_layout(font_color="white", margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig_sys, use_container_width=True)

# ---------- DIASTOLIC ----------
with c5:
    st.caption("Diastolic BP")

    fig_dia = px.box(
        filtered_df,
        x="RiskLevel",
        y="DiastolicBP",
        color="RiskLevel",
        color_discrete_map=COLOR_MAP,
        category_orders={"RiskLevel":["low risk","mid risk","high risk"]}
    )

    fig_dia.update_layout(font_color="white", margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig_dia, use_container_width=True)
st.divider()

# ================= INSIGHT ANALYSIS =================
st.subheader("Variable per Risk Level Insights")

left, right = st.columns([1.2,1])

# ---------- LEFT : AUTO INSIGHT ----------
with left:

    high_group = filtered_df[filtered_df.RiskLevel=="high risk"]
    low_group = filtered_df[filtered_df.RiskLevel=="low risk"]

    highest_bp = filtered_df.SystolicBP.max()
    highest_bs = filtered_df.BS.max()
    avg_age_high = high_group.Age.mean()
    avg_age_low = low_group.Age.mean()

    st.markdown(f"""
### Key Findings

• Highest **Systolic BP** recorded = **{highest_bp} mmHg**  
• Highest **Blood Sugar** recorded = **{highest_bs} mmol/L**

• Average age of **High Risk patients** = **{avg_age_high:.1f} years**  
• Average age of **Low Risk patients** = **{avg_age_low:.1f} years**

---

### Interpretation

• Patients with higher blood pressure tend to fall into **higher risk categories**  
• Older patients show slightly increased pregnancy risk  
• Blood sugar variability is higher in high-risk patients
""")

# ---------- RIGHT : STAT SUMMARY ----------
with right:

    risk_counts = filtered_df.RiskLevel.value_counts()

    st.markdown("### Risk Composition")

    for level in ["high risk","mid risk","low risk"]:
        pct = (risk_counts.get(level,0)/len(filtered_df))*100
        st.progress(int(pct), text=f"{level.title()} — {pct:.1f}%")

    st.markdown("---")

    st.markdown("### Clinical Note")
    st.info(
        "Patients classified as High Risk should receive closer monitoring "
        "especially for blood pressure and glucose levels."
    )
st.divider()

# ================= OUTLIER ANALYSIS =================
st.markdown(
    "<h3 style='text-align:center;'>Outlier Detection</h3>",
    unsafe_allow_html=True
)

cols = ["Age","SystolicBP","DiastolicBP","BS","BodyTemp","HeartRate"]
c1, c2, c3, c4, c5, c6 = st.columns(6)

for col, container in zip(cols, [c1,c2,c3,c4,c5,c6]):
    with container:

        fig = px.box(
            filtered_df,
            y=col,
            points="outliers"
        )

        fig.update_layout(
            title=col,
            font_color="white",
            margin=dict(l=0,r=0,t=30,b=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )

        fig.update_traces(
            marker=dict(size=5)
        )

        st.plotly_chart(fig, use_container_width=True)
st.divider()

# ================= OUTLIER INSIGHT =================
st.markdown("### Outlier Insights")

numeric_cols = ["Age","SystolicBP","DiastolicBP","BS","BodyTemp","HeartRate"]

insights = []

for col in numeric_cols:
    Q1 = filtered_df[col].quantile(0.25)
    Q3 = filtered_df[col].quantile(0.75)
    IQR = Q3 - Q1
    
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    
    outliers = filtered_df[(filtered_df[col] < lower) | (filtered_df[col] > upper)]
    pct = len(outliers) / len(filtered_df) * 100
    
    insights.append((col, pct))

# sorting berdasarkan outlier terbesar
insights.sort(key=lambda x: x[1], reverse=True)

most = insights[0]
least = insights[-1]

st.markdown(f"""
**Most Outliers Detected**
- **{most[0]}** → {most[1]:.1f}% data

**Least Outliers**
- **{least[0]}** → {least[1]:.1f}% data

---

**Interpretation**
- Variabel dengan outlier tinggi menandakan variabilitas data besar
- Variabel dengan outlier rendah menunjukkan distribusi stabil
- Outlier bisa menunjukkan kondisi medis ekstrem yang penting dianalisis
""")
st.divider()
# ================= DATA DISTRIBUTION =================
st.markdown(
    "<h3 style='text-align:center; margin-bottom:40px;'>Data Distribution</h3>",
    unsafe_allow_html=True
)

cols = ["Age","SystolicBP","DiastolicBP","BS","BodyTemp","HeartRate"]
grid = st.columns(3)

for i,col in enumerate(cols):
    with grid[i%3]:

        fig = px.histogram(filtered_df, x=col, nbins=20)

        fig.update_traces(
            marker=dict(
                color="#5DADE2",
                line=dict(color="white", width=1.2)
            )
        )

        fig.update_layout(
            title=col,
            font_color="white",
            margin=dict(l=0,r=0,t=30,b=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)

st.divider()
# ================= DATA DISTRIBUTION INSIGHT =================
st.markdown("### Distribution Insights")

cols_left, cols_right = st.columns(2)

variables = ["Age","SystolicBP","DiastolicBP","BS","BodyTemp","HeartRate"]

def get_skew_label(skew):
    if skew > 0.5:
        return "right-skewed (lebih banyak nilai rendah)"
    elif skew < -0.5:
        return "left-skewed (lebih banyak nilai tinggi)"
    else:
        return "relatively symmetric"

texts = []

for col in variables:
    mean = filtered_df[col].mean()
    median = filtered_df[col].median()
    skew = filtered_df[col].skew()

    texts.append(f"""
**{col}**
- Mean = {mean:.2f}  
- Median = {median:.2f}  
- Distribution shape = {get_skew_label(skew)}
""")

# bagi jadi 2 kolom (3 kiri, 3 kanan)
with cols_left:
    st.markdown("\n".join(texts[:3]))

with cols_right:
    st.markdown("\n".join(texts[3:]))

st.divider()
# ================= OHE =================
df_encoded = filtered_df.copy()

df_encoded["RiskLevel"] = df_encoded["RiskLevel"].map(RISK_MAP)

# ================= CORRELATION HEATMAP =================
st.markdown("<h2 style='text-align:center;'>Heatmap Correlation</h2>", unsafe_allow_html=True)

left, right = st.columns([1.2,1])

# ---------- HEATMAP ----------
with left:

    numeric_cols = ["Age","SystolicBP","DiastolicBP","BS","BodyTemp","HeartRate"]
    corr = df_encoded[numeric_cols + ["RiskLevel"]].corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        aspect="auto",
        height=600
    )

    fig.update_traces(
        textfont=dict(
            color="black",
            size=14,
            family="Arial Black"
        )
    )

    fig.update_layout(
        font_color="white",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------- EXPLANATION ----------
with right:

    st.markdown("### Insight Interpretation")

    strongest = corr.unstack().sort_values(ascending=False)

    # buang korelasi diri sendiri
    strongest = strongest[strongest < 1]

    top_pair = strongest.index[0]
    top_value = strongest.iloc[0]

    weakest = corr.unstack().sort_values().index[0]
    weakest_value = corr.unstack().sort_values().iloc[0]

    st.markdown(f"""
**Strongest Relationship**

- **{top_pair[0]} ↔ {top_pair[1]}**
- Correlation = **{top_value:.2f}**

Ini menunjukkan bahwa kedua variabel memiliki hubungan yang kuat.

---

**Weakest Relationship**

- **{weakest[0]} ↔ {weakest[1]}**
- Correlation = **{weakest_value:.2f}**

Hubungan antar variabel ini sangat lemah atau hampir tidak ada.

---

**Summary**

- Berdasarkan Heatmap Correlation dapat
disimpulkan bahwa kadar glukosa memiliki
hubungan dengan tingkat resiko kehamilan,
meskipun hubungan itu tidak terlalu kuat 
- Sedangkan kadar glukosa itu sendiri memiliki
hubungan dengan usia dan tekanan darah (sistolik
dan diastolik), meskipun tidak terlalu kuat  
""")

st.divider()

# ================= PREDICTION =================
st.subheader("Predict Pregnancy Risk")

st.caption("Enter patient health indicators to predict pregnancy risk level")

with st.form("prediction_form"):

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    age = c1.number_input("Age (year)", 10, 100, 25)
    sys = c2.number_input("Systolic BP", 50, 250, 120)
    dia = c3.number_input("Diastolic BP", 30, 200, 80)
    bs = c4.number_input("Blood Sugar", 0.0, 30.0, 7.0)
    hr = c5.number_input("Heart Rate", 30, 200, 80)
    temp = c6.number_input("Body Temp (°C)", 30.0, 45.0, 37.0)

    predict_btn = st.form_submit_button("Predict")

# ===== RESULT =====
st.markdown("### Risk Level of Maternity :")

if predict_btn:

    input_data = pd.DataFrame([{
        "Age": age,
        "SystolicBP": sys,
        "DiastolicBP": dia,
        "BS": bs,
        "HeartRate": hr,
        "BodyTemp_C": temp
    }])

    prediction = model.predict(input_data)[0]

    label_map = {1:"Low Risk", 2:"Mid Risk", 3:"High Risk"}
    result = label_map[prediction]

    if result == "High Risk":
        st.error(result)
        st.markdown("""
                    You may be experiencing a high pregnancy risk condition. Please consult a medical professional immediately for proper diagnosis and treatment. Regular monitoring is strongly recommended.
                    """)
    
    elif result == "Mid Risk":
        st.warning(result)
        st.markdown("""Your condition shows moderate risk indicators. It is recommended to monitor your health closely, maintain a balanced diet, and schedule routine check-ups with your healthcare provider.
                    """)
    else:
        st.success(result)
        st.markdown("""
                    I am very happy knowing that you are in a very good condition. Eat well, stay active, and don't forget to visit your doctor regularly for check-ups!
                    """)

st.divider()
# ================= DATA SUMMARY =================
st.markdown("""
<div style="
    text-align:center;
    padding:35px 20px;
    border-radius:18px;
    background: linear-gradient(135deg,#111827,#1f2937);
    border:1px solid rgba(255,255,255,0.08);
    margin-top:40px;
    margin-bottom:25px;
">
    <h1 style="
        margin-bottom:10px;
        font-size:34px;
        font-weight:700;
        letter-spacing:0.5px;
    ">
        Clinical Insight & Recommendation
    </h1>
    <p style="
        color:#9ca3af;
        font-size:16px;
    ">
        Final interpretation and medical insights generated from maternal health analysis
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin-top:10px;margin-bottom:30px;border:1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

avg_bs = filtered_df["BS"].mean()
avg_sys = filtered_df["SystolicBP"].mean()
avg_dia = filtered_df["DiastolicBP"].mean()
avg_temp = filtered_df["BodyTemp"].mean()

# cari variabel paling berpengaruh dari korelasi
corr_target = corr["RiskLevel"].drop("RiskLevel").abs().sort_values(ascending=False)
top_feature = corr_target.index[0]
top_corr = corr_target.iloc[0]

# ================= INSIGHT TEXT =================
st.markdown(f"""
### 📊 Population Insight

- Mayoritas pasien berada pada kategori **{filtered_df.RiskLevel.mode()[0].upper()}**
- Variabel paling berhubungan dengan risiko kehamilan → **{top_feature}**
- Kekuatan hubungan → **{top_corr:.2f}**

""")

# ================= HEALTH INTERPRETATION =================
st.markdown("### 🩺 Health Interpretation")

alerts = []

if avg_bs > 8:
    alerts.append("Average Blood Sugar tergolong tinggi")

if avg_sys > 130:
    alerts.append("Rata-rata tekanan darah sistolik tinggi")

if avg_dia > 85:
    alerts.append("Rata-rata tekanan darah diastolik tinggi")

if avg_temp > 37.5:
    alerts.append("Rata-rata suhu tubuh cenderung tinggi")

if alerts:
    for a in alerts:
        st.warning(a)
else:
    st.success("Sebagian besar indikator populasi berada dalam rentang normal")

# ================= RECOMMENDATION =================
st.markdown("### 💡 Recommendation")

st.info(f"""
Berdasarkan pola data:

• Fokus monitoring pada variabel **{top_feature}** karena memiliki pengaruh terbesar terhadap tingkat risiko  
• Lakukan screening rutin terutama pada pasien dengan nilai ekstrem  
• Gunakan hasil prediksi sebagai **alat pendukung keputusan**, bukan diagnosis utama

""")

st.divider()
# ================= TABLE =================
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# ================= FOOTER =================
st.markdown("---")
st.caption("Developed by Eva Musdalifah | Data Science Project")