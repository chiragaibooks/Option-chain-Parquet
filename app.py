import io
import re
import sqlite3
import tempfile
import urllib.parse
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="GitHub SQLite & Parquet Explorer", layout="wide")

st.title("📂 GitHub SQLite & Parquet Explorer")


# --- Helper Functions ---
def convert_to_raw_url(url: str) -> str:
    """Converts standard GitHub web URLs to raw.githubusercontent.com URLs."""
    url = url.strip()
    if "github.com" in url and "/blob/" in url:
        return url.replace("github.com", "raw.githubusercontent.com").replace(
            "/blob/", "/"
        )
    return url


def parse_github_folder_url(url: str):
    """Parses a GitHub directory URL to extract owner, repo, and folder path."""
    pattern = r"github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.*)"
    match = re.search(pattern, url.strip())
    if match:
        owner, repo, branch, folder_path = match.groups()
        return owner, repo, branch, folder_path
    return None, None, None, None


@st.cache_data(ttl=600, show_spinner=False)
def fetch_parquet_files_from_github_folder(folder_url: str):
    """Fetches the list of .parquet files in a GitHub folder using the GitHub REST API."""
    owner, repo, branch, folder_path = parse_github_folder_url(folder_url)
    if not owner:
        raise ValueError("Invalid GitHub folder URL format. Use format: https://github.com/owner/repo/tree/branch/folder")

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{folder_path}?ref={branch}"
    response = requests.get(api_url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch folder contents. HTTP Status: {response.status_code}")

    files = response.json()
    parquet_files = {
        item["name"]: item["download_url"]
        for item in files
        if item["type"] == "file" and item["name"].endswith(".parquet")
    }
    return parquet_files


@st.cache_data(ttl=600, show_spinner=False)
def load_parquet_from_url(download_url: str) -> pd.DataFrame:
    """Downloads and loads a Parquet file into a Pandas DataFrame."""
    response = requests.get(download_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Parquet file. HTTP Status: {response.status_code}")
    return pd.read_parquet(io.BytesIO(response.content))


@st.cache_data(ttl=600, show_spinner=False)
def load_database_from_github(raw_url: str) -> str:
    """Downloads the SQLite file from GitHub and stores it in a temporary file."""
    response = requests.get(raw_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch database from GitHub. HTTP Status: {response.status_code}")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_file.write(response.content)
    temp_file.close()
    return temp_file.name


# --- Dynamic Filter Component ---
def apply_dataframe_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Adds UI controls to filter a dataframe by selected columns."""
    df_filtered = df.copy()
    
    with st.expander("🔍 Filter Data"):
        columns_to_filter = st.multiselect("Select columns to filter", df.columns)
        
        for col in columns_to_filter:
            if pd.api.types.is_numeric_dtype(df[col]):
                min_val, max_val = float(df[col].min()), float(df[col].max())
                val_range = st.slider(f"Filter `{col}`", min_val, max_val, (min_val, max_val))
                df_filtered = df_filtered[df_filtered[col].between(val_range[0], val_range[1])]
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                min_date, max_date = df[col].min().date(), df[col].max().date()
                date_range = st.date_input(f"Filter `{col}`", (min_date, max_date))
                if len(date_range) == 2:
                    df_filtered = df_filtered[
                        (df_filtered[col].dt.date >= date_range[0]) & 
                        (df_filtered[col].dt.date <= date_range[1])
                    ]
            else:
                unique_vals = df[col].dropna().unique().tolist()
                selected_vals = st.multiselect(f"Filter `{col}`", unique_vals, default=unique_vals)
                df_filtered = df_filtered[df_filtered[col].isin(selected_vals)]
                
    return df_filtered


# --- Sidebar Inputs ---
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.radio("Select Data Source Type", ["Parquet Folder", "SQLite Database"])

# ==========================================
# PARQUET FOLDER EXPLORER
# ==========================================
if mode == "Parquet Folder":
    folder_url = st.sidebar.text_input(
        "GitHub Folder URL",
        placeholder="https://github.com/owner/repo/tree/main/data_folder",
        help="URL pointing to the directory containing .parquet files."
    )

    if folder_url:
        try:
            parquet_files = fetch_parquet_files_from_github_folder(folder_url)

            if not parquet_files:
                st.warning("No `.parquet` files found in the specified GitHub directory.")
            else:
                st.sidebar.success(f"Found {len(parquet_files)} Parquet file(s)")
                
                # 1. Select File from Dropdown
                selected_file_name = st.selectbox("Select Parquet File to Render", list(parquet_files.keys()))
                
                if selected_file_name:
                    file_raw_url = parquet_files[selected_file_name]
                    df = load_parquet_from_url(file_raw_url)

                    tab1, tab2, tab3 = st.tabs(["📊 Data Viewer & Filters", "🔀 Pivot Table", "ℹ️ File Schema"])

                    # 2. Data Viewer with Dynamic Filters
                    with tab1:
                        st.subheader(f"Data Preview: `{selected_file_name}`")
                        filtered_df = apply_dataframe_filters(df)
                        st.write(f"Showing **{len(filtered_df)}** of **{len(df)}** rows")
                        st.dataframe(filtered_df, use_container_width=True)

                    # 3. Pivot Table Facility
                    with tab2:
                        st.subheader("Interactive Pivot Table")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            index_cols = st.multiselect("Rows (Index)", df.columns)
                        with col2:
                            columns_cols = st.multiselect("Columns", [c for c in df.columns if c not in index_cols])
                        with col3:
                            values_cols = st.multiselect("Values", [c for c in df.columns if c not in index_cols + columns_cols])
                        with col4:
                            agg_func = st.selectbox(
                                "Aggregation Function", 
                                ["sum", "mean", "count", "min", "max", "std", "median"]
                            )

                        if index_cols and values_cols:
                            try:
                                pivot_df = pd.pivot_table(
                                    df,
                                    index=index_cols,
                                    columns=columns_cols if columns_cols else None,
                                    values=values_cols,
                                    aggfunc=agg_func,
                                    fill_value=0
                                )
                                st.dataframe(pivot_df, use_container_width=True)

                                # Pivot table download
                                csv_data = pivot_df.to_csv().encode("utf-8")
                                st.download_button(
                                    label="📥 Download Pivot Table as CSV",
                                    data=csv_data,
                                    file_name="pivot_table.csv",
                                    mime="text/csv",
                                )
                            except Exception as e:
                                st.error(f"Error building pivot table: {e}")
                        else:
                            st.info("Select at least one Row and one Value column to render the pivot table.")

                    # Schema view tab
                    with tab3:
                        st.subheader("Column Metadata & Data Types")
                        schema_info = pd.DataFrame({
                            "Column Name": df.columns,
                            "Data Type": [str(dtype) for dtype in df.dtypes],
                            "Non-Null Count": df.notnull().sum().values
                        })
                        st.dataframe(schema_info, use_container_width=True)

        except Exception as e:
            st.error(f"Error accessing GitHub folder: {e}")
    else:
        st.info("Please enter a valid GitHub folder URL containing Parquet files.")

# ==========================================
# SQLITE DATABASE EXPLORER
# ==========================================
else:
    repo_db_url = st.sidebar.text_input(
        "GitHub DB File URL",
        placeholder="https://github.com/username/repo/blob/main/database.db",
        help="Enter the direct URL to the .db or .sqlite file in your GitHub repo.",
    )

    if repo_db_url:
        try:
            raw_url = convert_to_raw_url(repo_db_url)
            with st.spinner("Downloading database from GitHub..."):
                db_path = load_database_from_github(raw_url)

            conn = sqlite3.connect(db_path)

            tab1, tab2 = st.tabs(["📋 Schema & Tables", "⚡ SQL Query Runner"])

            with tab1:
                st.header("Database Tables & Overview")
                tables_df = pd.read_sql_query(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';",
                    conn,
                )

                if tables_df.empty:
                    st.warning("No user tables found in this SQLite database.")
                else:
                    table_names = tables_df["name"].tolist()
                    st.success(f"Found **{len(table_names)}** table(s)")

                    selected_table = st.selectbox("Select a table to inspect:", table_names)

                    if selected_table:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader(f"Table Schema: `{selected_table}`")
                            schema_df = pd.read_sql_query(f"PRAGMA table_info('{selected_table}');", conn)
                            st.dataframe(schema_df[["cid", "name", "type", "notnull", "pk"]], use_container_width=True)

                        with col2:
                            st.subheader("Preview First 10 Rows")
                            preview_df = pd.read_sql_query(f"SELECT * FROM '{selected_table}' LIMIT 10;", conn)
                            st.dataframe(preview_df, use_container_width=True)

            with tab2:
                st.header("Execute Custom SQL Queries")
                default_query = (
                    f"SELECT * FROM '{table_names[0]}' LIMIT 50;" if not tables_df.empty else "SELECT 1;"
                )
                user_query = st.text_area("Write SQL Query", value=default_query, height=150)

                if st.button("Run Query", type="primary"):
                    try:
                        result_df = pd.read_sql_query(user_query, conn)
                        st.success(f"Query executed successfully! Returned **{len(result_df)}** row(s).")
                        st.dataframe(result_df, use_container_width=True)

                        csv_data = result_df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv_data,
                            file_name="query_results.csv",
                            mime="text/csv",
                        )
                    except Exception as e:
                        st.error(f"SQL Execution Error: {e}")

            conn.close()

        except Exception as e:
            st.error(f"Error loading database: {e}")
    else:
        st.info("Please enter a valid GitHub database URL in the sidebar.")
