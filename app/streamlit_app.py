
import streamlit as st
import pandas as pd
from PIL import Image
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.predict import predict_fruit


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="FruitFresh AI",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------
# CUSTOM CSS — THEME, ANIMATIONS & RESPONSIVENESS
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #07111f;
        --panel: #101e30;
        --green: #69f0ae;
        --green-dark: #24c982;
        --text: #f0f6fc;
        --muted: #9aacc0;
        --border: rgba(151, 178, 204, 0.16);
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 12% 0%, rgba(31, 153, 111, 0.16), transparent 34%),
            radial-gradient(ellipse at 90% 22%, rgba(34, 112, 175, 0.14), transparent 30%),
            linear-gradient(145deg, #07111f 0%, #0a1727 50%, #07111f 100%);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(7, 17, 31, 0.75);
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1120px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text) !important;
    }

    p, label, span {
        letter-spacing: 0.1px;
    }

    /* Hero section */
    .hero {
        position: relative;
        overflow: hidden;
        padding: 38px 34px;
        margin: 8px 0 26px 0;
        border: 1px solid rgba(105, 240, 174, 0.22);
        border-radius: 26px;
        background:
            radial-gradient(circle at 88% 18%, rgba(105, 240, 174, 0.16), transparent 32%),
            linear-gradient(120deg, rgba(18, 39, 57, 0.97), rgba(10, 28, 43, 0.94));
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.20);
        animation: fadeUp 0.75s ease-out both;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        right: -95px;
        bottom: -145px;
        border-radius: 50%;
        border: 1px solid rgba(105, 240, 174, 0.25);
        box-shadow:
            0 0 0 22px rgba(105, 240, 174, 0.025),
            0 0 0 44px rgba(105, 240, 174, 0.02);
        pointer-events: none;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: #8af5bb;
        background: rgba(105, 240, 174, 0.09);
        border: 1px solid rgba(105, 240, 174, 0.20);
        padding: 7px 12px;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 1.3px;
        text-transform: uppercase;
    }

    .live-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #69f0ae;
        box-shadow: 0 0 12px rgba(105, 240, 174, 0.9);
        animation: pulse 2s infinite;
    }

    .hero-title {
        margin: 19px 0 8px 0;
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(2.25rem, 5vw, 3.65rem);
        font-weight: 700;
        line-height: 1.08;
        letter-spacing: -2px;
        color: #f4f9ff;
    }

    .hero-title .accent {
        color: #69f0ae;
        text-shadow: 0 0 28px rgba(105, 240, 174, 0.14);
    }

    .hero-description {
        color: #a9bdcf;
        font-size: 1.02rem;
        line-height: 1.75;
        max-width: 650px;
        margin-bottom: 0;
    }

    .hero-fruit {
        font-size: 5rem;
        text-align: center;
        animation: floatFruit 4s ease-in-out infinite;
        filter: drop-shadow(0 12px 25px rgba(105, 240, 174, 0.14));
    }

    /* Section headings */
    .section-heading {
        margin: 22px 0 14px 0;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.35rem;
        font-weight: 600;
        color: #eff7ff;
    }

    .section-caption {
        color: #91a6ba;
        font-size: 0.91rem;
        margin-top: -8px;
        margin-bottom: 18px;
        line-height: 1.6;
    }

    /* Upload container */
    [data-testid="stFileUploader"] {
        padding: 13px;
        border: 1px dashed rgba(105, 240, 174, 0.40);
        border-radius: 18px;
        background: rgba(15, 34, 51, 0.75);
        transition: border-color 0.25s ease, background 0.25s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #69f0ae;
        background: rgba(25, 55, 67, 0.78);
    }

    [data-testid="stFileUploaderDropzone"] {
        background: rgba(8, 21, 35, 0.50);
        border-radius: 13px;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #c4d5e5;
    }

    [data-testid="stImage"] img {
        border-radius: 16px;
    }

    /* Buttons */
    .stButton > button {
        min-height: 49px;
        width: 100%;
        border: 1px solid rgba(105, 240, 174, 0.45);
        border-radius: 13px;
        background: linear-gradient(110deg, #69f0ae, #37d994);
        color: #062017;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 5px 20px rgba(55, 217, 148, 0.12);
        transition: transform 0.22s ease, box-shadow 0.22s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 9px 26px rgba(55, 217, 148, 0.25);
        border-color: #a3ffd0;
        color: #04190f;
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Result cards */
    .result-card {
        position: relative;
        overflow: hidden;
        padding: 25px;
        margin: 8px 0 15px 0;
        border: 1px solid rgba(105, 240, 174, 0.25);
        border-radius: 20px;
        background:
            radial-gradient(circle at 100% 0%, rgba(105, 240, 174, 0.10), transparent 38%),
            linear-gradient(140deg, #11283a, #0c1b2b);
        animation: fadeUp 0.6s ease-out both;
    }

    .result-label {
        color: #91a8bc;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        font-weight: 700;
    }

    .result-name {
        color: #f2f8ff;
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(1.65rem, 3vw, 2.25rem);
        font-weight: 700;
        margin: 10px 0;
    }

    .result-status {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 700;
    }

    .fresh {
        color: #8cf5b9;
        background: rgba(105, 240, 174, 0.12);
        border: 1px solid rgba(105, 240, 174, 0.28);
    }

    .rotten {
        color: #ffb3a8;
        background: rgba(255, 110, 100, 0.11);
        border: 1px solid rgba(255, 130, 115, 0.27);
    }

    .confidence-card {
        padding: 20px;
        border: 1px solid var(--border);
        border-radius: 18px;
        background: rgba(16, 30, 48, 0.76);
        height: 100%;
    }

    .confidence-value {
        color: #69f0ae;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.25rem;
        font-weight: 700;
        margin: 7px 0;
    }

    /* General Streamlit containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--border);
        border-radius: 18px;
    }

    [data-testid="stMetric"] {
        padding: 17px;
        border: 1px solid var(--border);
        border-radius: 15px;
        background: rgba(16, 30, 48, 0.68);
    }

    [data-testid="stMetricLabel"] {
        color: #9db2c6;
    }

    [data-testid="stMetricValue"] {
        color: #eaf7f0;
    }

    [data-testid="stAlert"] {
        border-radius: 13px;
    }

    /* Footer */
    .footer {
        margin-top: 45px;
        padding-top: 20px;
        border-top: 1px solid rgba(151, 178, 204, 0.14);
        text-align: center;
        color: #8298ad;
        font-size: 0.84rem;
        line-height: 1.8;
    }

    .footer strong {
        color: #8af5bb;
        font-weight: 600;
    }

    /* Animations */
    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(16px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.55; transform: scale(0.82); }
    }

    @keyframes floatFruit {
        0%, 100% { transform: translateY(0) rotate(-3deg); }
        50% { transform: translateY(-10px) rotate(3deg); }
    }

    @media (max-width: 700px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1rem 1rem 2rem 1rem;
        }

        .hero {
            padding: 27px 22px;
            border-radius: 20px;
        }

        .hero-title {
            letter-spacing: -1px;
        }

        .hero-fruit {
            font-size: 3rem;
        }

        .result-card {
            padding: 20px;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------
hero_left, hero_right = st.columns([4, 1], vertical_alignment="center")

with hero_left:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">
                <span class="live-dot"></span>
                TRANSFER LEARNING · COMPUTER VISION
            </div>
            <div class="hero-title">
                FruitFresh <span class="accent">AI</span>
            </div>
            <p class="hero-description">
                A smarter way to inspect your fruit. Upload an image and let
                our deep-learning model predict whether your apple, banana,
                or orange appears fresh or rotten.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_right:
    st.markdown(
        '<div class="hero-fruit">🥗</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="section-heading">🍃 Analyse your fruit</div>
    <div class="section-caption">
        Upload a clear image of one fruit. For best results, use good lighting
        and keep the fruit visible in the frame.
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# IMAGE UPLOAD
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Choose a fruit image",
    type=["jpg", "jpeg", "png", "webp"],
    help="Supported formats: JPG, JPEG, PNG and WEBP.",
)

if uploaded_file is None:
    st.markdown(
        """
        <div class="confidence-card" style="text-align:center; padding:28px;">
            <div style="font-size:2.2rem; margin-bottom:10px;">📸</div>
            <div style="font-size:1.05rem; font-weight:600; color:#eaf4ff;">
                Your fruit analysis starts here
            </div>
            <div style="color:#91a6ba; margin-top:7px; line-height:1.7;">
                Choose an image above to preview your fruit and run the
                freshness prediction.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    try:
        image = Image.open(uploaded_file).convert("RGB")

        preview_col, details_col = st.columns(
            [1.15, 1],
            gap="large",
            vertical_alignment="center",
        )

        with preview_col:
            st.markdown(
                '<div class="section-heading">🖼️ Image preview</div>',
                unsafe_allow_html=True,
            )
            st.image(
                image,
                caption="Uploaded fruit image",
                use_container_width=True,
            )

        with details_col:
            st.markdown(
                '<div class="section-heading">🔬 Ready to analyse</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="confidence-card">
                    <div class="result-label">IMAGE RECEIVED</div>
                    <div style="font-size:1.15rem; font-weight:600;
                                color:#eaf4ff; margin:10px 0;">
                        Your image is ready
                    </div>
                    <div style="color:#91a6ba; line-height:1.8;">
                        Run the model to see the predicted fruit class,
                        freshness category, confidence score, and class scores.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")
            predict_clicked = st.button(
                "✨  Predict freshness",
                type="primary",
                use_container_width=True,
            )

        if predict_clicked:
            with st.spinner("Analysing your fruit image..."):
                try:
                    result = predict_fruit(image)

                    class_name = result["class_name"]
                    condition = (
                        "Fresh"
                        if class_name.lower().startswith("fresh")
                        else "Rotten"
                    )

                    fruit = (
                        class_name.lower()
                        .replace("fresh", "")
                        .replace("rotten", "")
                        .replace("_", " ")
                        .replace("-", " ")
                        .strip()
                        .rstrip("s")
                        .title()
                    )

                    is_fresh = condition == "Fresh"
                    status_class = "fresh" if is_fresh else "rotten"
                    status_icon = "🌿" if is_fresh else "⚠️"

                    st.markdown(
                        '<div class="section-heading">📊 Analysis results</div>',
                        unsafe_allow_html=True,
                    )

                    result_col, confidence_col = st.columns(
                        [1.2, 1],
                        gap="medium",
                    )

                    with result_col:
                        st.markdown(
                            f"""
                            <div class="result-card">
                                <div class="result-label">PREDICTED FRUIT</div>
                                <div class="result-name">{fruit}</div>
                                <span class="result-status {status_class}">
                                    {status_icon} {condition}
                                </span>
                                <div style="color:#91a6ba; font-size:0.9rem;
                                            margin-top:17px; line-height:1.7;">
                                    Predicted class:
                                    <strong style="color:#eaf4ff;">
                                        {class_name}
                                    </strong>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with confidence_col:
                        confidence = float(result["confidence"])

                        st.markdown(
                            f"""
                            <div class="confidence-card">
                                <div class="result-label">MODEL CONFIDENCE</div>
                                <div class="confidence-value">
                                    {confidence:.2%}
                                </div>
                                <div style="color:#91a6ba; line-height:1.7;
                                            font-size:0.9rem;">
                                    Confidence reported by the model for
                                    its predicted class.
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.write("")
                    st.caption(
                        "Model confidence is not a guarantee of correctness. "
                        "Results can be affected by image quality, lighting, "
                        "and differences from the training dataset."
                    )

                    st.markdown(
                        '<div class="section-heading">📈 Scores across all classes</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        '<div class="section-caption">'
                        'Compare the model scores for the available fruit classes.'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    
                    probabilities = result["probabilities"]
                    if isinstance(probabilities, dict):
                        chart_data = pd.DataFrame(
                            {
                                "Class": [
                                    name.replace("_", " ").title()
                                    for name in probabilities.keys()
                                ],
                                "Probability": list(probabilities.values()),
                            }             
                            ).set_index("Class")
                    else:
                        chart_data = probabilities

                    st.bar_chart(chart_data)

                except Exception as exc:
                    st.error(f"Prediction failed: {exc}")

    except Exception as exc:
        st.error(f"Could not read this image: {exc}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <div class="footer">
        <strong>🍃 FruitFresh AI</strong><br>
        Built with Streamlit, TensorFlow and transfer learning.<br>
        An educational computer-vision project for fruit freshness
        classification.
    </div>
    """,
    unsafe_allow_html=True,
)
