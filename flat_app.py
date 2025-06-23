import streamlit as st
import os
import shutil
import tempfile

st.set_page_config(page_title="Folder Flattener", layout="centered")
st.title("📁 Folder Flattener Web App")
st.write("""
Select files from multiple folders (or drag-and-drop them), choose a destination, and flatten all files into one folder. 
**Note:** Streamlit does not support selecting folders directly, so please select or drag all files you want to flatten.
""")

uploaded_files = st.file_uploader(
    "Select or drag files from the folders you want to flatten:",
    type=None,
    accept_multiple_files=True
)

dest_dir = st.text_input(
    "Destination folder (absolute path, will be created if it doesn't exist):",
    value=os.path.join(tempfile.gettempdir(), "flattened_output")
)

if st.button("Flatten Files"):
    if not uploaded_files:
        st.error("Please upload at least one file.")
    elif not dest_dir:
        st.error("Please specify a destination folder.")
    else:
        os.makedirs(dest_dir, exist_ok=True)
        copied = 0
        renamed = 0
        skipped = 0
        st.info(f"Copying files to: {dest_dir}")
        progress = st.progress(0)
        for i, uploaded_file in enumerate(uploaded_files):
            file_data = uploaded_file.read()
            file_name = os.path.basename(uploaded_file.name)
            dest_path = os.path.join(dest_dir, file_name)
            base, ext = os.path.splitext(file_name)
            counter = 1
            # Handle name collisions
            while os.path.exists(dest_path):
                new_name = f"{base}_{counter}{ext}"
                dest_path = os.path.join(dest_dir, new_name)
                counter += 1
            try:
                with open(dest_path, "wb") as f:
                    f.write(file_data)
                if counter > 1:
                    renamed += 1
                else:
                    copied += 1
            except Exception as e:
                skipped += 1
                st.warning(f"Skipped {file_name}: {e}")
            progress.progress((i + 1) / len(uploaded_files))
        st.success(f"Done! {copied} files copied, {renamed} renamed, {skipped} skipped.")
        st.write(f"All files are now in: `{dest_dir}`") 