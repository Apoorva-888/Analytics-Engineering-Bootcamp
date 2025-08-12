# Example in Python
"""
Step 1: We create a pandas DataFrame.
Step 2: Convert it to an Arrow Table (columnar in memory).
Step 3: Convert back to pandas without re-reading from disk.
This demonstrates fast, in-memory data interchange.
"""

```python
import pyarrow as pa
#Loads the Apache Arrow Python API.
#pa will be used to work with Arrow’s in-memory columnar format.

import pandas as pd
#Loads the pandas library for creating and manipulating tabular data in Python.

# Create a pandas DataFrame
df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["A", "B", "C"]
})
"""
Creates a pandas DataFrame — a row/column data structure used widely in Python.
Data:
css
      id  value
      1   A
      2   B
      3   C
In-memory format here: pandas stores data internally as NumPy arrays (row + column hybrid, but not true columnar like Arrow).
If we later want to share this data with another system (e.g., Spark, Arrow, R), normally it would require serialization into a byte format.
"""

# Convert to Apache Arrow Table
arrow_table = pa.Table.from_pandas(df)
"""
Purpose: Converts the DataFrame into an Apache Arrow Table (a true columnar in-memory format).
What happens here:
Data from pandas (NumPy arrays) is copied into Arrow’s memory buffers.
Each column is stored contiguously in memory, improving compression and scan performance.
Why it matters:
Once in Arrow format, the data can be shared across different systems/languages without serialization.
If we were using to_parquet() instead, it would serialize data to a file (disk I/O) — slower and not zero-copy.
"""

# Zero-copy back to pandas
df2 = arrow_table.to_pandas()
"""
Zero-copy means: no full serialization (encode) and deserialization (decode) process happens.
Instead:
The Arrow table’s memory buffers are referenced directly by pandas.
Only minimal metadata conversion happens (e.g., column names, type info).
This avoids:
Creating new copies of all the data.
Wasting CPU on converting formats.
  Without Arrow, typical cross-tool data sharing would look like:
      Memory in System A → Serialize (bytes) → Transfer → Deserialize → Memory in System B
  With Arrow (zero-copy):
      Shared Columnar Buffers in Memory → Directly Referenced in Both Systems
"""
print(arrow_table)
print(df2)
"""
Displays the Arrow table in a readable form:
pyarrow.Table
    id: int64
    value: string
    ----
    id: [[1,2,3]]
    value: [["A","B","C"]]
    Shows column-oriented storage.

print(df2):
Displays the pandas DataFrame reconstructed from the Arrow table:
       id value
    0   1     A
    1   2     B
    2   3     C
"""



"""
Serialization vs Deserialization in This Context
    Serialization = converting in-memory data into a byte stream (for storage or transfer).
    Example: Converting a DataFrame to CSV, JSON, or Parquet.
    This takes CPU, and sometimes changes the layout completely.

Deserialization = reading that byte stream back into an in-memory structure.
    Example: Reading a CSV/Parquet back into pandas.
    Also CPU-heavy, and may require multiple data copies.

Arrow Advantage:
    Arrow’s memory format is already a universal standard understood by many systems.
    So, instead of serializing/deserializing:
    It shares pointers to the same memory buffers between tools.
    This is the zero-copy concept → no unnecessary CPU work.
"""

💡 In Short:
Pandas → Arrow (from_pandas) = convert to true columnar layout.
Arrow → Pandas (to_pandas) = no full serialization/deserialization → zero-copy.
This is why ADBC + Arrow is so powerful for warehouse-to-BI transfers — they skip the row-based conversion bottleneck.
