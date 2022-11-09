from PIL import Image, ImageOps
import numpy as np
import streamlit as st

st.title("Nothing Filter")


uploaded_file = st.file_uploader(None,type=["jpg", "png"], accept_multiple_files=False
)
image = (
    Image.open(uploaded_file) if uploaded_file is not None else Image.open("input.jpg")
)


img_format = str(image.format).lower()

fixed_image = ImageOps.exif_transpose(image)
converted_image = fixed_image.convert('RGB')
new_img = np.asarray(converted_image)

col1, col2 = st.columns(2)
with col1:
    with st.expander("Change Parameters"):
        SLICES = st.slider("Slices", 1, 20, 8) + 1
        FILTER_STR = st.slider("Spread", 0.0, 1.0, 0.6, 0.1)
        FACTOR = st.slider("Gradient", 0.80, 1.00, 0.90, 0.01)

height, width = fixed_image.height, fixed_image.width
slice_width = width / SLICES
start_index = (width / 2) - (slice_width / 2)


def add_gradient(array_section):
    array = create_gradient(int(slice_width), height, (255, 255, 255), (0, 0, 0))
    test = array_section * FACTOR + array * (1 - FACTOR)
    return test


def create_gradient(width, height, start_list, stop_list):
    result = np.zeros((height, width, len(start_list)), dtype=np.float64)
    for i, (start, stop) in enumerate(zip(start_list, stop_list)):
        result[:, :, i] = np.tile(np.linspace(start, stop, width), (height, 1))
    return result


for i in range(SLICES):
    cur_idx = start_index + (i - (SLICES - 1) / 2) * slice_width * (1 - FILTER_STR)
    cur_idx = int(cur_idx)
    end_idx = int(cur_idx + slice_width)

    new = new_img[0:height, cur_idx:end_idx]
    new = add_gradient(new)
    combined = (
        np.hstack((combined, new))
        if i > 0
        else add_gradient(new_img[0:height, cur_idx:end_idx])
    )


im = Image.fromarray(np.uint8(combined))
with col2:
    st.image(im)

with col1:                     
    im.save("output." + img_format)


    with open("output." + img_format, "rb") as img:
        btn = st.download_button(
            label="Download",
            data=img,
            file_name="nothing_filter." + img_format,
            mime="image/png",
        )
