import streamlit as st
import os

st.title("📸 Charts")
st.markdown("---")

# Define the directory where your images are stored
# This assumes 'assets' is in the main project directory, one level up from 'pages'
script_dir = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.abspath(os.path.join(script_dir, os.pardir, "Distribution Charts"))

st.write("""Explore a visual journey for Distribution Charts of medial data in the UAE.""")

st.markdown("---") # Initial separator

# Check if the assets directory exists
if os.path.exists(ASSETS_DIR) and os.path.isdir(ASSETS_DIR):
    # List all files in the assets directory
    all_files = os.listdir(ASSETS_DIR)

    # Filter for common image file extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    image_files = [f for f in all_files if f.lower().endswith(image_extensions)]

    # Sort the image files alphabetically for consistent display
    image_files.sort()

    if not image_files:
        st.warning(f"No image files found in the directory: {ASSETS_DIR}")
    else:
        # Loop through the image files and display each image with its filename as caption
        for img_file in image_files:
            image_path = os.path.join(ASSETS_DIR, img_file)
            # Create caption from filename by removing the extension
            caption = os.path.splitext(img_file)[0].replace('_', ' ').replace('-', ' ').title()

            st.image(image_path, caption=caption, use_container_width=True)
            st.markdown("---") # Separator after each image
else:
    st.error(f"Image assets directory not found: `{ASSETS_DIR}`. Please ensure your 'assets' folder is in the main project directory.")


st.write("Thank you for exploring our gallery.")
