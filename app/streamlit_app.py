
import streamlit as st
from PIL import Image

from src.predict import predict_fruit

st.set_page_config(
    page_title="FruitFresh AI",
    page_icon="🍎",
    layout="centered",
)

st.title("🍎 FruitFresh AI")
st.write("Upload an apple, banana, or orange image to predict its freshness.")

uploaded_file = st.file_uploader(
    "Choose a fruit image",
    type=["jpg", "jpeg", "png", "webp"],
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.image(image, caption="Uploaded fruit", width="stretch")

    if st.button("Predict freshness", type="primary"):
        with st.spinner("Analyzing image..."):
            try:
                result = predict_fruit(image)

                class_name = result["class_name"]
                fruit = (
                    class_name.replace("fresh", "")
                    .replace("rotten", "")
                    .capitalize()
                )
                condition = (
                    "Fresh" if class_name.startswith("fresh") else "Rotten"
                )

                st.subheader("Prediction")
                st.success(f"{fruit}: {condition}")
                st.metric(
                    "Model confidence",
                    f"{result['confidence']:.2%}",
                )

                st.subheader("Scores for all classes")
                st.bar_chart(result["probabilities"])

            except Exception as exc:
                st.error(f"Prediction failed: {exc}")
