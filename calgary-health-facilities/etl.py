"""
ETL — AFAP portfolio project
Source: City of Calgary Open Data, "Calgary Health Clinics and Hospitals"
Export the dataset as CSV from data.calgary.ca and save it in this folder
(ideally as data.csv). This script reads that local file.

What it does:
  1. EXTRACT   - reads the exported CSV from this folder (data.csv, or any .csv).
  2. PROFILE   - prints each column's null/distinct counts and sample values.
  3. LOAD RAW  - writes the raw flat table to SQLite (table: facilities_raw).
  4. NORMALIZE - AUTOMATICALLY splits categorical columns into lookup tables and
                 builds a 'facility' table with foreign keys. No editing needed.

Setup & run:
  pip install pandas
  python etl.py
"""

import os
import glob
import sqlite3
import pandas as pd

DB_PATH = "calgary_health.db"


def extract():
    """Read the dataset from a local CSV exported from the Calgary open-data portal."""
    path = "data.csv"
    if not os.path.exists(path):
        ours = {"example_queries.csv"}
        candidates = [f for f in glob.glob("*.csv") if f.lower() not in ours]
        if candidates:
            path = candidates[0]
        else:
            raise FileNotFoundError(
                "No CSV found. On data.calgary.ca, open the 'Calgary Health "
                "Clinics and Hospitals' dataset, Export it as CSV, and save it "
                "in this folder (e.g. as data.csv), then re-run."
            )
    df = pd.read_csv(path)
    # Clean column names to snake_case so they're safe as table/column names.
    df.columns = (
        df.columns.str.strip().str.lower()
        .str.replace(r"[^0-9a-z]+", "_", regex=True).str.strip("_")
    )
    print(f"Extracted {len(df)} rows, {len(df.columns)} columns from '{path}'.")
    print("Columns:", list(df.columns))
    return df


def profile(df):
    """Print a quick profile of every column (useful for your data dictionary)."""
    print("\n=== COLUMN PROFILE ===")
    for col in df.columns:
        s = df[col]
        nulls = int(s.isna().sum())
        distinct = int(s.nunique(dropna=True))
        samples = list(s.dropna().astype(str).unique()[:5])
        print(f"\n[{col}]")
        print(f"   nulls: {nulls}/{len(df)}    distinct: {distinct}")
        print(f"   samples: {samples}")
    print("\n=== END PROFILE ===\n")


def load_raw(df, conn):
    """Keep the raw flat table as the source of truth."""
    df.to_sql("facilities_raw", conn, if_exists="replace", index=False)
    print("Loaded raw table: facilities_raw")


def normalize(df, conn):
    """Automatically split categorical columns into lookup tables and build a
    'facility' table with foreign keys. No manual editing required.

    Rule (the same one a data modeller applies by hand): a text column whose
    values repeat across many rows is a category, so it becomes its own lookup
    table and the facility table references it by an id. Columns that are mostly
    unique (name, address, coordinates) stay on the facility table.
    """
    n = len(df)
    facility = df.copy()
    facility.insert(0, "facility_id", range(1, n + 1))

    created = []
    for col in list(df.columns):
        s = df[col]
        distinct = s.nunique(dropna=True)
        is_text = not pd.api.types.is_numeric_dtype(s)
        is_category = is_text and (1 < distinct <= 60) and (distinct < n)
        if not is_category:
            continue
        id_col = f"{col}_id"
        lookup = (
            s.dropna().drop_duplicates().reset_index(drop=True).to_frame(name=col)
        )
        lookup.insert(0, id_col, range(1, len(lookup) + 1))
        lookup.to_sql(f"{col}_lookup", conn, if_exists="replace", index=False)
        facility = facility.merge(lookup, on=col, how="left").drop(columns=[col])
        created.append((f"{col}_lookup", col, id_col))

    facility.to_sql("facility", conn, if_exists="replace", index=False)

    print("\n=== TABLES CREATED ===")
    print(f"facility  ->  {len(facility)} rows;  columns: {list(facility.columns)}")
    for lookup_name, col, id_col in created:
        print(f"{lookup_name}  ->  lookup for '{col}'  (facility.{id_col} links to {lookup_name}.{id_col})")
    if not created:
        print("(No categorical columns found to split out; 'facility' holds all fields.)")
    print("=== END ===\n")


def main():
    df = extract()
    profile(df)
    conn = sqlite3.connect(DB_PATH)
    try:
        load_raw(df, conn)
        normalize(df, conn)
        conn.commit()
    finally:
        conn.close()
    print(f"Done. SQLite database written to: {DB_PATH}")
    print("Next: copy the 'TABLES CREATED' summary above — that's your data model.")


if __name__ == "__main__":
    main()