import streamlit as st
import pandas as pd
import cv2
from PIL import Image
import numpy as np
import tempfile

# Load the color dataset
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

colors_df = load_colors()

# Find closest color name
def get_closest_color_name(R, G, B):
    min_dist = float("inf")
    color_name = "Unknown"
    for i in range(len(colors_df)):
        r, g, b = int(colors_df.loc[i, "R"]), int(colors_df.loc[i, "G"]), int(colors_df.loc[i, "B"])
        dist = abs(R - r) + abs(G - g) + abs(B - b)
        if dist < min_dist:
            min_dist = dist
            color_name = colors_df.loc[i, "color_name"]
    return color_name

# Streamlit UI
st.set_page_config(page_title="Color Detection App", layout="centered")
st.title("🎨 Color Detection from Image")
st.markdown("Upload an image and click to detect color!")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Save to temporary file to use with OpenCV
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        img_path = tmp_file.name

    # Load image using OpenCV and convert to RGB
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Display image using Streamlit and capture click coordinates
    st.image(img_rgb, caption="Click on the image below", use_column_width=True)

    click_x = st.number_input("X Coordinate", min_value=0, max_value=img.shape[1]-1, step=1)
    click_y = st.number_input("Y Coordinate", min_value=0, max_value=img.shape[0]-1, step=1)

    if st.button("Detect Color"):
        clicked_color = img_rgb[int(click_y), int(click_x)]
        R, G, B = int(clicked_color[0]), int(clicked_color[1]), int(clicked_color[2])
        color_name = get_closest_color_name(R, G, B)

        st.subheader("🧾 Detected Color")
        st.write(f"**Color Name:** {color_name}")
        st.write(f"**RGB:** ({R}, {G}, {B})")
        st.markdown(
            f"<div style='width:100px;height:50px;background-color:rgb({R},{G},{B});border:1px solid #000'></div>",
            unsafe_allow_html=True
        )

        st.success("Color detection complete!")

