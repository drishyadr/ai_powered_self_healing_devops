# TUD Telemetry Dataset for Anomaly Detection (CPU & Memory)

## Dataset description
This dataset contains snapshots of host telemetry metrics collected during different workload conditions. It is intended for training and evaluating anomaly detection models (e.g., reconstruction-based autoencoders).

The metrics cover:
- Per-core CPU utilization breakdown by state (percent)
- Memory metrics (bytes)

## Files
This Zenodo record should include the dataset in CSV format and this `README.md`.

Recommended file naming (adjust to your actual file names):
- `train_no_load.csv`, `train_medium_load.csv`, `train_high_load.csv`: training CSVs for different workload scenarios
- `test_telemetry.csv`: test CSV used for evaluation

If you prefer a single file, you can also concatenate all rows into one `telemetry_dataset.csv` and add two extra columns:
- `scenario` in {`no_load`, `medium_load`, `high_load`, ...}
- `split` in {`train`, `test`}

## How the dataset was generated
1. A node was instrumented with a telemetry pipeline (e.g., Prometheus + node exporter) to collect CPU and memory metrics at a fixed sampling interval.
2. Multiple workload scenarios were executed (e.g., no load / medium load / high load).
3. Metrics were exported to CSV with a fixed column order. Each row represents one telemetry snapshot.

Notes:
- CPU values are percentages per core and CPU state. Due to sampling/aggregation, values may occasionally slightly exceed 100.
- `node_memory_MemTotal_bytes` is constant for a given machine (total installed memory).

## Columns
All CSV files share the same schema (38 columns). Units and meanings are listed below.

### CPU columns (percent)
For each core `i` in {0,1,2,3}, the following columns represent the percentage of time spent in the given CPU state during the sampling window:
- `cpu_i_idle`, `cpu_i_iowait`, `cpu_i_irq`, `cpu_i_nice`, `cpu_i_softirq`, `cpu_i_steal`, `cpu_i_system`, `cpu_i_user`

### Memory columns (bytes)
- `memory_used_bytes`: used memory in bytes (as exported by the telemetry pipeline)
- `node_memory_Buffers_bytes`: memory used for buffers
- `node_memory_Cached_bytes`: memory used for page cache
- `node_memory_MemAvailable_bytes`: estimate of memory available for starting new applications
- `node_memory_MemFree_bytes`: unused memory
- `node_memory_MemTotal_bytes`: total installed memory

## Column descriptions (full list)
| Column | Unit | Description |
|---|---|---|
| `cpu_0_idle` | % | Core 0 CPU time in idle state |
| `cpu_0_iowait` | % | Core 0 CPU time waiting on I/O |
| `cpu_0_irq` | % | Core 0 CPU time servicing interrupts |
| `cpu_0_nice` | % | Core 0 CPU time for niced processes |
| `cpu_0_softirq` | % | Core 0 CPU time servicing softirqs |
| `cpu_0_steal` | % | Core 0 CPU time stolen (virtualization) |
| `cpu_0_system` | % | Core 0 CPU time in kernel space |
| `cpu_0_user` | % | Core 0 CPU time in user space |
| `cpu_1_idle` | % | Core 1 CPU time in idle state |
| `cpu_1_iowait` | % | Core 1 CPU time waiting on I/O |
| `cpu_1_irq` | % | Core 1 CPU time servicing interrupts |
| `cpu_1_nice` | % | Core 1 CPU time for niced processes |
| `cpu_1_softirq` | % | Core 1 CPU time servicing softirqs |
| `cpu_1_steal` | % | Core 1 CPU time stolen (virtualization) |
| `cpu_1_system` | % | Core 1 CPU time in kernel space |
| `cpu_1_user` | % | Core 1 CPU time in user space |
| `cpu_2_idle` | % | Core 2 CPU time in idle state |
| `cpu_2_iowait` | % | Core 2 CPU time waiting on I/O |
| `cpu_2_irq` | % | Core 2 CPU time servicing interrupts |
| `cpu_2_nice` | % | Core 2 CPU time for niced processes |
| `cpu_2_softirq` | % | Core 2 CPU time servicing softirqs |
| `cpu_2_steal` | % | Core 2 CPU time stolen (virtualization) |
| `cpu_2_system` | % | Core 2 CPU time in kernel space |
| `cpu_2_user` | % | Core 2 CPU time in user space |
| `cpu_3_idle` | % | Core 3 CPU time in idle state |
| `cpu_3_iowait` | % | Core 3 CPU time waiting on I/O |
| `cpu_3_irq` | % | Core 3 CPU time servicing interrupts |
| `cpu_3_nice` | % | Core 3 CPU time for niced processes |
| `cpu_3_softirq` | % | Core 3 CPU time servicing softirqs |
| `cpu_3_steal` | % | Core 3 CPU time stolen (virtualization) |
| `cpu_3_system` | % | Core 3 CPU time in kernel space |
| `cpu_3_user` | % | Core 3 CPU time in user space |
| `memory_used_bytes` | bytes | Used memory |
| `node_memory_Buffers_bytes` | bytes | Buffers |
| `node_memory_Cached_bytes` | bytes | Cached |
| `node_memory_MemAvailable_bytes` | bytes | MemAvailable |
| `node_memory_MemFree_bytes` | bytes | MemFree |
| `node_memory_MemTotal_bytes` | bytes | MemTotal |

## Summary statistics
The following table reports per-column data type and summary statistics (min / median / max).

This table was computed from the provided file.

| Column | Type | Min | Median | Max |
|---|---:|---:|---:|---:|
| `cpu_0_idle` | `float64` | 0 | 29.03 | 100.5 |
| `cpu_0_iowait` | `float64` | 0 | 0.02 | 16.43 |
| `cpu_0_irq` | `float64` | 0 | 0 | 21.77 |
| `cpu_0_nice` | `float64` | 0 | 0 | 18.78 |
| `cpu_0_softirq` | `float64` | 0 | 0 | 13.74 |
| `cpu_0_steal` | `float64` | 0 | 0 | 18.48 |
| `cpu_0_system` | `float64` | 0 | 0.48 | 22.55 |
| `cpu_0_user` | `float64` | 0 | 30.5 | 63.15 |
| `cpu_1_idle` | `float64` | 0 | 29 | 104 |
| `cpu_1_iowait` | `float64` | 0 | 0.02 | 22.61 |
| `cpu_1_irq` | `float64` | 0 | 0 | 20.17 |
| `cpu_1_nice` | `float64` | 0 | 0 | 17 |
| `cpu_1_softirq` | `float64` | 0 | 0 | 26.32 |
| `cpu_1_steal` | `float64` | 0 | 0 | 17.09 |
| `cpu_1_system` | `float64` | 0 | 0.43 | 35.32 |
| `cpu_1_user` | `float64` | 0 | 30.63 | 75.72 |
| `cpu_2_idle` | `float64` | 0 | 28.91 | 100.4 |
| `cpu_2_iowait` | `float64` | 0 | 0.01 | 19.66 |
| `cpu_2_irq` | `float64` | 0 | 0 | 14.42 |
| `cpu_2_nice` | `float64` | 0 | 0 | 19.61 |
| `cpu_2_softirq` | `float64` | 0 | 0 | 16.19 |
| `cpu_2_steal` | `float64` | 0 | 0 | 15.58 |
| `cpu_2_system` | `float64` | 0 | 0.45 | 33.33 |
| `cpu_2_user` | `float64` | 0 | 30.7 | 86.3 |
| `cpu_3_idle` | `float64` | 0 | 29.01 | 112.5 |
| `cpu_3_iowait` | `float64` | 0 | 0.02 | 14.85 |
| `cpu_3_irq` | `float64` | 0 | 0 | 17.67 |
| `cpu_3_nice` | `float64` | 0 | 0 | 19.58 |
| `cpu_3_softirq` | `float64` | 0 | 0 | 19.25 |
| `cpu_3_steal` | `float64` | 0 | 0 | 15.61 |
| `cpu_3_system` | `float64` | 0 | 0.44 | 29.21 |
| `cpu_3_user` | `float64` | 0 | 30.62 | 70 |
| `memory_used_bytes` | `float64` | 8.89095e+08 | 1.70806e+09 | 3.32244e+09 |
| `node_memory_Buffers_bytes` | `float64` | 1.05865e+08 | 1.16023e+08 | 1.18623e+08 |
| `node_memory_Cached_bytes` | `float64` | 5.08577e+09 | 5.39835e+09 | 5.57918e+09 |
| `node_memory_MemAvailable_bytes` | `float64` | 5.00084e+09 | 6.61521e+09 | 7.43418e+09 |
| `node_memory_MemFree_bytes` | `float64` | 0 | 1.26609e+09 | 1.96274e+09 |
| `node_memory_MemTotal_bytes` | `float64` | 8.32328e+09 | 8.32328e+09 | 8.32328e+09 |





## Reproducing the statistics table
To recompute the summary statistics for one or more CSV files (e.g., all training files plus the test file), run the following locally (requires `pandas` and `numpy`):

```bash
python - <<"PY"
import glob
import numpy as np
import pandas as pd

# Edit paths as needed
files = glob.glob("data/*.csv") + ["telemetry.csv"]

frames = [pd.read_csv(f) for f in files]
df = pd.concat(frames, ignore_index=True, sort=False)

rows = []
for col in df.columns:
    s = df[col]
    dtype = str(s.dtype)
    if pd.api.types.is_numeric_dtype(s):
        arr = s.to_numpy(dtype=float)
        rows.append((col, dtype, np.nanmin(arr), np.nanmedian(arr), np.nanmax(arr)))
    else:
        rows.append((col, dtype, np.nan, np.nan, np.nan))

print("| Column | Type | Min | Median | Max |")
print("|---|---:|---:|---:|---:|")
for col, dtype, mn, med, mx in rows:
    def fmt(v):
        if isinstance(v, float) and np.isnan(v):
            return ""
        av = abs(float(v))
        if av >= 1e6:
            return f"{v:.6g}"
        return f"{v:.4g}"

    print(f"| `{col}` | `{dtype}` | {fmt(mn)} | {fmt(med)} | {fmt(mx)} |")
PY
```
