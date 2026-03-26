#!/usr/bin/env python3
"""
Power BI Python Load Script
Copy this script into Power BI's Python script editor for direct CSV loading.
Power BI → Transform Data → Python script
"""

import pandas as pd
import os

# ============================================================================
# CONFIGURATION
# ============================================================================
# Change this path to your CSV folder
DATA_PATH = r"C:\Users\YourUser\Documents\PROJECTS\powerbi\data"

print(f"Loading data from: {DATA_PATH}")

# ============================================================================
# LOAD CSVs
# ============================================================================

try:
    flavors = pd.read_csv(os.path.join(DATA_PATH, "flavors.csv"))
    print(f"✓ Loaded flavors.csv ({len(flavors)} rows)")
except Exception as e:
    print(f"✗ Error loading flavors.csv: {e}")
    flavors = pd.DataFrame()

try:
    apps = pd.read_csv(os.path.join(DATA_PATH, "apps.csv"))
    print(f"✓ Loaded apps.csv ({len(apps)} rows)")
except Exception as e:
    print(f"✗ Error loading apps.csv: {e}")
    apps = pd.DataFrame()

try:
    instances = pd.read_csv(os.path.join(DATA_PATH, "instances.csv"))
    print(f"✓ Loaded instances.csv ({len(instances)} rows)")
except Exception as e:
    print(f"✗ Error loading instances.csv: {e}")
    instances = pd.DataFrame()

try:
    metrics = pd.read_csv(os.path.join(DATA_PATH, "metrics.csv"))
    print(f"✓ Loaded metrics.csv ({len(metrics)} rows)")
except Exception as e:
    print(f"✗ Error loading metrics.csv: {e}")
    metrics = pd.DataFrame()

try:
    timeline = pd.read_csv(os.path.join(DATA_PATH, "timeline.csv"))
    print(f"✓ Loaded timeline.csv ({len(timeline)} rows)")
except Exception as e:
    print(f"✗ Error loading timeline.csv: {e}")
    timeline = pd.DataFrame()

# ============================================================================
# DATA TRANSFORMATIONS (Optional)
# ============================================================================

# Convert date columns to datetime
if not instances.empty and "CreatedDate" in instances.columns:
    instances["CreatedDate"] = pd.to_datetime(instances["CreatedDate"])

if not metrics.empty and "MeasureDate" in metrics.columns:
    metrics["MeasureDate"] = pd.to_datetime(metrics["MeasureDate"])

if not timeline.empty and "SnapshotDate" in timeline.columns:
    timeline["SnapshotDate"] = pd.to_datetime(timeline["SnapshotDate"])

# ============================================================================
# RETURN TO POWER BI
# ============================================================================

# Return all dataframes as separate tables in Power BI
# Power BI will load: Flavors, Apps, Instances, Metrics, Timeline

print("\nDatasets ready for Power BI import.")
