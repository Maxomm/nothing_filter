from PIL import Image, ImageOps
import io
import numpy as np
import streamlit as st


def add_gradient(array_section):
    array = create_gradient(int(slice_width), height, (255, 255, 255), (0, 0, 0))
    test = array_section * 0.9 + array * (1 - 0.9)
    return test


def create_gradient(width, height, start_list, stop_list):
    result = np.zeros((height, width, len(start_list)), dtype=np.float64)
    for i, (start, stop) in enumerate(zip(start_list, stop_list)):
        result[:, :, i] = np.tile(np.linspace(start, stop, width), (height, 1))
    return result


def apply_filter(input_array):
    for i in range(slice_amt):
        cur_idx = start_index + (i - (slice_amt - 1) / 2) * slice_width * (
            1 - filter_str
        )
        cur_idx = int(cur_idx)
        end_idx = int(cur_idx + slice_width)

        new_data = input_array[0:height, cur_idx:end_idx]
        new_data = add_gradient(new_data) if gradient_enabled else new_data
        new_image = np.hstack((new_image, new_data)) if i > 0 else new_data
    return new_image


if __name__ == "__main__":
    st.title("Nothing Filter")

    up_file = st.file_uploader(
        label="Image",
        type=["jpg", "png"],
        accept_multiple_files=False,
        label_visibility="hidden",
    )

    image = Image.open(up_file) if up_file is not None else Image.open("input.jpeg")

    img_format = str(image.format).lower()
    fixed_image = ImageOps.exif_transpose(image)
    converted_image = fixed_image.convert("RGB")
    img_array = np.asarray(converted_image)

    left_column, right_column = st.columns(2)
    with left_column:
        with st.expander("Change Parameters"):
            slice_amt = st.slider("Slice Amount", 1, 10, 8) + 1
            filter_str = st.slider("Filter Strength", 0.0, 1.0, 0.6, 0.1)
            gradient_enabled = st.checkbox("Enable Gradient", value=True)

    height, width = fixed_image.height, fixed_image.width
    slice_width = width / slice_amt
    start_index = (width / 2) - (slice_width / 2)

    filtered_img = apply_filter(img_array)
    image = Image.fromarray(np.uint8(filtered_img))

    with right_column:
        st.image(image)

        buf = io.BytesIO()
        image.save(buf, format=img_format)
        st.download_button(
            label="Download",
            data=buf.getvalue(),
            file_name="nothing_filter." + img_format,
        )
