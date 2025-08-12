"""
1. Why Parquet is Usually Faster than CSV
Parquet:
    Columnar storage → reads only required columns.
    Compressed → less I/O from disk.
    Binary format → no parsing of text.

CSV:
    Row-oriented → reads everything, even unused columns.
    No compression by default → more disk space.
    Must parse text → slower CPU performance.
"""

Code Example: DuckDB Timing Test
import duckdb
import time

# Paths to your files
csv_file = "big_data.csv"
parquet_file = "big_data.parquet"

# Example query: only select one column and aggregate
query = "SELECT COUNT(*) FROM data"

# --- Test CSV Read ---
start_csv = time.time()
duckdb.query(f"SELECT * FROM read_csv_auto('{csv_file}') AS data").fetchall()
end_csv = time.time()
csv_time = end_csv - start_csv
print(f"CSV Read Time: {csv_time:.4f} seconds")

# --- Test Parquet Read ---
start_parquet = time.time()
duckdb.query(f"SELECT * FROM read_parquet('{parquet_file}') AS data").fetchall()
end_parquet = time.time()
parquet_time = end_parquet - start_parquet
print(f"Parquet Read Time: {parquet_time:.4f} seconds")

# Compare
if parquet_time < csv_time:
    print(f"✅ Parquet is {csv_time / parquet_time:.2f}x faster")
else:
    print(f"❌ CSV is faster by {parquet_time / csv_time:.2f}x (unlikely for big data)")


3. Expected Output Example
    On a 1M row, 40MB CSV vs 6MB Parquet:
CSV Read Time: 1.8234 seconds
    Parquet Read Time: 0.2741 seconds
    Parquet is 6.65x faster


"""
Why This Happens
    Parquet:
        DuckDB only decompresses relevant column chunks.
        Columnar read avoids unnecessary parsing.
        Less data to pull from disk.
        
    CSV:
        Reads entire file line-by-line.
        Parses strings into types (int, float, etc.).
        Even unused columns are loaded.
"""
