import streamlit as st
from pathlib import Path
from datetime import datetime

from file_operations import (
    create_file,
    read_file,
    rename_file,
    append_file,
    overwrite_file,
    delete_file,
    get_files
)


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="FileFlow",
    page_icon="📁",
    layout="wide"
)


# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Header */

.hero {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #111827, #1e293b);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 5px;
}

.hero p {
    color: #cbd5e1;
    font-size: 17px;
}


/* Cards */

.card {
    padding: 22px;
    border-radius: 16px;
    background: white;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04);
}


/* Stats */

.stat {
    padding: 18px;
    border-radius: 15px;
    background: white;
    border: 1px solid #e2e8f0;
}

.stat-title {
    color: #64748b;
    font-size: 14px;
}

.stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #0f172a;
}


/* Section title */

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #0f172a;
    margin-top: 20px;
    margin-bottom: 10px;
}


/* File item */

.file-item {
    padding: 15px;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    margin-bottom: 8px;
    background: var(--secondary-background-color);
    color: var(--text-color);
}

.file-item b {
    color: var(--text-color);
}

.file-item small {
    color: var(--text-color);
}

.section-title {
    color: var(--text-color);
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# HEADER
# -----------------------------

st.markdown("""
<div class="hero">

<h1>📁 FileFlow</h1>

<p>
A simple and powerful file management system built with
Python + Streamlit
</p>

</div>
""", unsafe_allow_html=True)


# -----------------------------
# GET FILES
# -----------------------------

files = get_files()

file_count = len(files)

total_size = sum(
    file.stat().st_size for file in files
    if file.is_file()
)


# -----------------------------
# STATISTICS
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat">
        <div class="stat-title">Total Files</div>
        <div class="stat-value">📄 {file_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat">
        <div class="stat-title">Storage Used</div>
        <div class="stat-value">{total_size} B</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat">
        <div class="stat-title">System Status</div>
        <div class="stat-value">🟢 Active</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("📂 FileFlow")

st.sidebar.markdown("### Operations")

operation = st.sidebar.radio(
    "Choose an operation",
    [
        "📄 Create File",
        "👁️ Read File",
        "✏️ Update File",
        "🗑️ Delete File"
    ]
)


# =========================================================
# CREATE
# =========================================================

if operation == "📄 Create File":

    st.markdown('<div class="section-title">Create New File</div>',
                unsafe_allow_html=True)

    with st.container(border=True):

        filename = st.text_input(
            "File name",
            placeholder="example.txt"
        )

        content = st.text_area(
            "File content",
            height=200,
            placeholder="Write something here..."
        )

        if st.button(
            "➕ Create File",
            use_container_width=True,
            type="primary"
        ):

            if not filename:
                st.warning("Please enter a file name.")

            else:

                success, message = create_file(
                    filename,
                    content
                )

                if success:
                    st.success(message)
                    st.rerun()

                else:
                    st.error(message)


# =========================================================
# READ
# =========================================================

elif operation == "👁️ Read File":

    st.markdown(
        '<div class="section-title">Read File</div>',
        unsafe_allow_html=True
    )

    if not files:

        st.info("No files available. Create a file first.")

    else:

        file_names = [
            file.name
            for file in files
            if file.is_file()
        ]

        selected_file = st.selectbox(
            "Select a file",
            file_names
        )

        if st.button(
            "👁️ Read File",
            use_container_width=True,
            type="primary"
        ):

            success, content = read_file(selected_file)

            if success:

                st.markdown("### File Content")

                st.code(
                    content,
                    language="text"
                )

            else:

                st.error(content)


# =========================================================
# UPDATE
# =========================================================

elif operation == "✏️ Update File":

    st.markdown(
        '<div class="section-title">Update File</div>',
        unsafe_allow_html=True
    )

    if not files:

        st.info("No files available.")

    else:

        file_names = [
            file.name
            for file in files
            if file.is_file()
        ]

        selected_file = st.selectbox(
            "Select a file",
            file_names
        )

        update_type = st.selectbox(
            "Choose operation",
            [
                "Rename",
                "Append Content",
                "Overwrite Content"
            ]
        )


        # -------------------------
        # Rename
        # -------------------------

        if update_type == "Rename":

            new_name = st.text_input(
                "New file name",
                placeholder="new_name.txt"
            )

            if st.button(
                "✏️ Rename File",
                use_container_width=True,
                type="primary"
            ):

                if not new_name:

                    st.warning("Enter a new file name.")

                else:

                    success, message = rename_file(
                        selected_file,
                        new_name
                    )

                    if success:

                        st.success(message)
                        st.rerun()

                    else:

                        st.error(message)


        # -------------------------
        # Append
        # -------------------------

        elif update_type == "Append Content":

            content = st.text_area(
                "Content to append",
                height=180
            )

            if st.button(
                "➕ Append Content",
                use_container_width=True,
                type="primary"
            ):

                success, message = append_file(
                    selected_file,
                    content
                )

                if success:

                    st.success(message)

                else:

                    st.error(message)


        # -------------------------
        # Overwrite
        # -------------------------

        elif update_type == "Overwrite Content":

            content = st.text_area(
                "New file content",
                height=180
            )

            st.warning(
                "⚠️ This will replace the existing file content."
            )

            if st.button(
                "🔄 Overwrite File",
                use_container_width=True,
                type="primary"
            ):

                success, message = overwrite_file(
                    selected_file,
                    content
                )

                if success:

                    st.success(message)

                else:

                    st.error(message)


# =========================================================
# DELETE
# =========================================================

elif operation == "🗑️ Delete File":

    st.markdown(
        '<div class="section-title">Delete File</div>',
        unsafe_allow_html=True
    )

    if not files:

        st.info("No files available.")

    else:

        file_names = [
            file.name
            for file in files
            if file.is_file()
        ]

        selected_file = st.selectbox(
            "Select a file",
            file_names
        )

        st.error(
            "⚠️ Deleted files cannot be recovered."
        )

        confirm = st.checkbox(
            "I understand that this file will be permanently deleted."
        )

        if st.button(
            "🗑️ Delete File",
            use_container_width=True,
            type="primary"
        ):

            if not confirm:

                st.warning(
                    "Please confirm the deletion first."
                )

            else:

                success, message = delete_file(
                    selected_file
                )

                if success:

                    st.success(message)
                    st.rerun()

                else:

                    st.error(message)


# -----------------------------
# FILE EXPLORER
# -----------------------------

st.markdown(
    '<div class="section-title">📋 File Explorer</div>',
    unsafe_allow_html=True
)

if not files:

    st.info("No files created yet.")

else:

    for file in files:

        if file.is_file():

            size = file.stat().st_size

            modified = datetime.fromtimestamp(
                file.stat().st_mtime
            ).strftime("%d %b %Y, %I:%M %p")

            st.markdown(f"""
            <div class="file-item">

            📄 <b>{file.name}</b>

            <br>

            <small>
            Size: {size} bytes &nbsp; | &nbsp;
            Modified: {modified}
            </small>

            </div>
            """, unsafe_allow_html=True)