import streamlit as st
import tempfile
import pandas as pd
from duplicate_finder import find_duplicates

st.set_page_config(page_title="Duplicate Finder", layout="wide")
st.title("🔍Duplicate Finder Agent")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(uploaded_file.read())
        input_file = tmp.name

    if st.button("Find Duplicates"):
        df = find_duplicates(input_file)

        if df.empty:
            st.warning("No duplicates found ❌")
        else:
            pd.set_option("display.max_columns", None)
            pd.set_option("display.max_rows", None)
            st.success(f"Found {df['Pair_ID'].nunique()} duplicate pairs ✅")
            st.dataframe(df, use_container_width=True)
