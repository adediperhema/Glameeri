import os
import httpx
import streamlit as st
from PIL import Image
from io import BytesIO
from streamlit_cropper import st_cropper

# Configuration matching your backend setup
ALLOWED_CATEGORIES = ["tops", "bottoms", "one-pieces"]
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Streamlit Page Setup
st.set_page_config(page_title="AI Try-On Studio", page_icon="👗", layout="wide")
st.title("👗 Interactive Virtual Try-On Studio")
st.markdown(
    "Crop your photos, adjust fitting controls, and see the composite instantly."
)
st.divider()

col_input, col_output = st.columns(2, gap="large")

with col_input:
    st.subheader("1. Setup & Crop Media Assets")
    sub_col1, sub_col2 = st.columns(2)

    person_cropped_bytes = None
    garment_cropped_bytes = None

    # --- COLUMN 1: PERSON PHOTO ---
    with sub_col1:
        st.write("**Your Photo (Person)**")
        person_file = st.file_uploader(
            "Upload Person", type=["png", "jpg", "jpeg"], label_visibility="collapsed"
        )
        if person_file is not None:
            img_p = Image.open(person_file)
            st.write("📐 Drag box corners to crop:")

            # Interactive cropper layout component
            cropped_p = st_cropper(
                img_file=img_p,
                realtime_update=True,
                box_color="#FF4B4B",
                aspect_ratio=None,
            )

            # Alternative way to extract raw image bytes safely without confusing code editor linters
            buf_p = BytesIO()
            Image.Image.save(cropped_p, buf_p, format="PNG")
            person_cropped_bytes = buf_p.getvalue()

            st.image(
                cropped_p, caption="Cropped Person Preview", use_container_width=True
            )

    # --- COLUMN 2: CLOTHING ITEM ---
    with sub_col2:
        st.write("**Clothing Item**")
        garment_file = st.file_uploader(
            "Upload Clothing", type=["png", "jpg", "jpeg"], label_visibility="collapsed"
        )
        if garment_file is not None:
            img_g = Image.open(garment_file)
            st.write("📐 Drag box corners to crop:")

            # Interactive cropper layout component
            cropped_g = st_cropper(
                img_file=img_g,
                realtime_update=True,
                box_color="#FF4B4B",
                aspect_ratio=None,
            )

            # Alternative way to extract raw image bytes safely without confusing code editor linters
            buf_g = BytesIO()
            Image.Image.save(cropped_g, buf_g, format="PNG")
            garment_cropped_bytes = buf_g.getvalue()

            st.image(
                cropped_g, caption="Cropped Clothing Preview", use_container_width=True
            )

    # --- CONTROLS SECTION ---
    st.subheader("2. Fit Customization Settings")
    category = st.selectbox("Garment Category", options=ALLOWED_CATEGORIES)

    with st.expander("🛠️ Fine-Tune Clothes Fitting Controls", expanded=True):
        scale_val = st.slider(
            "Garment Scale Multiplier",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.05,
        )
        x_val = st.slider(
            "Horizontal Adjust (Left ⇄ Right)",
            min_value=-150,
            max_value=150,
            value=0,
            step=5,
        )
        y_val = st.slider(
            "Vertical Adjust (Up ⇄ Down)",
            min_value=-150,
            max_value=150,
            value=0,
            step=5,
        )

    submit_btn = st.button(
        "✨ Apply & Render Try-On", type="primary", use_container_width=True
    )

# --- OUTPUT VIEW ROW SPLIT ---
with col_output:
    st.subheader("3. Rendered Output")

    if submit_btn:
        if not person_cropped_bytes or not garment_cropped_bytes:
            st.error(
                "Missing asset configurations. Please make sure both images are uploaded."
            )
        else:
            with st.spinner("Processing local canvas rendering..."):
                try:
                    files = {
                        "person_image": (
                            "person.png",
                            person_cropped_bytes,
                            "image/png",
                        ),
                        "garment_image": (
                            "garment.png",
                            garment_cropped_bytes,
                            "image/png",
                        ),
                    }
                    data = {
                        "category": category,
                        "offset_x": str(x_val),
                        "offset_y": str(y_val),
                        "scale_multiplier": str(scale_val),
                    }

                    response = httpx.post(
                        f"{API_URL}/try-on", files=files, data=data, timeout=30.0
                    )

                    if response.status_code == 200:
                        output_image = Image.open(BytesIO(response.content))
                        st.image(
                            output_image,
                            caption="Tailored Output Fit",
                            use_container_width=True,
                        )
                        st.success("Rendering success!")
                        st.download_button(
                            label="📥 Save Look",
                            data=response.content,
                            file_name="tryon_fitted.png",
                            mime="image/png",
                            use_container_width=True,
                        )
                    else:
                        st.error(f"Backend Issue: {response.text}")
                except Exception as e:
                    st.error(f"Network Failure: {e}")
    else:
        st.info("Adjust framing and click 'Apply & Render Try-On' to composite.")
