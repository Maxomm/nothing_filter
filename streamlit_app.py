from PIL import Image, ImageOps
from numpy import asarray, hstack
import streamlit as st

st.title("Nothing Filter")

uploaded_file = st.file_uploader(
    "image", type="jpg", accept_multiple_files=False
)
image = (
    Image.open(uploaded_file) if uploaded_file is not None else Image.open("input.jpg")
)

fixed_image = ImageOps.exif_transpose(image)
new_img = asarray(fixed_image)

SLICES = st.slider("Slices", 1, 20, 8) + 1
# OFFSET = st.slider("Offset", 0 + slice_width, width - slice_width, 0)
FILTER_STR = st.slider("Strength", 0.0, 1.0, 0.6, 0.1)

height, width = fixed_image.height, fixed_image.width
slice_width = width / SLICES
start_index = (width / 2) - (slice_width / 2)


for i in range(SLICES):
    cur_idx = start_index + (i - (SLICES - 1) / 2) * slice_width * (1 - FILTER_STR)
    end_idx = int(cur_idx + slice_width)
    cur_idx = int(cur_idx)
    new = new_img[0:height, cur_idx:end_idx]
    combined = hstack((combined, new)) if i > 0 else new_img[0:height, cur_idx:end_idx]


im = Image.fromarray(combined)

col1, col2 = st.columns(2)
with col1:
    st.image(fixed_image)
with col2:
    st.image(im)

im.save("output.jpg")

with open("output.jpg", "rb") as img:
    btn = st.download_button(
        label="Download",
        data=img,
        file_name="nothing_filter.jpg",
        mime="image/png",
    )
